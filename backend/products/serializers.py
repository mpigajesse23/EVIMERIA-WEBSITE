from rest_framework import serializers
from .models import Category, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'image_url']
        
    def get_image_url(self, obj):
        # Utiliser la méthode get_image_url du modèle
        return obj.get_image_url

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'stock', 'available', 'featured', 'category', 
            'category_name', 'images', 'created_at'
        ]

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'image_url', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_published=True).count()
        
    def get_image_url(self, obj):
        # Utiliser la méthode get_image_url du modèle
        return obj.get_image_url

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'stock', 'available', 'featured', 'category', 
            'images', 'created_at', 'updated_at'
        ] 