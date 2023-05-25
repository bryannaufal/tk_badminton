from django.urls import path
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('umpire_ujian_kualifikasi_list/', umpire_ujian_kualifikasi_list, name='umpire_ujian_kualifikasi_list'),
    path('umpire_ujian_kualifikasi_riwayat/', umpire_ujian_kualifikasi_riwayat, name='umpire_ujian_kualifikasi_riwayat'),
    path('umpire_ujian_kualifikasi_buat/', umpire_ujian_kualifikasi_buat, name='umpire_ujian_kualifikasi_buat'),
    path('lihat_daftar_atlet/', lihat_daftar_atlet, name='lihat_daftar_atlet'),
    path('daftar_partai_kompetisi/', lihat_partai_kompetisi, name='lihat_partai_kompetisi'),
    path('lihat_hasil_pertandingan/', lihat_hasil_pertandingan, name='lihat_hasil_pertandingan'),
    path('dashboard/', dashboard_umpire, name='dashboard_umpire'),
    path('dashboard/', umpire_ujian_kualifikasi_riwayat, name='umpire_ujian_kualifikasi_riwayat'),
    path('perempat/', perempat, name='perempat')
]