import json

from django.core.management.base import BaseCommand

from quotes.models import Quotes, Authors, Tags, QuotesToTags


class Command(BaseCommand):
    help = 'Loads quotes from json into db.'

    # def add_arguments(self, parser):
    #     parser.add_argument('path', nargs=1, type=str)

    def handle(self, *args, **options):
        # path = options['path'][0]

        with open('quotes.json', 'r') as f:
            data = json.load(f)

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
