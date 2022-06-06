import threading
import requests
from lxml import html
import time
import random


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, queue, **kwargs) -> None:
        super().__init__()
        self._queue = queue
    
    def run(self):
        while True:
            val = self._queue.get()
            if val == "DONE":
                break
            worker = YahooFinanceWorker(symbol=val)
            price = worker.get_price()
            print(price)
            time.sleep(random.random())




class YahooFinanceWorker:

    def __init__(self, symbol: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._symbol = symbol
        self._base_url = f"https://finance.yahoo.com/quote/{self._symbol}"

    
    def get_price(self):
        response = requests.get(self._base_url)
        
        if response.status_code != 200:
            return

        page_contents = html.fromstring(response.text)
        return float(page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')[0].text.replace(",", ""))
        