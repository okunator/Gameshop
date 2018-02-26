from django.db import models
from django.utils.text import slugify
from django import template
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def to_json(self):
        json = {'id': self.id, 'name': self.name}
        return json

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    developer = models.ForeignKey(User, related_name='game_developed_by', null=True)
    owners = models.ManyToManyField(User, related_name='game_owned_by')
    genre = models.ForeignKey(Genre, related_name='game_genre')
    description = models.TextField(blank=True, default='')
    coverpicture = models.ImageField(upload_to='cover_pics', blank=True)
    url = models.URLField(null=False, blank=False, unique=True)
    price = models.DecimalField(null=False, blank=False, max_digits=5,
                                decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
    games_sold = models.PositiveIntegerField(default = 0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:gamedetail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
