from rest_framework import serializers
from .models import Category, Product, Partner, BlogPost, Order, ProductReview, Slider, HomeBanner


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'product_count']

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name', 'partner', 'partner_name',
            'image', 'hover_image', 'price', 'old_price', 'label', 'short_description',
            'stock', 'available', 'created',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    extra_images = serializers.SerializerMethodField()
    color_variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_extra_images(self, obj):
        return [img.image.url for img in obj.extra_images.all()]

    def get_color_variants(self, obj):
        return [{'name': v.color_name, 'code': v.color_code, 'image': v.image.url if v.image else None} for v in obj.color_variants.all()]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'slug', 'logo', 'description', 'phone', 'address', 'is_dealer', 'is_seller']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'image', 'excerpt', 'author', 'created', 'views']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'comment', 'created']


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'title', 'subtitle', 'image', 'link_url', 'order']


class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'image', 'link_url', 'order']
