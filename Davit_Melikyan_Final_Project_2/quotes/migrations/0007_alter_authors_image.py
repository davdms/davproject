# Generated by Django 3.2.10 on 2022-05-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0006_alter_quotestotags_quote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='author_images'),
        ),
    ]