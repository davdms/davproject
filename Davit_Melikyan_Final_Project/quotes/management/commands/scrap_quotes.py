import json
import requests
from bs4 import BeautifulSoup


def get_quotes_list(total_pages):
    quotes = []
    for page_number in range(1, total_pages + 1):
        url = f'https://quotes.toscrape.com/page/{page_number}/'
        response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'})

        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')

        quotes_list = soup.find_all('div', {'class': 'quote'})

        for q in quotes_list:
            tags = []
            quote = q.find('span', {'class': 'text'}).text
            author = q.find('small', {'class': 'author'}).text
            tagslist = q.find('div', {'class': 'tags'}).select('a', {'class': 'tag'})
            for t in tagslist:
                tags.append(t.text)
            quotes.append({
                'quote': quote[1:-1],
                'author': author,
                'tags': tags
            })
    return quotes


def write_in_json(quotes):
    with open('quotes.json', 'w', encoding='UTF8') as f:
        f.write(json.dumps(quotes, ensure_ascii=False))


quotes = get_quotes_list(10)
write_in_json(quotes)
