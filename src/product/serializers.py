from django.db.models import Avg
from rest_framework import serializers

from src.product.models import Product, ProductReview, ProductBrand
from src.user_profile.serializers import UserSerializer


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = ProductReview
        fields = ['user', 'product', 'rating', 'description']


class ProductBrandSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        """
        Category é um choice field, por isso são armazenados ints no bd
        Para retornar o nome atrelado, é necessário usar o 'get_xxx_display()'
        """
        return obj.get_category_display()

    class Meta:
        model = ProductBrand
        fields = ['name', 'category']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    reviewScore = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    brand = ProductBrandSerializer(many=False, read_only=True)

    def get_id(self, obj):
        """
        Retorna a pk com o nome de 'id', que deve ser única.
        """
        return obj.pk

    def get_reviewScore(self, obj):
        """
        Retorna a média dos reviews do produto
        Caso não seja problema retornar 'null' (já que mean pode ser None), retornar mean diretamente.
        """
        mean = ProductReview.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']
        return mean if mean else 0

    def get_reviews(self, obj):
        """
        Retorna a média dos reviews do produto
        """
        reviews = ProductReview.objects.filter(product=obj)
        serializer = ProductReviewSerializer(reviews, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'brand', 'price', 'image', 'reviewScore', 'reviews']
