from django.urls import path
from pelatih.views import register
from pelatih.views import login_user
from pelatih.views import logout_user
from pelatih.views import *

app_name = 'pelatih'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('daftar_atlet/', daftar_atlet, name='daftar_atlet'),
    path('latih_atlet/', latih_atlet, name='latih_atlet'),
    path('dashboard/', dashboard_pelatih, name='dashboard_pelatih')
]