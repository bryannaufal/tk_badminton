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
    path('dashboard_atlet/', dashboard_atlet, name='dashboard_atlet'),
    path('atlet_ujian_kualifikasi_list/', atlet_ujian_kualifikasi_list, name='atlet_ujian_kualifikasi_list'),
    path('atlet_ujian_kualifikasi_riwayat/', atlet_ujian_kualifikasi_riwayat, name='atlet_ujian_kualifikasi_riwayat'),
    path('atlet_ujian_kualifikasi_soal/', atlet_ujian_kualifikasi_soal, name='atlet_ujian_kualifikasi_soal'),
    path('atlet_daftar_stadium/', atlet_daftar_stadium, name='atlet_daftar_stadium'),
    path('atlet_daftar_stadium/<str:stadium>', atlet_daftar_event, name='atlet_daftar_event'),
    path('atlet_daftar_stadium/<str:stadium>/<str:event>', atlet_daftar_partai, name='atlet_daftar_partai')
]