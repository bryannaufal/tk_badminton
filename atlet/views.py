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

    cur = connection.cursor()
   
    # # Sessions
    # nama = request.session['nama']
    # email = request.session['email']
    # role = request.session['role'] 
    # batch = request.session['batch']
    # tempat_pelaksanaan = request.session['tempat_pelaksanaan']
    # tanggal_pelaksanaan = request.session['tanggal_pelaksanaan']

    # cur.execute(""" SELECT id FROM MEMBER WHERE nama = %s AND email = %s; """, [nama, email])
    # id_atlet = cur.fetchone()[0] 

    # print(id_atlet)
    # print(batch)
    # print(tempat_pelaksanaan)
    # print(tanggal_pelaksanaan)

    if request.method == 'POST':
      
        option_1 = request.POST.get('1', '')
        option_2 = request.POST.get('2', '')
        option_3 = request.POST.get('3', '')
        option_4 = request.POST.get('4', '')
        option_5 = request.POST.get('5', '')

        score = 0
        if option_1 == 'benar':
            score += 1
        if option_2 == 'benar':
            score += 1
        if option_3 == 'benar':
            score += 1
        if option_4 == 'benar':
            score += 1
        if option_5 == 'benar':
            score += 1

        cur.execute(""" SELECT id FROM MEMBER WHERE nama = %s AND email = %s; """, [nama, email])
        id_atlet = cur.fetchone()[0] 

        if score >= 4:
            print("Anda Lulus")
        else:
            print("Anda Tidak Lulus")
        print(score)
        return redirect('/atlet_ujian_kualifikasi_riwayat')
    return render(request, "atlet_ujian_kualifikasi_soal.html")

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
        print(response['atlet_gender'])
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
            SELECT
                A.ID AS ID_Atlet,
                A.Jenis_Kelamin,
                M.Nama AS Nama_Atlet,
                AK.ID_Atlet AS ID_Atlet_Kualifikasi
            FROM
                ATLET A
                INNER JOIN MEMBER M ON A.ID = M.ID
                LEFT JOIN ATLET_GANDA AG ON A.ID = AG.ID_Atlet_Kualifikasi OR A.ID = AG.ID_Atlet_Kualifikasi_2
                LEFT JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet
            WHERE
                AG.ID_Atlet_Ganda IS NULL AND a.jenis_kelamin = FALSE;
        """)

        response['daftar_atlet_wanita'] = cursor.fetchall()
        print(response['daftar_atlet_wanita'])

        cursor.execute("""
            SELECT
                A.ID AS ID_Atlet,
                A.Jenis_Kelamin,
                M.Nama AS Nama_Atlet,
                AK.ID_Atlet AS ID_Atlet_Kualifikasi
            FROM
                ATLET A
                INNER JOIN MEMBER M ON A.ID = M.ID
                LEFT JOIN ATLET_GANDA AG ON A.ID = AG.ID_Atlet_Kualifikasi OR A.ID = AG.ID_Atlet_Kualifikasi_2
                LEFT JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet
            WHERE
                AG.ID_Atlet_Ganda IS NULL AND a.jenis_kelamin = TRUE;
        """)
        response['daftar_atlet_pria'] = cursor.fetchall()
        print(response['daftar_atlet_pria'])

        cursor.execute("""
            SELECT
                A.ID AS ID_Atlet,
                A.Jenis_Kelamin,
                M.Nama AS Nama_Atlet,
                AK.ID_Atlet AS ID_Atlet_Kualifikasi
            FROM
                ATLET A
                INNER JOIN MEMBER M ON A.ID = M.ID
                LEFT JOIN ATLET_GANDA AG ON A.ID = AG.ID_Atlet_Kualifikasi OR A.ID = AG.ID_Atlet_Kualifikasi_2
                LEFT JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet
            WHERE
                AG.ID_Atlet_Ganda IS NULL;
        """)

        response['daftar_atlet_all'] = cursor.fetchall()
        print(response['daftar_atlet_all'])

    return render(request, "atlet_daftar_partai.html", response)

def dashboard_atlet(request):
    nama = request.session["nama"]
    email = request.session["email"]

    response = {}

    with connection.cursor() as cursor:
        # Get member ID
        cursor.execute("""
            SELECT id
                FROM MEMBER
                WHERE nama = %s AND email = %s;
        """, [nama, email])
        member_id = cursor.fetchone()[0]
        response['member_id'] = member_id
        print(response['member_id'])

        # Get athlete details
        cursor.execute(
            """
            SELECT M.Nama, A.Negara_Asal, M.Email, A.Tgl_Lahir, A.Play_Right, A.Height, A.Jenis_Kelamin, A.World_Rank
            FROM MEMBER M
            JOIN ATLET A ON M.ID = A.ID AND M.ID = %s;
            """,
            [member_id]
        )
        athlete_data = cursor.fetchone()
        response['athlete_data'] = athlete_data
        print(response['athlete_data'])

        if athlete_data:
            response.update({
                "nama": athlete_data[0],
                "negara": athlete_data[1],
                "email": athlete_data[2],
                "tgl_lahir": athlete_data[3],
                "play": "Right Hand" if athlete_data[4] else "Left Hand",
                "height": athlete_data[5],
                "jenis_kelamin": "Laki-laki" if athlete_data[6] else "Perempuan",
                "world_rank": str(athlete_data[7]) if athlete_data[7] is not None else "-",
                "status": "Qualified" if athlete_data[7] is not None else "Not Qualified"
            })
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
        response["total_points"] = total_points
        print(response['total_points'])

        # Get coach name
        cursor.execute(
            """
            SELECT nama
            FROM MEMBER M
            JOIN ATLET_PELATIH AP ON AP.id_pelatih = M.id
            WHERE AP.id_atlet = %s
            """,
            [member_id]
        )
        coach_name = cursor.fetchone()
        response["pelatih"] = coach_name[0] if coach_name else "-"
        print(response['pelatih'])

    return render(request, "atlet_dashboard.html", response)

def daftar_sponsor(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM sponsor;
                        """)

        response['daftar_sponsor'] = cursor.fetchall()
        print(response['daftar_sponsor'])
        # sql = "INSERT INTO ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai) VALUES (%s,%s,%s,%s)"
        # cursor.execute(sql, (str(id_atlet), str(id_sponsor), tgl_mulai, tgl_selesai))
        return render(request, "daftar_sponsor.html", response)
    
def list_sponsor(request):
    response = {}
    with connection.cursor() as cursor:
       
        cursor.execute("""
                        SELECT *
                        FROM atlet_sponsor
                        INNER JOIN sponsor
                        ON atlet_sponsor.ID_Sponsor=sponsor.ID;
                        """)

        response['list_sponsor'] = cursor.fetchall()
        print(response['list_sponsor'])

        return render(request, "list_sponsor.html", response)    
