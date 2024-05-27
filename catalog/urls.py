from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),

    # path('cars/', CarListView.as_view(),name='cars'),
    path('about us', views.aboutUs, name='about us'),
    path('authorisation', views.authorisation, name='authorisation'),
    path('registration', views.registration, name='registration'),
    path('car_list', views.CarListView.as_view(), name='car_list'),
    path('cars/<str:slug>/', views.CarDetailView.as_view(),name='car_detail'),
    path('create_user', views.create_user, name='create_user'),
    path('rating', views.RatingCreateView.as_view(), name='rating'),
    path('upload-rating', views.UploatRating, name='upload-rating'),
    path('user/<str:slug>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('login_user', views.login_user, name='login_user'),
    path('order_car', views.OrderCar.as_view(), name='order_user'),
]
