import requests
from bs4 import BeautifulSoup


class Model:
    def __init__(self, number_of_quotes: int, url: str) -> None:
        self.number_of_quotes = number_of_quotes
        self.url = url

    def get_request(self, adding: str = "") -> str:
        url = self.url + adding
        try:
            result = requests.get(url)
            result.raise_for_status()
            return result.text
        except (requests.exceptions.RequestException, ValueError):
            raise ConnectionError("Server is down")

    def parse_request(self, adding: str = "") -> list[str]:
        soup = BeautifulSoup(self.get_request(adding), "html.parser")
        count = self.number_of_quotes
        if adding == "":
            count += 1
        quote_list = soup.findAll("div", class_="quote__body", limit=count)
        filtered_quote_list = list(filter(lambda quote: quote.find_parent("section"), quote_list))
        parsed_quote_list = list(map(lambda x: x.get_text().replace("                    ", ""), filtered_quote_list))
        return parsed_quote_list

    async def main(self, request: int) -> list[str]:
        request_list = ["byrating", "", "random"]
        return self.parse_request(request_list[request])
