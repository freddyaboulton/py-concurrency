import threading
import requests
from lxml import html
import time
import random
import datetime

class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, queue, output_queue, **kwargs) -> None:
        super().__init__(**kwargs)
        self._queue = queue
        self._output_queue = output_queue
        self.start()

    
    def run(self):
        while True:
            val = self._queue.get()
            if val == "DONE":
                if self._output_queue is not None:
                    self._output_queue.put("DONE")
                break
            worker = YahooFinanceWorker(symbol=val)
            price = worker.get_price()
            if self._output_queue is not None:
                insert_time = datetime.datetime.fromtimestamp(time.time())
                output = (val, price, insert_time)
                print(output)
                self._output_queue.put(output)
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
        