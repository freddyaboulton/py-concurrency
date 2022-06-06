import requests
from bs4 import BeautifulSoup

class WikiWorker:

    def __init__(self) -> None:
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    def get_sp_500_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Cannot get S&P")
            return []
        yield from self._extract_company_symbols(response.text)
    
    @staticmethod
    def _extract_company_symbols(html):
        soup = BeautifulSoup(html)
        table = soup.find(id="constituents")
        table_rows = table.find_all("tr")
        # Skip header
        for table_row in table_rows[1:]:
            symbol = table_row.find("td").text.strip("\n")
            yield symbol