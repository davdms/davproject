# Generated by Django 3.2.10 on 2022-05-13 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_rename_user_id_authors_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quoteshistory',
            old_name='quote',
            new_name='quote_text',
        ),
        migrations.RenameField(
            model_name='quoteshistory',
            old_name='user_id',
            new_name='user',
        ),
    ]
