# Generated by Django 5.0 on 2024-01-10 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/cover/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]