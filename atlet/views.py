from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from pprint import pprint

@login_required(login_url='login/')
def show_wishlist(request):
    return render(request, "babadu.html")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('babadu:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('babadu:show_wishlist')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('babadu:login')

from collections import namedtuple
from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import render
from collections import namedtuple
from django.db import connection
from datetime import datetime as dt

# Create your views here.
def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def atlet_ujian_kualifikasi_list(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['atlet_ujian_kualifikasi_list'] = cursor.fetchall()
        print(response['atlet_ujian_kualifikasi_list'])
        return render(request, "atlet_ujian_kualifikasi_list.html", response)

def atlet_ujian_kualifikasi_riwayat(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['atlet_ujian_kualifikasi_riwayat'] = cursor.fetchall()
        print(response['atlet_ujian_kualifikasi_riwayat'])
        return render(request, "atlet_ujian_kualifikasi_riwayat.html", response)

def atlet_ujian_kualifikasi_soal(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['atlet_ujian_kualifikasi_soal'] = cursor.fetchall()
        print(response['atlet_ujian_kualifikasi_soal'])
        return render(request, "atlet_ujian_kualifikasi_soal.html", response)

def atlet_daftar_stadium(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM stadium;
                        """)

        response['atlet_daftar_stadium'] = cursor.fetchall()
        print(response['atlet_daftar_stadium'])
        return render(request, "atlet_daftar_stadium.html", response)

def atlet_daftar_event(request, stadium):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute(f"""
                        SELECT *
                        FROM event
                        WHERE nama_stadium like '{stadium}%';
                        """)

        response['atlet_daftar_event'] = cursor.fetchall()

        pprint(response['atlet_daftar_event'])
        return render(request, "atlet_daftar_event.html", response)

# def atlet_daftar_partai(request, stadium, event):
#     response = {}
#     with connection.cursor() as cursor:
       
#         cursor.execute("""
#                         SELECT *
#                         FROM event
#                         WHERE nama_stadium = %s AND nama_event = %s ;
#                         """, [stadium, event])

#         response['atlet_daftar_partai'] = cursor.fetchall()
#         print(response['atlet_daftar_partai'])
#         return render(request, "atlet_daftar_partai.html", response)

# def atlet_daftar_partai(request, stadium, event):
#     response = {}
#     with connection.cursor() as cursor:
       
#         cursor.execute("""
#                         SELECT e.nama_event, e.total_hadiah, e.tgl_mulai, e.tgl_selesai, e.kategori_superseries, s.kapasitas, e.nama_stadium, e.negara
#                         FROM event as e, stadium as s
#                         WHERE e.nama_stadium = %s AND e.nama_event = %s AND s.nama = e.nama_stadium;
#                         """, [stadium, event])

#         response['atlet_daftar_partai'] = cursor.fetchall()
#         print(response['atlet_daftar_partai'])

#         cursor.execute("""
#                         SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
#                         FROM member as m
#                         join atlet as a on a.id = m.id
#                         join atlet_kualifikasi as ak on a.id = ak.id_atlet
#                         WHERE a.jenis_kelamin = TRUE;
#                         """)

#         response['daftar_atlet_wanita'] = cursor.fetchall()
#         print(response['atlet_daftar_wanita'])

#         cursor.execute("""
#                         SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
#                         FROM member as m
#                         join atlet as a on a.id = m.id
#                         join atlet_kualifikasi as ak on a.id = ak.id_atlet
#                         WHERE a.jenis_kelamin = FALSE;
#                         """)
#         response['daftar_atlet_pria'] = cursor.fetchall()
#         print(response['atlet_daftar_pria'])

#         cursor.execute("""
#                         SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
#                         FROM member as m
#                         join atlet as a on a.id = m.id
#                         join atlet_kualifikasi as ak on a.id = ak.id_atlet
#                         """)

#         response['daftar_atlet_all'] = cursor.fetchall()
#         print(response['atlet_daftar_all'])

#         return render(request, "atlet_daftar_partai.html", response)

def atlet_daftar_partai(request, stadium, event):
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.nama_event, e.total_hadiah, e.tgl_mulai, e.tgl_selesai, e.kategori_superseries, s.kapasitas, e.nama_stadium, e.negara
            FROM event as e, stadium as s
            WHERE e.nama_stadium = %s AND e.nama_event = %s AND s.nama = e.nama_stadium;
        """, [stadium, event])

        response['atlet_daftar_partai'] = cursor.fetchall()
        print(response['atlet_daftar_partai'])

        cursor.execute("""
            SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
            FROM member as m
            JOIN atlet as a on a.id = m.id
            JOIN atlet_kualifikasi as ak on a.id = ak.id_atlet
            WHERE a.jenis_kelamin = TRUE;
        """)

        response['daftar_atlet_wanita'] = cursor.fetchall()
        print(response['daftar_atlet_wanita'])

        cursor.execute("""
            SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
            FROM member as m
            JOIN atlet as a on a.id = m.id
            JOIN atlet_kualifikasi as ak on a.id = ak.id_atlet
            WHERE a.jenis_kelamin = FALSE;
        """)
        response['daftar_atlet_pria'] = cursor.fetchall()
        print(response['daftar_atlet_pria'])

        cursor.execute("""
            SELECT a.id, a.jenis_kelamin, m.nama, ak.id_atlet
            FROM member as m
            JOIN atlet as a on a.id = m.id
            JOIN atlet_kualifikasi as ak on a.id = ak.id_atlet;
        """)

        response['daftar_atlet_all'] = cursor.fetchall()
        print(response['daftar_atlet_all'])

    return render(request, "atlet_daftar_partai.html", response)
