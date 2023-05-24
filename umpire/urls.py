from django.urls import path
from umpire.views import register
from umpire.views import login_user
from umpire.views import logout_user
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('umpire_ujian_kualifikasi_list/', umpire_ujian_kualifikasi_list, name='umpire_ujian_kualifikasi_list'),
    path('umpire_ujian_kualifikasi_riwayat/', umpire_ujian_kualifikasi_riwayat, name='umpire_ujian_kualifikasi_riwayat'),
    path('umpire_ujian_kualifikasi_buat/', umpire_ujian_kualifikasi_buat, name='umpire_ujian_kualifikasi_buat')
]