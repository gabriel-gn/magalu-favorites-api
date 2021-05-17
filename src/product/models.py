from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.magalu_favorites.models import DefaultModel


class ProductBrand(DefaultModel):
    CATEGORIES = [
        (0, "Outros"),
        (1, "Alimentação"),
        (2, "Entretenimento"),
        (3, "Informática"),
        (4, "Jardinagem"),
    ]
    name = models.CharField(max_length=256, default='Nova Marca')
    category = models.PositiveIntegerField(choices=CATEGORIES, default=0)

    def __str__(self):
        return self.name


class Product(DefaultModel):
    title = models.CharField(max_length=256, default='Novo Produto')
    description = models.TextField(default='', blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    image = models.CharField(
        max_length=256,
        default='https://picsum.photos/200'
    )
    brand = models.ForeignKey(ProductBrand, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class ProductReview(DefaultModel):
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, default=None, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'({self.pk}) {self.user} - {self.rating}'


class UserFavorites(DefaultModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, symmetrical=False, blank=True)

    def __str__(self):
        return self.user.email  # email == username


@receiver(post_save, sender=User)
def create_user_favorites(sender, instance, created, **kwargs):
    """
    Django signal. Ao criar um novo usuário na base, automaticamente cria uma lista de favoritos atrelado a ele
    """
    if created and not kwargs.get('raw', False):
        UserFavorites.objects.create(user=instance)
