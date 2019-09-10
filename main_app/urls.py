from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('yorkies/', views.yorkies_index, name='index'),
    path('yorkies/<int:yorkie_id>/', views.yorkies_detail, name='detail'),
    path('yorkies/create/', views.YorkieCreate.as_view(), name="yorkies_create"),
    path('yorkies/<int:pk>/update/', views.YorkieUpdate.as_view(), name='yorkies_update'),
    path('yorkies/<int:pk>/delete/', views.YorkieDelete.as_view(), name='yorkies_delete'),
]