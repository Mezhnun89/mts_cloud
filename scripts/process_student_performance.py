import pandas as pd
import re

def clean_student_id(student_id):
    """Функция для очистки student_id, оставляя только числовые символы."""
    return re.sub(r'\D+', '', str(student_id))

def process_student_performance(input_file='data/StudentsPerformanceFinal.xlsx', output_file='output_data/processed_student_data.xlsx'):
    # Загрузка данных
    df = pd.read_excel(input_file)
    
    # Удаление студентов с отсутствующими оценками по 2 и более предметам
    df['missing_scores'] = df[['math_score', 'reading_score', 'writing_score']].isnull().sum(axis=1)
    df = df[df['missing_scores'] < 2].drop(columns=['missing_scores'])

    # Замена отсутствующих оценок медианой по этому предмету
    df['math_score'].fillna(df['math_score'].median(), inplace=True)
    df['reading_score'].fillna(df['reading_score'].median(), inplace=True)
    df['writing_score'].fillna(df['writing_score'].median(), inplace=True)

    # Очистка столбца student_id
    df['student_id'] = df['student_id'].apply(clean_student_id)

    # Расчет средневзвешенной оценки
    df['weighted_average'] = (
        df['math_score'] * 0.5 +
        df['reading_score'] * 0.2 +
        df['writing_score'] * 0.3
    )

    # Сортировка по средневзвешенной оценке в порядке убывания
    df = df.sort_values(by='weighted_average', ascending=False)

    # Фильтрация студентов с weighted_average > 70
    filtered_df = df[df['weighted_average'] > 70]

    # Сохранение обработанных данных
    filtered_df.to_excel(output_file, index=False)
    print(f"Обработанные данные сохранены в {output_file}")

if __name__ == "__main__":
    process_student_performance()
