from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# @login_required(login_url='login/')
def begin_page(request):
    return render(request, "begin.html")

def pilih_role(request):
    return render(request, "pilih_role.html")


def register_atlet(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = request.POST.get('jenis_kelamin')

    context = {}
    return render(request, 'register_atlet.html', context)
    # return render(request, "dashboard_atlet.html")
    
def register_pelatih(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        kategori = request.POST.get('kategori')
        tanggal_mulai = request.POST.get('tanggal_mulai')

    context = {}
    return render(request, 'register_pelatih.html', context)

def register_umpire(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')

    context = {}
    return render(request, 'register_umpire.html', context)

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

def login(request):
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


def ujian_kualifikasi_buat(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['ujian_kualifikasi_buat'] = cursor.fetchall()
        print(response['ujian_kualifikasi_buat'])
        return render(request, "ujian_kualifikasi_buat.html", response)

def ujian_kualifikasi_list(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['ujian_kualifikasi_list'] = cursor.fetchall()
        print(response['ujian_kualifikasi_list'])
        return render(request, "ujian_kualifikasi_list.html", response)

def ujian_kualifikasi_riwayat(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['ujian_kualifikasi_riwayat'] = cursor.fetchall()
        print(response['ujian_kualifikasi_riwayat'])
        return render(request, "ujian_kualifikasi_riwayat.html", response)

def ujian_kualifikasi_soal(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['ujian_kualifikasi_soal'] = cursor.fetchall()
        print(response['ujian_kualifikasi_soal'])
        return render(request, "ujian_kualifikasi_soal.html", response)