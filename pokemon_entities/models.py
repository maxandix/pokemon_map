from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='название на русском')
    title_en = models.CharField(max_length=200, verbose_name='название на английском', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='название на японском', blank=True)
    photo = models.ImageField(upload_to='pokemon', verbose_name='фото', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='описание')
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.SET_NULL,
                                           related_name='next_evolutions',
                                           verbose_name='предыдущая эволюция',
                                           null=True, blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='покемон', related_name='entities')
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='появится в', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='исчезнет в', null=True, blank=True)

    level = models.IntegerField(verbose_name='уровень', blank=True)
    health = models.IntegerField(verbose_name='здоровье', blank=True)
    strength = models.IntegerField(verbose_name='атака', blank=True)
    defence = models.IntegerField(verbose_name='защита', blank=True)
    stamina = models.IntegerField(verbose_name='выносливось', blank=True)


    def __str__(self):
        return f'{self.pokemon} entity at {self.lat}, {self.lon}'
