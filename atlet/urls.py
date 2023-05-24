from django.urls import path
from atlet.views import register
from atlet.views import login_user
from atlet.views import logout_user
from atlet.views import *

app_name = 'atlet'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('atlet_ujian_kualifikasi_list/', atlet_ujian_kualifikasi_list, name='atlet_ujian_kualifikasi_list'),
    path('atlet_ujian_kualifikasi_riwayat/', atlet_ujian_kualifikasi_riwayat, name='atlet_ujian_kualifikasi_riwayat'),
    path('atlet_ujian_kualifikasi_soal/', atlet_ujian_kualifikasi_soal, name='atlet_ujian_kualifikasi_soal')
]