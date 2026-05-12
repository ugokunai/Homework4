import pandas as pd
from sqlalchemy import create_engine
import time
import sqlalchemy

# Параметри підключення
DB_URL = "mysql+mysqlconnector://user:password@localhost:3306/my_database"

def get_data_with_retry(max_retries=10, delay=10):
    engine = create_engine(DB_URL)
    attempt = 1
    
    while attempt <= max_retries:
        try:
            print(f"Спроба підключення {attempt}/{max_retries}...")
            query = "SELECT * FROM titanic"
            df = pd.read_sql(query, engine)
            print("Успішно підключено та зчитано дані!")
            return df
        except Exception as e:
            print(f"Помилка: База ще не готова або виникла проблема: {e}")
            attempt += 1
            if attempt <= max_retries:
                print(f"Чекаємо {delay} секунд перед наступною спробою...")
                time.sleep(delay)
            else:
                print("Всі спроби вичерпано. Перевірте статус контейнера.")
                return None

if __name__ == "__main__":
    df = get_data_with_retry()
    
    if df is not None:
        print("\n--- Перші 5 рядків датасету ---")
        print(df.head())
        print(f"\nЗагальна кількість рядків: {len(df)}")
        print("\n--- Кількість NULL значень по колонках ---")
        print(df.isnull().sum())