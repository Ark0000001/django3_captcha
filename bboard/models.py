
from django.db import models


class Bb(models.Model):

    title = models.CharField(max_length=100, verbose_name='Товар', default='Какой-то товар')
    # slug = models.SlugField(max_length=50, unique_for_date='publish')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', help_text='руб.')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано', help_text='Дата и время публикации товара')

    rubric=models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')



    class Meta:
        verbose_name_plural='Объявления'
        verbose_name='Объявление'
        ordering=['-published']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Рубрики'
        verbose_name='Рубрика'
        ordering=['name']