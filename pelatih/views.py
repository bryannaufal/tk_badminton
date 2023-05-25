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

def daftar_atlet(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            id_pelatih = request.session["id"]
            id_atlet = request.POST.get("id_atlet")

            if id_atlet:
                cursor.execute(
                    f"""
                    INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                    """
                )

                return redirect("/pelatih/list_atlet")

        cursor.execute(
            f"""
            SELECT M.Nama, M.id FROM MEMBER M, ATLET A WHERE M.ID=A.ID ORDER BY M.nama;
            """
        )

        result = cursor.fetchall()

        daftar_atlet = []

        for res in result:
            atlet ={
                    "nama_atlet": res[0],
                    "id_atlet": res[1]
                }
            daftar_atlet.append(atlet)

        context = {
            "daftar_atlet": daftar_atlet
        }
        print(context)

        return render(request, 'daftar_atlet.html', context)

def list_atlet(request):
    print("hello")