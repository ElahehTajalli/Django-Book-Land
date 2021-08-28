# Generated by Django 3.2.1 on 2021-07-21 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='read',
            field=models.ManyToManyField(blank=True, related_name='read', to='books.Book'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='reading',
            field=models.ManyToManyField(blank=True, related_name='reading', to='books.Book'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='wants_to_read',
            field=models.ManyToManyField(blank=True, related_name='wants_to_read', to='books.Book'),
        ),
    ]
