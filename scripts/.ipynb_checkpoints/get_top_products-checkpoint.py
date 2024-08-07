import pandas as pd
import json
import os

def get_top_products_by_category(category_name, products_file='data/products.csv', sales_file='data/sales.json', output_folder='output_data'):
    try:
        # Проверяем, существует ли папка, и создаем её, если не существует
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Определяем путь к выходному файлу
        output_file = os.path.join(output_folder, 'top_products.csv')

        # Загрузка данных
        products_df = pd.read_csv(products_file)
        with open(sales_file, 'r') as file:
            sales_data = json.load(file)
        sales_df = pd.DataFrame(sales_data)
        
        # Объединение данных для получения полной информации о продажах
        merged_df = pd.merge(sales_df, products_df, on='ProductID', how='left')
        
        # Фильтрация по заданной категории
        category_df = merged_df[merged_df['Category'] == category_name].copy()
        
        if category_df.empty:
            print(f"Категория '{category_name}' не найдена в данных.")
            return
        
        # Добавление столбца с общей суммой продаж для каждой записи
        category_df['SaleAmount'] = category_df['Quantity'] * category_df['Price']
        
        # Группировка по продукту и расчет общего объема продаж
        top_products = category_df.groupby('ProductName').agg(
            Total_Sales=('SaleAmount', 'sum')
        ).nlargest(3, 'Total_Sales').reset_index()
        
        if top_products.empty:
            print(f"Нет данных для категории '{category_name}'.")
        else:
            print(f"\nТоп-3 продукта по объему продаж в категории '{category_name}':")
            print(top_products.to_string(index=False))
            
            # Сохранение топ-3 продуктов в файл
            top_products.to_csv(output_file, index=False)
            print(f"Результаты сохранены в файл {output_file}.")
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")

if __name__ == "__main__":
    category = input("Введите название категории: ")
    get_top_products_by_category(category)
