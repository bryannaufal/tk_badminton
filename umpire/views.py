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

def umpire_ujian_kualifikasi_buat(request):
    # DB Connection
    cur = connection.cursor()
    context={}
    if request.method == 'POST':
        tahun = request.POST.get('tahun')
        batch = request.POST.get('batch')
        tempat_pelaksanaan = request.POST.get('tempat')
        tanggal_pelaksanaan = request.POST.get('tanggal')

        # Cek
        print(tahun)
        print(batch)
        print(tempat_pelaksanaan)
        print(tanggal_pelaksanaan)
        
        if tahun == "" or batch ==  "" or tempat_pelaksanaan == "" or tanggal_pelaksanaan == None :
            context["error_message"] =  "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu."
            return render(request, "buat_ujian_kualifikasi.html", context)
    
        # SQL Query
        cur.execute(
            """
            INSERT INTO UJIAN_KUALIFIKASI VALUES (%s, %s, %s, CAST(%s AS DATE));
            """,
            [int(tahun), int(batch), tempat_pelaksanaan, tanggal_pelaksanaan]
        )
        return redirect("../umpire_ujian_kualifikasi_list")
        print("berhasil nambahin")

    return render(request, "umpire_ujian_kualifikasi_buat.html")


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
            SELECT M.nama, U.tahun, U.batch, U.tempat, U.tanggal, N.hasil_lulus
            FROM member M, atlet A, ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI N, ujian_kualifikasi U
            WHERE M.id IN (SELECT A.id FROM ATLET) 
            AND N.id_atlet = M.id 
            AND N.tempat = U.tempat
            AND N.batch = U.batch 
            AND N.tempat = U.tempat 
            AND N.tanggal = U.tanggal
            ORDER BY u.tanggal desc;
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


def lihat_hasil_pertandingan(request):
    # nama_event = request.GET.get("nama_event")
    nama_event = "India Open 2022"
    tahun = "2022"
    jenis_partai = 'WD'
    # tahun = request.GET.get("tahun")
    # jenis_partai = request.GET.get("jenis_partai")
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT E.nama_stadium, E.total_hadiah,
                        E.kategori_superseries, E.tgl_mulai, E.Tgl_selesai, S.kapasitas
                        FROM EVENT E, PARTAI_KOMPETISI PK, STADIUM S
                        WHERE E.Nama_event=PK.Nama_event
                        AND E.Tahun=PK.Tahun_event
                        AND E.Nama_stadium=S.Nama
                        AND PK.jenis_partai='{jenis_partai}'
                        AND PK.nama_event='{nama_event}'
                        AND PK.tahun_event='{tahun}';
                        """)
        data_partai = cursor.fetchall()
        partai = {
            'nama_stadium': data_partai[0][0],
            'total_hadiah': data_partai[0][1],
            'kategori_superseries': data_partai[0][2],
            'tgl_mulai': data_partai[0][3],
            'tgl_selesai': data_partai[0][4],
            'kapasitas': data_partai[0][5]
        }
        print(partai)
        if jenis_partai in ['MD', 'XD', 'WD']:
            cursor.execute(f"""SELECT M1.nama AS nama1, M2. nama AS nama2, PM.jenis_babak, PM.status_menang
                        FROM MEMBER M1, MEMBER M2, ATLET_GANDA AG, PESERTA_KOMPETISI PK,
                        MATCH M, PESERTA_MENGIKUTI_MATCH PM
                        WHERE AG.ID_Atlet_Kualifikasi=M1.ID
                        AND AG.ID_Atlet_Kualifikasi_2=M2.ID
                        AND AG.ID_atlet_ganda=PK.ID_atlet_ganda
				        AND PM.nomor_peserta=PK.nomor_peserta
                        AND M.jenis_babak=PM.jenis_babak
                        AND M.tanggal=PM.tanggal
                        AND M.waktu_mulai=PM.waktu_mulai
                        AND M.nama_event='{nama_event}'
                        AND M.tahun_event='{tahun}';
                    """)
            data_peserta = cursor.fetchall()
            print(data_peserta)
            peserta_dict = []
            for row in data_peserta:
                peserta = {
                    'nama1': row[0],
                    'nama2': row[1],
                    'jenis_babak': row[2],
                    'status_menang': row[3],
                }
                peserta_dict.append(peserta)
        else:
            cursor.execute(f"""SELECT ME.nama AS nama1, PM.jenis_babak, PM.status_menang
                        FROM MEMBER ME, PESERTA_KOMPETISI PK,
                        MATCH M, PESERTA_MENGIKUTI_MATCH PM
                        WHERE PM.nomor_peserta=PK.nomor_peserta
                        AND M.jenis_babak=PM.jenis_babak
                        AND M.tanggal=PM.tanggal
                        AND M.waktu_mulai=PM.waktu_mulai
                        AND PK.ID_ATLET_KUALIFIKASI=ME.ID
                        AND (status_menang='false' OR PM.jenis_babak='FINAL')
                        AND M.nama_event='{nama_event}'
                        AND M.tahun_event='{tahun}';
                    """)
            data_peserta = cursor.fetchall()
            peserta_dict = []
            for row in data_peserta:
                peserta = {
                    'nama1': row[0],
                    'nama2': "",
                    'jenis_babak': row[2],
                    'status_menang': row[3],
                }
                peserta_dict.append(peserta)
        juara_1 = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="final" and peserta["status_menang"]==True]
        juara_2 = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="final" and peserta["status_menang"]==False]
        juara_3 = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="juara 3" and peserta["status_menang"]==True]
        semifinal = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="semifinal"]
        quarterfinal = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="quarterfinal"]
        r16 = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="r16"]
        r32 = [peserta for peserta in peserta_dict if peserta["jenis_babak"]=="r32"]
    context = {
        "jenis_partai": jenis_partai,
        "nama_event": nama_event,
        "nama_stadium": partai["nama_stadium"],
        "total_hadiah": partai["total_hadiah"],
        "kategori_superseries": partai["kategori_superseries"],
        "tgl_mulai": partai["tgl_mulai"],
        "tgl_selesai": partai["tgl_selesai"],
        "kapasitas": partai["kapasitas"],
        "juara_1": juara_1,
        "juara_2": juara_2,
        "juara_3": juara_3,
        "semifinal": semifinal,
        "quarterfinal": quarterfinal,
        "r16": r16,
        "r32": r32,
        "jumlah_peserta": len(peserta_dict),
        "partai_ganda": ['MD', 'XD', 'WD'] 
    }
    print(context)
    return render(request, "lihat_hasil_pertandingan.html", context)