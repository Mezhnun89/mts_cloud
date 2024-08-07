import pandas as pd
import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(products_file, sales_file):
    try:
        products_df = pd.read_csv(products_file)
        with open(sales_file, 'r') as file:
            sales_data = json.load(file)
        sales_df = pd.DataFrame(sales_data)
        logging.info("Данные успешно загружены.")
        return products_df, sales_df
    except Exception as e:
        logging.error("Ошибка загрузки данных: %s", e)
        return None, None

def merge_data(products_df, sales_df):
    try:
        sales_df['Date'] = pd.to_datetime(sales_df['Date'])
        sales_df['SaleMonth'] = sales_df['Date'].dt.to_period('M')
        
        merged_df = pd.merge(sales_df, products_df, on='ProductID', how='left')
        logging.info("Данные успешно объединены.")
        return merged_df
    except Exception as e:
        logging.error("Ошибка объединения данных: %s", e)
        return None

def calculate_sales_metrics(merged_df):
    try:
        merged_df['SaleAmount'] = merged_df['Quantity'] * merged_df['Price']
        summary_df = merged_df.groupby(['Category', 'SaleMonth']).agg(
            Total_Sales=('SaleAmount', 'sum'),
            Average_Price=('Price', 'mean'),
            Total_Quantity_Sold=('Quantity', 'sum')
        ).reset_index()
        logging.info("Метрики продаж успешно рассчитаны.")
        return summary_df
    except Exception as e:
        logging.error("Ошибка расчета метрик: %s", e)
        return None

def save_summary_to_csv(summary_df, filename):
    try:
        summary_df.to_csv(filename, index=False)
        logging.info("Результаты успешно сохранены в %s.", filename)
    except Exception as e:
        logging.error("Ошибка сохранения результатов: %s", e)

# Загрузка данных
products_df, sales_df = load_data('data/products.csv', 'data/sales.json')

if products_df is not None and sales_df is not None:
    # Объединение данных
    merged_df = merge_data(products_df, sales_df)
    
    if merged_df is not None:
        # Расчет метрик с разбивкой по месяцам
        summary_df = calculate_sales_metrics(merged_df)
        
        if summary_df is not None:
            # Сохранение результатов
            save_summary_to_csv(summary_df, 'output_data/category_sales_summary.csv')
