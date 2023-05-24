from django.urls import path
# from babadu.views import index
from babadu.views import register
from babadu.views import login_user
from babadu.views import logout_user
from babadu.views import *

app_name = 'babadu'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('ujian_kualifikasi_buat/', ujian_kualifikasi_buat, name='ujian_kualifikasi_buat'),
    path('ujian_kualifikasi_list/', ujian_kualifikasi_list, name='ujian_kualifikasi_list'),
    path('ujian_kualifikasi_riwayat/', ujian_kualifikasi_riwayat, name='ujian_kualifikasi_riwayat'),
    path('ujian_kualifikasi_soal/', ujian_kualifikasi_soal, name='ujian_kualifikasi_soal')
]