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
    path('yorkies/<int:yorkie_id>/add_grooming/', views.add_grooming, name='add_grooming'),
    path('yorkies/<int:yorkie_id>/add_photo/', views.add_photo, name='add_photo'),

    path('yorkies/<int:yorkie_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),

    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
]