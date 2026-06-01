from django.db.models import Q
from rest_framework import viewsets, filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Partner, BlogPost, Order, ProductReview, Slider, HomeBanner
from .serializers import (
    CategorySerializer, ProductSerializer, ProductDetailSerializer,
    PartnerSerializer, BlogPostSerializer, OrderSerializer,
    ProductReviewSerializer, SliderSerializer, HomeBannerSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True, trashed=False).filter(Q(partner__isnull=True) | Q(partner__show_products=True)).select_related('category', 'partner')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'partner', 'label', 'available']
    search_fields = ['name', 'short_description']
    ordering_fields = ['price', 'created', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer


class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address', 'description']


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    ordering = ['-created']


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SliderListView(generics.ListAPIView):
    queryset = Slider.objects.filter(is_active=True)
    serializer_class = SliderSerializer


class HomeBannerListView(generics.ListAPIView):
    queryset = HomeBanner.objects.filter(is_active=True)
    serializer_class = HomeBannerSerializer
