from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt


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

def umpire_ujian_kualifikasi_buat(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['umpire_ujian_kualifikasi_buat'] = cursor.fetchall()
        print(response['umpire_ujian_kualifikasi_buat'])
        return render(request, "umpire_ujian_kualifikasi_buat.html", response)

def umpire_ujian_kualifikasi_list(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['umpire_ujian_kualifikasi_list'] = cursor.fetchall()
        print(response['umpire_ujian_kualifikasi_list'])
        return render(request, "umpire_ujian_kualifikasi_list.html", response)

def umpire_ujian_kualifikasi_riwayat(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM ujian_kualifikasi;
                        """)

        response['umpire_ujian_kualifikasi_riwayat'] = cursor.fetchall()
        print(response['umpire_ujian_kualifikasi_riwayat'])
        return render(request, "umpire_ujian_kualifikasi_riwayat.html", response)

def lihat_daftar_atlet(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT M.nama, A.tgl_lahir, A.negara_asal, A.play_right, A.height, AK.world_rank, AK.world_tour_rank, A.jenis_kelamin, P.total_point
                        FROM MEMBER M, ATLET A, ATLET_KUALIFIKASI AK, POINT_HISTORY P
                        WHERE M.ID=A.ID AND A.ID=AK.ID_atlet
                        AND A.ID=P.ID_atlet
                        AND total_point IN (
                            SELECT total_point FROM POINT_HISTORY
                            WHERE ID_atlet=P.ID_atlet
                            ORDER BY (Tahun, Bulan, Minggu_ke) LIMIT 1
                        );""")
        atlet_kuali = cursor.fetchall()
        atlet_kuali_dict = []
        for row in atlet_kuali:
            atlet_dict = {
                'nama': row[0],
                'tgl_lahir': row[1],
                'negara_asal': row[2],
                'play_right': row[3],
                'height': row[4],
                'world_rank': row[5],
                'world_tour_rank': row[6],
                'jenis_kelamin': row[7],
                'total_point': row[8]
            }
            atlet_kuali_dict.append(atlet_dict)

        cursor.execute(f"""
            SELECT DISTINCT M.nama, A.tgl_lahir, A.negara_asal, A.play_right, A.height, A.jenis_kelamin
            FROM MEMBER M, ATLET A, ATLET_NON_KUALIFIKASI AN
            WHERE M.ID=A.ID AND A.ID=AN.ID_atlet;
        """)
        atlet_nonkuali = cursor.fetchall()

        atlet_nonkuali_dict = []
        for row in atlet_nonkuali:
            atlet_dict = {
                'nama': row[0],
                'tgl_lahir': row[1],
                'negara_asal': row[2],
                'play_right': row[3],
                'height': row[4],
                'jenis_kelamin': row[5]
            }
            atlet_nonkuali_dict.append(atlet_dict)

        cursor.execute(f"""
            SELECT AG.ID_Atlet_Ganda, MA.Nama AS nama_atlet_1, MB.Nama AS nama_atlet_2, SUM(PHA.total_point + PHB.total_point) AS total_point
            FROM ATLET_GANDA AG
            JOIN MEMBER MA ON AG.ID_Atlet_kualifikasi = MA.ID
            JOIN MEMBER MB ON AG.ID_Atlet_kualifikasi_2 = MB.ID
            LEFT JOIN POINT_HISTORY PHA ON PHA.ID_Atlet = AG.ID_Atlet_kualifikasi
            LEFT JOIN POINT_HISTORY PHB ON PHB.ID_Atlet = AG.ID_Atlet_kualifikasi_2
            GROUP BY AG.ID_Atlet_Ganda, MA.Nama, MB.Nama;
                    """)
        atlet_ganda = cursor.fetchall()

        # pprint(atlet_ganda_raw)
        atlet_ganda_dict = []
        for row in atlet_ganda:
            atlet_dict = {
                'ID_Atlet_Ganda': row[0],
                'nama_atlet_1': row[1],
                'nama_atlet_2': row[2],
                'total_point': row[3]
            }
            atlet_ganda_dict.append(atlet_dict)

    context = {
        "atlet_kuali_dict": atlet_kuali_dict,
        "atlet_nonkuali_dict": atlet_nonkuali_dict,
        "atlet_ganda_dict": atlet_ganda_dict
    }

    return render(request, "lihat_daftar_atlet.html", context)

def lihat_partai_kompetisi(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
                        E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
                        FROM EVENT E, PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, STADIUM S
                        WHERE E.Nama_event=PK.Nama_event
                        AND E.Tahun=PK.Tahun_event
                        AND PK.Nama_event=PPK.Nama_event
                        AND PK.Tahun_event=PPK.Tahun_event
                        AND PK.Jenis_partai=PPK.Jenis_partai
                        AND E.Nama_stadium=S.Nama
                        GROUP BY E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
                        E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, S.Kapasitas;
                    """)
        partai_kompetisi = cursor.fetchall()
        partai_kompetisi_dict = []
        for row in partai_kompetisi:
            partai = {
                'Nama_event': row[0],
                'Tahun': row[1],
                'Nama_stadium': row[2],
                'Jenis_partai': row[3],
                'Kategori_Superseries': row[4],
                'Tgl_mulai': row[5],
                'Tgl_selesai': row[6],
                'jumlah_peserta': row[7],
                'Kapasitas': row[8]
            }
            partai_kompetisi_dict.append(partai)
        context = {
            "partai_kompetisi": partai_kompetisi_dict
        }
    return render(request, "lihat_partai_kompetisi.html", context)

@csrf_exempt
def perempat(request):
    pertandingan = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    context = {
        'pertandingan': pertandingan,
        'score': [[0,0], [0,0], [0,0], [0,0]]
    }

    if request.method == 'POST':
        score = [request.POST.get('score-1'), request.POST.get('score-2'), request.POST.get('score-3'), request.POST.get('score-4'),
                request.POST.get('score-5'), request.POST.get('score-6'), request.POST.get('score-7'), request.POST.get('score-8'), ]
        
        print(score)
        tanggal = date.today()
        waktu = datetime.now().strftime("%H:%M:%S")

        if score[1] > score[2]:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[1]}', '1');")
        else :
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[2]}', '1');")

        if score[3] > score[4]:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[3]}', '1');")
        else :
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[4]}', '1');")

        if score[5] > score[6]:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[5]}', '1');")
        else :
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[6]}', '1');")

        if score[7] > score[8]:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[7]}', '1');")
        else :
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO PESERTA_MENGIKUTI_MATCH VALUES ('Perempat final', '{tanggal}', '{waktu}', '{pertandingan[8]}', '1');")

        return render(request, "pertandingan-semifinal.html", context)
    return render(request, "pertandingan-perempat.html", context)