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
from django.http import HttpResponse



def fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def dashboard_atlet(request):
    nama = request.session.get("nama")
    email = request.session.get("email")

    query = {}

    with connection.cursor() as cursor:
        # Get member ID
        cursor.execute(
            """
            SELECT id
            FROM MEMBER
            WHERE nama = %s AND email = %s
            """,
            [nama, email]
        )
        member_id = cursor.fetchone()[0]

        # Get athlete details
        cursor.execute(
            """
            SELECT m.nama, negara_asal, email, tgl_lahir, play_right, height, jenis_kelamin, world_rank
            FROM ATLET A
            INNER JOIN MEMBER M ON M.id = A.id
            WHERE A.id = %s
            GROUP BY m.nama, negara_asal, email, tgl_lahir, play_right, height, jenis_kelamin, world_rank;
            """,
            [member_id]
        )
        athlete_data = cursor.fetchone()

        if athlete_data:
            query["nama"] = athlete_data[0]
            query["negara"] = athlete_data[1]
            query["email"] = athlete_data[2]
            query["tgl_lahir"] = athlete_data[3]
            query["play"] = "Right Hand" if athlete_data[4] else "Left Hand"
            query["height"] = athlete_data[5]
            query["jenis_kelamin"] = "Laki-laki" if athlete_data[6] else "Perempuan"
            query["world_rank"] = athlete_data[7] if athlete_data[7] is not None else "-"
            query["status"] = "Qualified" if athlete_data[7] is not None else "Not Qualified"
        else:
            return HttpResponse("Athlete data not found.")

        # Get total points
        cursor.execute(
            """
            SELECT SUM(total_point)
            FROM POINT_HISTORY
            WHERE id_atlet = %s
            """,
            [member_id]
        )
        total_points = cursor.fetchone()[0] or 0
        query["poin"] = total_points

        # Get coach name
        cursor.execute(
            """
            SELECT nama
            FROM MEMBER M
            INNER JOIN ATLET_PELATIH AP ON AP.id_pelatih = M.id
            WHERE AP.id_atlet = %s
            """,
            [member_id]
        )
        coach_name = cursor.fetchone()
        query["pelatih"] = coach_name[0] if coach_name else "-"

    return render(request, "dashboard_atlet.html", query)


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
                            WHERE nama_stadium like '{stadium}%' and tgl_mulai > current_date;
                        """)

        response['atlet_daftar_event'] = cursor.fetchall()

        pprint(response['atlet_daftar_event'])
        return render(request, "atlet_daftar_event.html", response)

def atlet_daftar_partai(request, stadium, event):
    nama = request.session["nama"]
    email = request.session["email"]
    response = {}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id
                FROM MEMBER
                WHERE nama = %s AND email = %s;
        """, [nama, email])

        member_id = cursor.fetchone()[0]
        response['member_id'] = member_id
        print(response['member_id'])

        cursor.execute("""
            SELECT jenis_kelamin
            FROM atlet
            WHERE id = %s;
        """, [member_id])

        atlet_gender = cursor.fetchone()[0]
        response['atlet_gender'] = atlet_gender

        cursor.execute("""
            SELECT
                e.nama_event, e.total_hadiah, e.tgl_mulai, e.tgl_selesai, e.kategori_superseries, s.kapasitas / 5, e.nama_stadium, e.negara,
                COUNT(CASE WHEN pp.jenis_partai = 'WD' THEN 1 END) AS jumlah_peserta_WD,
                COUNT(CASE WHEN pp.jenis_partai = 'WS' THEN 1 END) AS jumlah_peserta_WS,
                COUNT(CASE WHEN pp.jenis_partai = 'MD' THEN 1 END) AS jumlah_peserta_MD,
                COUNT(CASE WHEN pp.jenis_partai = 'MS' THEN 1 END) AS jumlah_peserta_MS,
                COUNT(CASE WHEN pp.jenis_partai = 'XD' THEN 1 END) AS jumlah_peserta_WD
                FROM event e
                INNER JOIN stadium s ON e.nama_stadium = s.nama
                INNER JOIN partai_peserta_kompetisi pp ON e.nama_event = pp.nama_event AND e.tahun = pp.tahun_event
                WHERE e.nama_stadium = %s AND e.nama_event = %s
                GROUP BY e.nama_event, e.total_hadiah, e.tgl_mulai, e.tgl_selesai, e.kategori_superseries, s.kapasitas, e.nama_stadium, e.negara;
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
