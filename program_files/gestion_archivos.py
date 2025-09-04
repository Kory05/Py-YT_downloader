import os
import re
import sys
import requests
import zipfile


FFMPEG_DICC = {
    "windows": ("https://drive.usercontent.google.com/download?id=18kAjlgPn2p9WQSEYwnFK-p1KFEnS1cMM&export=download&authuser=0&confirm=t&uuid=5ee14b6b-ea5e-4d66-99de-ad9d5c02a28b&at=AEz70l6gfCotKc16NkTe8r6Xllkv:1742352008688","ffmpeg-n7.1-latest-win64-lgpl-7.1.zip"),
    "darwin": ("https://evermeet.cx/ffmpeg/ffmpeg-7.1.1.zip","ffmpeg-7.1.1.zip")
    #TODO insertar url del ffmpeg de Linux
}

# Descarga de ffmpeg
def down_ffmpeg(os_name, dir_ffmpeg):
    os.chdir(dir_ffmpeg)
    # Comprobacion de OS
    if os_name not in FFMPEG_DICC:
        exit(f"El sistema operativo '{os_name}' no es compatible con el programa.")
    url, nombre_archivo = FFMPEG_DICC[os_name]
    # Descarga de ffmpeg
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(nombre_archivo, 'wb') as archivo:
            for chunk in response.iter_content(1024):
                if chunk:
                    archivo.write(chunk)
    except requests.exceptions.RequestException as e:
        print("ERROR:", e)
    # Descompresión de ffmpeg
    with zipfile.ZipFile(nombre_archivo, 'r') as zip_ref:
        zip_ref.extractall('.')
    if os.name == "posix":
        os.chmod(fr"{dir_ffmpeg}/ffmpeg", 0o755)
    os.remove(nombre_archivo)
    return


# Búsqueda de ffmpeg
def whereffmpeg(direc_ffmpeg):
    if os.name == 'posix':
        nombre_os = sys.platform
        nombre_os = nombre_os.lower()
        if os.path.isfile(fr"{direc_ffmpeg}/ffmpeg"):
            print("Ffmpeg esta descargado, continuando con la ejecución del programa")
        else:
            print("Ffmpeg no esta descargado, procediendo con la descarga")
            down_ffmpeg(nombre_os, direc_ffmpeg)
            print("Ffmpeg descargado, procediendo con el programa")
    elif os.name == 'nt':
        nombre_os = "windows"
        if os.path.isfile(fr"{direc_ffmpeg}\ffmpeg.exe"):
            print("Ffmpeg esta descargado, continuando con la ejecución del programa")
        else:
            print("Ffmpeg no esta descargado, procediendo con la descarga")
            down_ffmpeg(nombre_os, direc_ffmpeg)
            print("Ffmpeg descargado, procediendo con el programa")
    return


# Limpiar nombre del título
def limpiar_nombre(v_title):
    # Eliminar caracteres inválidos
    v_title = re.sub(r'[<>:"/\\|?*#]', "", v_title)
    # Reemplazar espacios múltiples por un solo espacio
    v_title = re.sub(r'\s+', " ", v_title)
    v_title = v_title.strip()
    return v_title


# Exportar audio m4a -> mp3
def export_func(v_title, direc_ffmpeg):
    if os.name == 'posix':
        file_ffmpeg = os.path.join(direc_ffmpeg, "ffmpeg")
        basura = "/dev/null"
    elif os.name == 'nt':
        file_ffmpeg = os.path.join(direc_ffmpeg, "ffmpeg.exe")
        basura = "NUL"
    os.rename(f"{v_title}.m4a", "audio.m4a")
    export = f'{file_ffmpeg} -i audio.m4a -q:a 0 audio.mp3 > {basura} 2>&1'
    print("Gestionando...")
    os.system(export)
    os.rename("audio.mp3", f"{v_title}.mp3")
    try:
        os.remove("audio.m4a")
    except OSError as e:
        print(f"Advertencia: no se pudo eliminar {v_title}: {e}")
    return v_title


# Fusion de audio y video
def fusion_func(v_title, direc_ffmpeg):
    if os.name == 'posix':
        direc_ffmpeg = fr"{direc_ffmpeg}/ffmpeg"
        basura = "/dev/null"
    elif os.name == 'nt':
        direc_ffmpeg = fr"{direc_ffmpeg}\ffmpeg.exe"
        basura = "NUL"
    os.rename(f"{v_title}.mp4", "video.mp4")
    os.rename(f"{v_title}.mp3", "audio.mp3")
    fusion = f'"{direc_ffmpeg}" -i video.mp4 -i audio.mp3 -c:v copy -c:a copy pru.mp4 > {basura} 2>&1'
    print("Gestionando...")
    os.system(fusion)
    os.rename("pru.mp4", f"{v_title}.mp4")
    os.remove("audio.mp3")
    os.remove("video.mp4")
    return v_title
