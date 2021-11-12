import os
import pathlib
import sqlite3
import shutil

# вынес словарь значений отдельно для возможности замены сторонним файлом, подключением и т.д.

# для теоритического расширения проекта вполне удобно, мне кажется

class SampleController:
    def __init__(self):
        self.table = f"{os.getcwd()}/PathControl/samples_paths.db"
        self.samples_path = f"{os.getcwd()}/Resources/Samples/"

    def index_samples(self):
        with sqlite3.connect(self.table) as con:
            cur = con.cursor()
            query = """SELECT sample_name FROM path"""
            return cur.execute(query).fetchall()

    def return_sample(self, sample_name):
        with sqlite3.connect(self.table) as con:
            cur = con.cursor()
            query = """SELECT sample_name FROM path WHERE sample_name = ?""", (sample_name,)
            return cur.execute(query).fetchall()

    def create_sample(self, sample_name, file):
        shutil.copy2(file, self.samples_path)
        with sqlite3.connect(self.table) as con:
            cur = con.cursor()
            query = """INSERT INTO path(sample_name) VALUES(?)""", (self.samples_path + sample_name,)
            return cur.execute(query)



    # def _open_connection(self):
