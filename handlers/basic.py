from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from service import get_list_from_excel, send_bad_feedback_by_sku
from keyboards.reply import reply_keyboard, reply_keyboard_remove, reply_cancel_keyboard

basic_router = Router()


class ProductState(StatesGroup):
    sku = State()


@basic_router.message(CommandStart())
async def start_command_handler(message: types.Message):
    await message.answer('Привет! Нажми на кнопку "Получить информацию по товару 📑"', reply_markup=reply_keyboard)


@basic_router.message(StateFilter(None))
@basic_router.message(F.text.casefold() == 'получить информацию по товару 📑')
async def input_sku_command_handler(message: types.Message, state: FSMContext):
    await message.answer('Отправьте excel файл', reply_markup=reply_cancel_keyboard)

    await state.set_state(ProductState.sku)


@basic_router.message(F.text.casefold() == 'отмена ❌')
async def cancel_command_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено', reply_markup=reply_keyboard_remove)


@basic_router.message(ProductState.sku)
async def send_bad_feedback(message: types.Message, state: FSMContext):
    sku_list = await get_list_from_excel(message, state)

    if sku_list is not None:
        for sku in sku_list:
            await send_bad_feedback_by_sku(message, sku)

        await message.answer('Готово!', reply_markup=reply_keyboard)
