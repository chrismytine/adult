import sqlite3
import csv
from config import DATABASE

class CSVDatabaseManager:
    def __init__(self, database):
        self.database = database

    def create_adult_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS adults (
                    age INTEGER,
                    workclass TEXT,
                    fnlwgt INTEGER,
                    education TEXT,
                    education_num INTEGER,
                    marital_status TEXT,
                    occupation TEXT,
                    relationship TEXT,
                    race TEXT,
                    sex TEXT,
                    capital_gain INTEGER,
                    capital_loss INTEGER,
                    hours_per_week INTEGER,
                    native_country TEXT,
                    income TEXT
                )
            ''')
            conn.commit()

    def insert_adult_data(self, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany('''
                INSERT INTO adults (
                    age, workclass, fnlwgt, education, education_num,
                    marital_status, occupation, relationship, race, sex,
                    capital_gain, capital_loss, hours_per_week, native_country, income
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()

    def load_csv_data(self, csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            return [row for row in reader]

    def get_all_data(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM adults')
            return cur.fetchall()

# === Pemakaian ===

if __name__ == '__main__':
    csv_file = 'adult.csv'  # pastikan file ada
    manager = CSVDatabaseManager(DATABASE)

    manager.create_adult_table()

    data = manager.load_csv_data(csv_file)
    manager.insert_adult_data(data)

    # Tes ambil 5 data
    all_data = manager.get_all_data()
    for row in all_data[:5]:
        print(row)