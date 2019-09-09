from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('yorkies/', views.cats_index, name='index'),
    path('yorkies/<int:yorkie_id>/', views.cats_detail, name='detail'),
]