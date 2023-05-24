from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
       
        cursor.execute("""
                        SELECT *
                        FROM event
                        WHERE nama_stadium = %s;
                        """, [stadium])

        response['atlet_daftar_event'] = cursor.fetchall()
        print(response['atlet_daftar_event'])
        return render(request, "atlet_daftar_event.html", response)

def atlet_daftar_partai(request, stadium, event):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM event
                        WHERE nama_stadium = %s AND nama_event = %s ;
                        """, [stadium, event])

        response['atlet_daftar_partai'] = cursor.fetchall()
        print(response['atlet_daftar_partai'])
        return render(request, "atlet_daftar_partai.html", response)