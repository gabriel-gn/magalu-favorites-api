import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "magalu_favorites.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

if __name__ == '__main__':
    import django
    django.setup()

    from random_words import RandomWords
    from django_seed import Seed
    from django.contrib.auth.models import User
    from products.models import *

    rw = RandomWords()
    seeder = Seed.seeder()
    seeder.add_entity(User, 5)
    seeder.add_entity(ProductBrand, 5, {
        'name': lambda x: rw.random_word(),
        'category': lambda x: random.randint(0, len(ProductBrand.CATEGORIES) - 1),
    })
    seeder.add_entity(Product, 50, {
        'title': lambda x: rw.random_word(),
        'description': lambda x: ' '.join(rw.random_words(count=10)),
        'price': lambda x: random.randint(1, 1000),
    })
    seeder.add_entity(ProductReview, 100, {
        'rating': lambda x: random.randint(1, 100),
        'description': lambda x: ' '.join(rw.random_words(count=10)),
    })

    inserted_pks = seeder.execute()