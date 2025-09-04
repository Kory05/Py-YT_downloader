from time import sleep

from pytubefix import YouTube
from pytubefix import cli
import os
import shutil
import tempfile
import gestion_archivos


# Directorio inicial
dir_inicio = os.getcwd()
if os.name == "posix":
    dir_descarga = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "Downloads", "Py-YT_Downloads")
elif os.name == "nt":
    dir_descarga = os.path.join(os.environ["USERPROFILE"], "Downloads", "Py-YT_Downloads")
else:
    exit("ERROR: El sistema operativo actual no es compatible con el programa")
dirs = {
    # Diccionario de carpetas que usa el programa
    # Directorio de descarga
    "descarga": dir_descarga,
    # Directorio de gestion de archivos
    "gestion": os.path.join(tempfile.gettempdir(), "pytube", "gestion"),
    # Directorio de ffmpeg
    "ffmpeg": os.path.join(tempfile.gettempdir(), "pytube", "ffmpeg")
}

def limpieza(directory):
    for file in os.listdir(directory["gestion"]):
        arch = os.path.join(directory["gestion"], file)
        try:
            if os.path.isfile(arch):
                os.remove(arch)
        except Exception:
            pass

for name, direc in dirs.items():
    if not os.path.isdir(direc):
        os.makedirs(direc, exist_ok=True)

gestion_archivos.whereffmpeg(dirs["ffmpeg"])
limpieza(dirs)

def is_num(rango_max):
    num = -1
    rango_max += 1
    while num not in range(1, rango_max):
        num = input("Escribe el número de la opción: ")
        try:
            num = int(num)
        except:
            print("ERROR: El valor introducido no es valido")
        if num in range(1, rango_max):
            break
        else:
            print("ERROR: El valor introducido no es valido")
    return num


def info_video(yt):
    print("=" * 25)
    print("\t1. Video 1080p\n\t2. Video 720p\n\t3. Video 480p\n\t4. Todos los Videos")
    print("=" * 25)
    max_num = 4
    op = is_num(max_num)
    if op == 1:
        print(yt.streams.filter(adaptive=True, res="1080p"))
    elif op == 2:
        print(yt.streams.filter(adaptive=True, res="720p"))
    elif op == 3:
        print(yt.streams.filter(adaptive=True, res="480p"))
    elif op == 4:
        print(yt.streams.filter(adaptive=True, type="video"))
    return


def info_audio(yt):
    print("=" * 25)
    print("\t1. Audio 160kbps\n\t2. Audio 128kbps\n\t3. Todos los Audios")
    print("=" * 25)
    max_num = 3
    op = is_num(max_num)
    if op == 1:
        print(yt.streams.filter(adaptive=True, abr="160kbps"))
    elif op == 2:
        print(yt.streams.filter(adaptive=True, abr="128kbps"))
    elif op == 3:
        print(yt.streams.filter(adaptive=True, type="audio"))
    return


# Menu de descarga
def menu(yt):
    itag_video = 0
    itag_audio = 0
    print("=" * 33)
    print("\t1. Video con audio\n\t2. Video sin audio\n\t3. Solo Audio")
    print("=" * 33)
    max_num = 3
    opti_down = is_num(max_num)
    if opti_down == 1:
        info_video(yt)
        itag_video = input("Escribe la itag: ")
        info_audio(yt)
        itag_audio = input("Escribe la itag: ")
    elif opti_down == 2:
        info_video(yt)
        itag_video = input("Escribe la itag: ")
    elif opti_down == 3:
        info_audio(yt)
        itag_video = input("Escribe la itag: ")
    return opti_down, itag_video, itag_audio


# Descarga del video
def download_video_yt(url_yt, download_path):
    try:
        yt = YouTube(url_yt, on_progress_callback=cli.on_progress)
        op_down, itag_video, itag_audio = menu(yt)
        tit_video = gestion_archivos.limpiar_nombre(yt.streams.get_by_itag(itag_video).title)
        if op_down == 1:
            print(f"Descargando Video sin Audio: {tit_video}")
            yt.streams.get_by_itag(itag_video).download(filename=f"{tit_video}.mp4", output_path=download_path)
            print("\nCompleted")
            print(f"Descargando Audio del Video: {tit_video}")
            yt.streams.get_by_itag(itag_audio).download(filename=f"{tit_video}.m4a", output_path=download_path)
            print("\nCompleted")
        elif op_down == 3:
            print(f"Title: {tit_video}")
            yt.streams.get_by_itag(itag_video).download(filename=f"{tit_video}.m4a", output_path=download_path)
            print("\nCompleted")
        else:
            print(f"Title: {tit_video}")
            yt.streams.get_by_itag(itag_video).download(filename=f"{tit_video}.mp4", output_path=download_path)
            print("\nCompleted")
    except Exception as e:
        exit(f"ERROR: {e}")
    return tit_video, op_down


while True:
    print("=" * 33)
    print("\t1. Salir del programa\n\t2. Iniciar programa")
    print("=" * 33)
    max_num = 2
    opt_menu = is_num(max_num)
    if opt_menu == 2:
        url_youtube = input("Pon la URL: ")
        titulo_video, opt_down = download_video_yt(url_youtube, dirs["gestion"])
        os.chdir(dirs["gestion"])
        if opt_down == 1:
            titulo_video = gestion_archivos.export_func(titulo_video, dirs["ffmpeg"])
            titulo_video = f"{gestion_archivos.fusion_func(titulo_video, dirs["ffmpeg"])}.mp4"
            shutil.move(f"{titulo_video}", f"{os.path.join(dir_descarga, titulo_video)}")
        elif opt_down == 2:
            os.rename(fr'{titulo_video}.mp4', fr'{titulo_video} - Sin Audio.mp4')
            titulo_video = f"{titulo_video} - Sin Audio.mp4"
            shutil.move(f"{titulo_video}", f"{os.path.join(dir_descarga, titulo_video)}")
        elif opt_down == 3:
            titulo_video = f"{gestion_archivos.export_func(titulo_video, dirs["ffmpeg"])}.mp3"
            shutil.move(f"{titulo_video}", f"{os.path.join(dir_descarga, titulo_video)}")
        os.chdir(dir_inicio)
        print("Descarga y gestión del archivo completada")
    else:
        print("=" * 33)
        print("Saliendo del programa...")
        sleep(2)
        print("=" * 33)
        print("Programa finalizado")
        sleep(0.5)
        break
