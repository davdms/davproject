# Generated by Django 3.2.10 on 2022-05-13 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_quoteshistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotestotags',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.quotes'),
        ),
    ]