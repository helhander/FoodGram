# Generated by Django 2.2.19 on 2022-08-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, max_length=7, verbose_name='Цвет в HEX'),
        ),
    ]
