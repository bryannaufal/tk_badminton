from urllib import response
from uuid import uuid1
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from collections import namedtuple
from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import render
from collections import namedtuple
from django.db import connection
from datetime import datetime as dt

# @login_required(login_url='login/')

def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def begin_page(request):
    return render(request, "begin.html")

def pilih_role(request):
    return render(request, "pilih_role.html")

def register_atlet(request):
    if request.method == 'POST':
        id = uuid1()
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        play = True if play == 'True' else False
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        jenis_kelamin = True if jenis_kelamin == 'True' else False


        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT *
                            FROM member
                            WHERE email ='{email}';
                            """)

            is_email_exist = cursor.fetchall()
            if is_email_exist:
                messages.info(request, 'Email sudah pernah terdaftar!')
            else:
                cursor.execute(f"""INSERT INTO MEMBER VALUES ('{id}', '{nama}', '{email}')""")
                connection.commit()
                cursor.execute(f"INSERT INTO atlet VALUES ('{id}', '{tanggal_lahir}', '{negara}', {play}, '{tinggi_badan}', null,{jenis_kelamin})")
                connection.commit()
                messages.success(request, 'Akun telah berhasil dibuat!')
                return redirect('/atlet')
            print(is_email_exist)

    context = {}
    return render(request, 'register_atlet.html', context)
    # return render(request, "dashboard_atlet.html")
    
def register_pelatih(request):
    if request.method == 'POST':
        id = uuid1()
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        kategori = request.POST.get('kategori')
        tanggal_mulai = request.POST.get('tanggal_mulai')
    
        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT *
                            FROM member
                            WHERE email ='{email}';
                            """)

            is_email_exist = cursor.fetchall()
            if is_email_exist:
                messages.info(request, 'Email sudah pernah terdaftar!')
            else:
                cursor.execute(f"""INSERT INTO member VALUES ('{id}', '{nama}', '{email}')""")
                connection.commit()
                cursor.execute(f"INSERT INTO pelatih VALUES ('{id}', '{tanggal_mulai}')")
                connection.commit()
                messages.success(request, 'Akun telah berhasil dibuat!')
                return redirect('/pelatih')
            print(is_email_exist)

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
    
@csrf_exempt
def login(request):
    with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT member.nama, member.email
                            FROM member, atlet
                            WHERE atlet.id = member.id;
                            """)

            atlet_data = cursor.fetchall()
            cursor.execute("""
                            SELECT member.nama, member.email
                            FROM member, pelatih
                            WHERE pelatih.id = member.id;
                            """)

            pelatih_data = cursor.fetchall()
            cursor.execute("""
                            SELECT member.nama, member.email
                            FROM member, umpire
                            WHERE umpire.id = member.id;
                            """)

            umpire_data = cursor.fetchall()

    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')

        is_valid = False
        role = ""
        for element in atlet_data:
            print(element)
            print(nama)
            print(email)
            if nama == element[0] and email == element[1]:
                is_valid = True
                role = 'atlet'
                request.session['role'] = role
        for element in pelatih_data:
            if nama == element[0] and email == element[1]:
                is_valid = True
                role = 'pelatih'
                request.session['role'] = role
                break
        for element in umpire_data:
            if nama == element[0] and email == element[1]:
                is_valid = True
                role = 'umpire'
                request.session['role'] = role
                break

        if is_valid:
            request.session['nama'] = nama
            request.session['email'] = email
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         f"""
            #         SELECT ID 
            #         FROM MEMBER 
            #         WHERE NAMA = '{nama}' AND EMAIL = '{email}';
            #         """
            #     )
            #     request.session['id'] = cursor.fetchone()[0]
            messages.success(request, f'Anda telah berhasil login sebagai {role} :)')
            return redirect(f'/{role}/dashboard/')
        else:
            messages.info(request, f'Data yang anda masukkan tidak valid :(')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    request.session.clear()
    return redirect("/")
