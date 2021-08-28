# Generated by Django 3.2.1 on 2021-07-21 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.ManyToManyField(related_name='read', to='books.Book')),
                ('reading', models.ManyToManyField(related_name='reading', to='books.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wants_to_read', models.ManyToManyField(related_name='wants_to_read', to='books.Book')),
            ],
        ),
    ]
