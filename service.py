import os

import requests
import pandas as pd
from aiogram import types
from aiogram.fsm.context import FSMContext

from config import WB_API_URL
from keyboards.reply import reply_keyboard, reply_keyboard_remove, reply_cancel_keyboard
from config import bot


def get_product_info(sku):
    response = requests.get(WB_API_URL + str(sku))
    return response.json()['data']['products'][0]


async def get_list_from_excel(message: types.Message, state: FSMContext):
    sku_list = None
    if message.document is None:
        await message.answer('Некорректный формат файла', reply_markup=reply_cancel_keyboard)
    elif message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        await message.answer('Собираю информацию...', reply_markup=reply_keyboard_remove)

        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, f'excel_files/{message.document.file_name}')

        try:
            df = pd.read_excel(f'excel_files/{message.document.file_name}')
            sku_list = df.iloc[:, 0].tolist()
            await state.update_data(sku=sku_list)
            await state.clear()
        except Exception as e:
            await state.clear()
            await message.answer(f"Произошла ошибка при обработке файла: {e}", reply_markup=reply_keyboard)
        os.remove(f'excel_files/{message.document.file_name}')
    else:
        await message.answer('Некорректный формат файла', reply_markup=reply_cancel_keyboard)
    return sku_list



async def send_bad_feedback_by_sku(message: types.Message, sku: int):
    product_data = get_product_info(sku)
    root = product_data['root']
    api_url_1 = f'https://feedbacks1.wb.ru/feedbacks/v1/{root}'
    api_url_2 = f'https://feedbacks2.wb.ru/feedbacks/v1/{root}'

    if requests.get(api_url_1).json()['feedbacks'] is not None:
        response = requests.get(api_url_1)
    else:
        response = requests.get(api_url_2)

    product_name = product_data.get('name')
    product_rating = product_data.get('reviewRating')
    response_data = response.json()

    counter = 0
    for feedback in response_data['feedbacks']:
        counter += 1
        if feedback.get('productValuation') < 5:
            feedback_text = feedback.get('text')
            stars_count = feedback.get('productValuation')
            stars_string = '⭐' * stars_count

            answer_message = (

                f'<b>Название товара:</b>{product_name}\n\n'
                f'<b>Артикул:</b> <b>{sku}</b>\n\n'
                f'<b>Оценка</b>: {stars_string}\n\n'
                f'<b>Содержание отзыва:</b> \n{feedback_text}\n\n'
                f'<b>Рейтинг товара:</b> {float(product_rating)}\n\n'
            )

            await message.answer(answer_message, parse_mode='HTML')
            if counter >= 3:
                break  # Отправляем только 3 отзыва, чтобы не нагружать компьютер и не вызывать ошибку
