import csv
import sqlite3

def create_table(cursor, table_name, columns_types):
    columns_str = ', '.join(columns_types)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

def insert_data(cursor, table_name, columns, data):
    placeholders = ', '.join(['?' for _ in columns])
    cursor.executemany(
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
        data
    )

def csv_to_sqlite(csv_file, db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Nama kolom dan tipe datanya
    # Definisikan kolom dan tipe data yang sesuai dengan dataset Anda
    columns_types = [
        'age INTEGER',
        'workclass TEXT',
        'fnlwgt INTEGER',
        'education TEXT',
        'education_num INTEGER',
        'marital_status TEXT',
        'occupation TEXT',
        'relationship TEXT',
        'race TEXT',
        'sex TEXT',
        'capital_gain INTEGER',
        'capital_loss INTEGER',
        'hours_per_week INTEGER',
        'native_country TEXT',
        'income TEXT'
    ]
    column_names = [col.split()[0] for col in columns_types]

    create_table(cursor, table_name, columns_types)

    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Lewati header
        data = [row for row in csvreader]

    insert_data(cursor, table_name, column_names, data)

    conn.commit()
    conn.close()

# Contoh penggunaan:
csv_file = 'adult.csv'
db_file = 'adult.db'
table_name = 'adults'

csv_to_sqlite(csv_file, db_file, table_name)