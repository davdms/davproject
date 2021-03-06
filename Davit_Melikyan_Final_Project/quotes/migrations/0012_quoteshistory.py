# Generated by Django 3.2.10 on 2022-05-13 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotes', '0011_delete_quoteshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.IntegerField()),
                ('quote_text', models.TextField()),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'history_quotes',
            },
        ),
    ]
