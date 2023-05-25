from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
def daftar_atlet(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nama_pelatih = request.session["nama"]
            email_pelatih = request.session["email"]
            cursor.execute(
            f"""
            SELECT ID 
            FROM MEMBER 
            WHERE NAMA = '{nama_pelatih}' AND EMAIL = '{email_pelatih}';
            """
            )
            id_pelatih= cursor.fetchone()[0]
            id_atlet = request.POST.get("id_atlet")

            if id_atlet:
                cursor.execute(
                    f"""
                    INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
                    """
                )
                connection.commit()

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

def latih_atlet(request):
    nama_pelatih = request.session["nama"]
    email_pelatih = request.session["email"]

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT ID 
            FROM MEMBER 
            WHERE NAMA = '{nama_pelatih}' AND EMAIL = '{email_pelatih}';
            """
        )
        id_pelatih= cursor.fetchone()[0]
        cursor.execute(f"""
                            SELECT MA.Nama, MA.Email, A.World_rank
                            FROM MEMBER MA
                            JOIN ATLET A ON MA.ID = A.ID
                            JOIN ATLET_PELATIH AP ON A.ID = AP.ID_Atlet
                            JOIN PELATIH P ON AP.ID_Pelatih = P.ID
                            WHERE p.id= '{id_pelatih};'""")

        daftar_atlet_latih= cursor.fetchall()

        latih_atlet = []

        for res in daftar_atlet_latih:
            atlet = {
                    "nama": res[0],
                    "email": res[1],
                    "world_rank": res[2],
                }
            latih_atlet.append(atlet)

    context = {
        "latih_atlet": latih_atlet
    }
    return render(request, "latih_atlet.html", context)

def dashboard_pelatih(request):
    pelatih_id = request.session["id"]
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT DISTINCT
                            M.Nama,
                            M.Email,
                            P.tanggal_mulai
                        FROM
                            PELATIH P,
                            MEMBER M,
                            PELATIH_SPESIALISASI PS

                        WHERE P.ID = M.ID AND P.ID = %s
                        """, [pelatih_id])

        response['list_dashboard_pelatih'] = cursor.fetchall()
        print(response['list_dashboard_pelatih'])

        cursor.execute("""
                        SELECT DISTINCT
                            S.Spesialisasi
                        FROM
                            PELATIH P,
                            MEMBER M,
                            SPESIALISASI S,
                            PELATIH_SPESIALISASI PS

                        WHERE P.ID = M.ID AND PS.ID_Pelatih = P.ID AND PS.ID_SPESIALISASI = S.ID AND P.ID = %s
                        """, [pelatih_id])
        response['pelatih_spesialisasi'] = cursor.fetchall()
        # print(response['pelatih_spesialisai'])

        merge = []
        for i in response['pelatih_spesialisasi']:
            merge.append(i[0])

        string_sp = ''
        for sp in merge:
            string_sp += " " + sp + ","

        spec = string_sp[1:len(string_sp)-1]

        new_tuple = (spec,)

        response['list_dashboard_pelatih'][0] += new_tuple
        print(response['list_dashboard_pelatih'])

        return render(request, "dashboard_pelatih.html", response)