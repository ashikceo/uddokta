from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('categories', api_views.CategoryViewSet)
router.register('products', api_views.ProductViewSet)
router.register('partners', api_views.PartnerViewSet)
router.register('blog', api_views.BlogPostViewSet)
router.register('orders', api_views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('sliders/', api_views.SliderListView.as_view(), name='api-sliders'),
    path('banners/', api_views.HomeBannerListView.as_view(), name='api-banners'),
    path('products/<int:product_pk>/reviews/', api_views.ProductReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-product-reviews'),
    path('auth/', include('rest_framework.urls')),
]
