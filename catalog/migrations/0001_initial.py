# Generated by Django 5.0.6 on 2024-05-13 15:52

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text='Модель автомобиля', max_length=30, unique=True)),
                ('price', models.IntegerField(help_text='Цена автомобиля')),
                ('type', models.CharField(help_text='Тип двигателя', max_length=30)),
                ('power', models.IntegerField(help_text='Мощность двигателя')),
                ('volume', models.IntegerField(help_text='Топливного бака(л)')),
                ('maxTorque', models.IntegerField(help_text='Максимальная крутящий момент')),
                ('length', models.IntegerField(help_text='Длина кузова')),
                ('height', models.IntegerField(help_text='высота кузова')),
                ('width', models.IntegerField(help_text='Ширина кузова')),
                ('transmission', models.CharField(help_text='Тип коробки передач', max_length=30)),
                ('drive', models.CharField(help_text='Привод', max_length=30)),
                ('seats', models.IntegerField(help_text='Количество мест в автомобиле')),
                ('acceleration', models.IntegerField(help_text='Разгон 0-100 км/ч')),
                ('maxSpeed', models.IntegerField(help_text='Максимальная скорость')),
                ('yearManufacture', models.DateField(blank=True, help_text='Год выпуска', null=True)),
                ('cardImage', models.ImageField(help_text='Картинка на карточке автомобиля', upload_to='')),
                ('slideImage1', models.ImageField(default='7d441c5s-1920.jpg', help_text='Картинка на слайде 1', upload_to='')),
                ('slideImage2', models.ImageField(default='7d441c5s-1920.jpg', help_text='Картинка на слайде 2', upload_to='')),
                ('slug', models.CharField(blank=True, help_text='URL', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный идентификатор для конкретного экземпляра автомобиля', primary_key=True, serialize=False)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.car')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')], verbose_name='Значение')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Адрес')),
                ('car', models.ForeignKey(help_text='Автомобиль', on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='catalog.car')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
