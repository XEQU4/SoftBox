from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('start/', views.start_view, name='start'),
    path('random-box/', views.random_box_view, name='random_box'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/opened_boxes/', views.profile_opened_boxes_view, name='profile_opened_boxes'),
    path('profile/created_boxes/', views.profile_created_boxes_view, name='profile_created_boxes'),
    path('create_message/', views.create_message_view, name='create_message'),
    path('choose_category/', views.choose_category_view, name='choose_category'),
    path('box/<int:number>/', views.box_detail_view, name='box_detail'),
]
