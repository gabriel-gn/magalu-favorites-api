from django.db.models import Avg
from rest_framework import serializers

from src.product.models import Product, ProductReview
from src.user_profile.serializers import UserSerializer


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = ProductReview
        fields = ['user', 'product', 'rating', 'description']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    review_score = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_id(self, obj):
        """
        Retorna a pk com o nome de 'id', que deve ser única.
        """
        return obj.pk

    def get_review_score(self, obj):
        """
        Retorna a média dos reviews do produto
        """
        return ProductReview.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']

    def get_reviews(self, obj):
        """
        Retorna a média dos reviews do produto
        """
        reviews = ProductReview.objects.filter(product=obj)
        serializer = ProductReviewSerializer(reviews, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'review_score', 'reviews']
