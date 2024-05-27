from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from pytils.translit import slugify
from django.core.validators import FileExtensionValidator

from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

# from models.services.utils import unique_slugify


User = get_user_model()


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid.uuid4().hex[:8]}'
    return unique_slug


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    order = models.ForeignKey('CarInstance', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.get_username()

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Car(models.Model):
    model = models.CharField(max_length=30, help_text="Модель автомобиля", unique=True)
    price = models.IntegerField(help_text="Цена автомобиля")

    type = models.CharField(max_length=30, help_text="Тип двигателя")
    power = models.IntegerField(help_text="Мощность двигателя")
    volume = models.IntegerField(help_text="Топливного бака(л)")
    maxTorque = models.IntegerField(help_text="Максимальная крутящий момент")

    length = models.IntegerField(help_text="Длина кузова")
    height = models.IntegerField(help_text="высота кузова")
    width = models.IntegerField(help_text="Ширина кузова")

    transmission = models.CharField(max_length=30, help_text="Тип коробки передач")
    drive = models.CharField(max_length=30, help_text="Привод")
    seats = models.IntegerField(help_text="Количество мест в автомобиле")

    acceleration = models.IntegerField(help_text="Разгон 0-100 км/ч")
    maxSpeed = models.IntegerField(help_text="Максимальная скорость")
    yearManufacture = models.DateField(null=True, blank=True, help_text="Год выпуска")

    cardImage = models.ImageField(help_text="Картинка на карточке автомобиля")
    slideImage1 = models.ImageField(help_text="Картинка на слайде 1", default='7d441c5s-1920.jpg')
    slideImage2 = models.ImageField(help_text="Картинка на слайде 2", default='7d441c5s-1920.jpg')
    slug = models.CharField(help_text='URL', max_length=255, blank=True, unique=True)

    def __str__(self):
        return "%s" % (self.model)

    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'slug': self.slug})

    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])




def generate_order_number():
    order_number = str(uuid.uuid4().fields[-1])[:10].upper()
    return order_number
class CarInstance(models.Model):
  number = models.CharField(max_length=10,default=generate_order_number,unique=True, help_text="Номер заказа")
  car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
  due_start = models.DateField(null=True, blank=True)
  due_back = models.DateField(null=True, blank=True)
  address = models.CharField(max_length=200, null=True, blank=True)
  cost = models.IntegerField(null=True, blank=True)

  def save(self, *args, **kwargs):
      if not self.number:
          self.number = generate_order_number()
      super(CarInstance, self).save(*args, **kwargs)

  def __str__(self):
      return self.number


class Rating(models.Model):
    car = models.ForeignKey(to=Car, on_delete=models.CASCADE, help_text="Автомобиль", related_name='ratings')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Значение', choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    def __str__(self):
        return self.car.model



