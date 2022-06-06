from readline import insert_text
import threading
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, queue, output_queue=None, **kwargs):
        super().__init__(**kwargs)
        self._queue = queue
        self._output_queue = output_queue
        self.start()
    
    def run(self):
        while True:
            val = self._queue.get()
            print(val)
            if val == "DONE":
                break
            symbol, price, extracted_time = val
            worker = PostgresWorker(symbol, price, extracted_time)
            worker.insert()



class PostgresWorker:
    def __init__(self, symbol, price, insert_time):
        self._symbol = symbol
        self._price = price
        self._insert_time = insert_time

        self._PG_USER = os.environ.get("PG_USER") or "postgres"
        self._PG_PW = os.environ.get("PG_PW") or "postgres"
        self._PG_HOST = os.environ.get("PG_HOST") or "localhost:5438"
        self._PG_DB = os.environ.get("PG_DB") or "postgres"

        self._engine = create_engine(f"postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}")
    
    def _create_insert_query(self):
        sql = """INSERT INTO prices (symbol, price, insert_time) VALUES 
        (:symbol, :price, :insert_time)"""
        return sql


    def insert(self):
        query  = self._create_insert_query()

        with self._engine.connect() as conn:
            conn.execute(text(query), {"symbol": self._symbol,
                                       "price": self._price,
                                       "insert_time": self._insert_time})




