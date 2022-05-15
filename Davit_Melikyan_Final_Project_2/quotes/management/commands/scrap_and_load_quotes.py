import json
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from quotes.models import Quotes, Authors, Tags, QuotesToTags


def get_quotes_list(total_pages):
    quotesinfo = []
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
            quotesinfo.append({
                'quote': quote[1:-1],
                'author': author,
                'tags': tags
            })
    return quotesinfo


class Command(BaseCommand):
    help = 'Scrap and loads quotes into db.'

    # def add_arguments(self, parser):
    #     parser.add_argument('path', nargs=1, type=str)

    def handle(self, *args, **options):
        # path = options['path'][0]

        data = get_quotes_list(10)

        authors = set()
        for q in data:
            authors.add(q['author'])
        
        _ = Authors.objects.bulk_create(
            [Authors(name=name) for name in authors],
            ignore_conflicts=True,
        )

        authors = Authors.objects.all()
        author_name_id = {c.name: c.pk for c in authors}
        # {'Einstain': 50}

        tags = set()
        for t in data:
            ts = t['tags']
            if len(ts) != 0:
                for tag in ts:
                    tags.add(tag)

        _ = Tags.objects.bulk_create(
            [Tags(name=name) for name in tags],
            ignore_conflicts=True,
        )

        tags = Tags.objects.all()
        tag_name_id = {c.name: c.pk for c in tags}
        # {'world': 50}


        quotes = []
        for q in data:

            c = Quotes(
                quote=q['quote'],
                author_id=author_name_id[q['author']],
            )

            quotes.append(c)

        Quotes.objects.bulk_create(quotes, ignore_conflicts=True)
        quotes = Quotes.objects.all()
        quote_name_id = {c.quote: c.pk for c in quotes}

        quotestotags = []
        for t in data:
            ts = t['tags']
            q = t['quote']
            if len(ts) != 0:
                for tag in ts:
                    c = QuotesToTags(
                        quote_id=quote_name_id[q],
                        tag_id=tag_name_id[tag],
                    )
                    quotestotags.append(c)

        QuotesToTags.objects.bulk_create(quotestotags, ignore_conflicts=True)
