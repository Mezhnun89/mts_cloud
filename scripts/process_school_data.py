import pandas as pd
import re

def clean_state_code(state_code):
    """Функция для очистки state_code, оставляя только буквенно-цифровые символы."""
    return re.sub(r'\W+', '', state_code)

def process_school_data(input_file='data/school_data (1).xlsx', output_file='output_data/processed_school_data.xlsx'):
    # Загрузка данных
    df = pd.read_excel(input_file)
    
    # Фильтрация школ, предлагающих менее 3 предметов
    df['subject_count'] = df['subjects'].apply(lambda x: len(x.split()))
    df = df[df['subject_count'] >= 3].drop(columns=['subject_count'])

    # Очистка столбца state_code
    df['state_code'] = df['state_code'].apply(clean_state_code)

    # Инициализация столбцов для подсчета предметов
    df['english_count'] = df['subjects'].apply(lambda x: 1 if 'english' in x.split() else 0)
    df['maths_count'] = df['subjects'].apply(lambda x: 1 if 'maths' in x.split() else 0)
    df['physics_count'] = df['subjects'].apply(lambda x: 1 if 'physics' in x.split() else 0)
    df['chemistry_count'] = df['subjects'].apply(lambda x: 1 if 'chemistry' in x.split() else 0)

    # Группировка по state_code и суммирование количества школ, предлагающих каждый предмет
    summary_df = df.groupby('state_code').agg(
        english_schools=('english_count', 'sum'),
        maths_schools=('maths_count', 'sum'),
        physics_schools=('physics_count', 'sum'),
        chemistry_schools=('chemistry_count', 'sum')
    ).reset_index()

    # Сохранение обработанных данных
    summary_df.to_excel(output_file, index=False)
    print(f"Обработанные данные сохранены в {output_file}")

if __name__ == "__main__":
    process_school_data()
