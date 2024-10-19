from django.urls import path
from .views import register, login, LogoutAPIView, ProfileAPIView, AccountDeleteAPIView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', LogoutAPIView.as_view(), name = 'logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('delete_account/', AccountDeleteAPIView.as_view(), name='detete_account'),
]