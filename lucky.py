import bs4
import webbrowser
import requests
import argparse
from fake_useragent import UserAgent


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(self)

        self.add_argument('--request', '-r', default='kitties pics')
        self.add_argument('--search_engine', '-se', default='yandex')
        self.add_argument('--number', '-n', default=5, type=int)

    def get_engine(self):
        return self.parse_args().search_engine

    def get_request(self):
        return self.parse_args().request

    def get_url_number(self):
        return self.parse_args().number


class Scrapper:
    def __init__(self, engine, request):
        self.request = request
        self.search_engines = {
            'google': self._get_from_google,
            'yandex': self._get_from_yandex
        }
        if engine not in self.search_engines:
            raise Exception('Engine is not valid, try another!')

        self.engine = self.search_engines[engine]
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
        }

    def _get_from_google(self):
        """Находит на (1) странице запроса все ссылки и вовращает их"""
        page = requests.get(
            f'https://www.google.com/search?q={self.request}', headers=self.headers)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        return [div.find('a')['href'] for div in soup.find_all('div', class_='r')]

    def _get_from_yandex(self):
        """Находит на (1) странице запроса все ссылки и вовращает их"""
        page = requests.get(
            f'https://yandex.ru/search/?lr=10000&text={self.request}', headers=self.headers)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', class_=['organic__url', 'OrganicTitle-Link'])]

    def get_urls(self, num):
        """Возвращает первые num или меньше ссылок"""
        return self.engine()[: min(len(self.engine()), num)]


def main():
    cmd = Parser()
    scr = Scrapper(cmd.get_engine(), cmd.get_request())
    print(f'Гуглим с помощью {cmd.get_engine()}')
    for url in scr.get_urls(cmd.get_url_number()):
        print(url)
        webbrowser.open_new_tab(url)
    print('Готово!')


if __name__ == '__main__':
    main()
