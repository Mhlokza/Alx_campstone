from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ReviewViewSet, OrderViewSet, RateViewset

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'ratings', RateViewset)
router.register(r'orders', OrderViewSet, basename = 'order')

urlpatterns = [
    path('', include(router.urls)),

]