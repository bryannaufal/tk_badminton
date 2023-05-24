from django.urls import path
# from babadu.views import index
from babadu.views import pilih_role, register_atlet, register_umpire, register_pelatih
from babadu.views import login
from babadu.views import logout_user
from babadu.views import *

app_name = 'babadu'

urlpatterns = [
    path('', begin_page, name='begin_page'),
    path('register/', pilih_role, name='pilih_role'),
    path('register/atlet', register_atlet, name='register_atlet'),
    path('register/pelatih', register_pelatih, name='register_pelatih'),
    path('register/umpire', register_umpire, name='register_umpire'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('ujian_kualifikasi_buat/', ujian_kualifikasi_buat, name='ujian_kualifikasi_buat'),
    path('ujian_kualifikasi_list/', ujian_kualifikasi_list, name='ujian_kualifikasi_list'),
    path('ujian_kualifikasi_riwayat/', ujian_kualifikasi_riwayat, name='ujian_kualifikasi_riwayat'),
    path('ujian_kualifikasi_soal/', ujian_kualifikasi_soal, name='ujian_kualifikasi_soal')
]