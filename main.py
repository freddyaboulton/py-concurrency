from multiprocessing import Queue
import time
from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorker import YahooFinancePriceScheduler


def sleep_a_little(seconds):
    time.sleep(seconds)

def main():
    symbol_queue = Queue()
    calc_start_time = time.time()

    wiki_worker = WikiWorker()
    threads = []
    n_threads = 4
    
    for _ in range(n_threads):
        scheduler = YahooFinancePriceScheduler(queue=symbol_queue)
        scheduler.start()
        threads.append(scheduler)
    
    for symbol in wiki_worker.get_sp_500_companies():
        symbol_queue.put(symbol)
    
    
    for _ in threads:
        symbol_queue.put("DONE")

    [t.join() for t in threads]
    print(f"Extracting prices took {round(time.time() - calc_start_time, 1)}")

    
    #     price_worker = YahooFinanceWorker(symbol)
    #     current_workers.append(price_worker)
    
    # [w.join() for w in current_workers]

    # print(f"Extracting prices took {round(time.time() - calc_start_time, 1)}")
    
    # current_threads = []
    # for i in range(5):
    #     n = (i + 1) * 1000000
    #     worker = SquaredSumWorker(n)
    #     # Every non-daemon thread needs to finish for the program to finish
    #     current_threads.append(worker)
    
    # for i in range(len(current_threads)):
    #     current_threads[i].join()
    
    
    # print(f"Calculating sum of squares took: {round(time.time() - calc_start_time, 1)}")
    # sleep_start_time = time.time()
    # current_threads = []
    # for i in range(1, 6):
    #     worker = SleepyWorker(seconds=i)
    #     #sleep_a_little(i)       
    #     # Loop is blocked until each thread finishes. Sequential.
    #     #thread.join()
    #     current_threads.append(worker)
    
    # [t.join() for t in current_threads]

    # print(f"Sleep took: {round(time.time() - sleep_start_time, 1)}")


if __name__ == "__main__":
    main()