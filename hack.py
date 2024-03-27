import pandas as pd

# Путь к файлу Excel
file_path = 'Книга 1.xlsx'

# Чтение файла Excel с использованием openpyxl
df = pd.read_excel(file_path, engine='openpyxl')

# Преобразование первой колонки в список
sku_list = df.iloc[:, 0].tolist()

print(sku_list)