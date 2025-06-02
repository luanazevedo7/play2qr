import os
import socket
import subprocess
from flask import Flask
import qrcode

# Inicializa o app Flask
app = Flask(__name__)

# Caminhos das pastas
caminho_pasta_videos = os.path.join(os.getcwd(), "videos")
caminho_pasta_qrcodes = os.path.join(os.getcwd(), "qrcodes")

# Cria pastas se não existirem
os.makedirs(caminho_pasta_videos, exist_ok=True)
os.makedirs(caminho_pasta_qrcodes, exist_ok=True)


# -------------------------------------
# Retorna um dicionário com os vídeos da pasta
# Ex: {'cena1': 'videos/cena1.mp4'}
# -------------------------------------
def obter_videos_disponiveis():
    dicionario_videos = {}
    for nome_arquivo in os.listdir(caminho_pasta_videos):
        if nome_arquivo.endswith(".mp4"):
            nome_id = os.path.splitext(nome_arquivo)[0]
            caminho_absoluto = os.path.join(caminho_pasta_videos, nome_arquivo)
            dicionario_videos[nome_id] = caminho_absoluto
    return dicionario_videos


# -------------------------------------
# Obtém o IP local da máquina (ex: 192.168.0.100)
# -------------------------------------
def descobrir_ip_local():
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soquete.connect(("8.8.8.8", 80))
        endereco_ip = soquete.getsockname()[0]
    finally:
        soquete.close()
    return endereco_ip


# -------------------------------------
# Executa o VLC para tocar um vídeo
# -------------------------------------
def executar_video_vlc(caminho_do_video):
    caminho_vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

    subprocess.Popen([
        caminho_vlc,
        "--fullscreen",
        "--play-and-exit",
        caminho_do_video
    ])


# -------------------------------------
# Rota do Flask que toca o vídeo correspondente
# -------------------------------------
@app.route('/<string:id_video>')
def rota_tocar_video(id_video):
    videos_dict = obter_videos_disponiveis()

    if id_video in videos_dict:
        executar_video_vlc(videos_dict[id_video])
        return f"🎬 Tocando vídeo: {id_video}"
    else:
        return "❌ Vídeo não encontrado.", 404


# -------------------------------------
# Gera QR Codes para os vídeos encontrados
# -------------------------------------
def gerar_qrcodes_para_videos(ip_local, porta_http):
    videos_encontrados = obter_videos_disponiveis()

    for identificador, caminho_arquivo in videos_encontrados.items():
        url_completa = f"http://{ip_local}:{porta_http}/{identificador}"
        imagem_qr = qrcode.make(url_completa)

        nome_arquivo_qr = f"{identificador}.png"
        caminho_qr = os.path.join(caminho_pasta_qrcodes, nome_arquivo_qr)
        imagem_qr.save(caminho_qr)

        print(f"✅ QR Code salvo: {caminho_qr}")


# -------------------------------------
# Programa principal
# -------------------------------------
if __name__ == "__main__":
    ip_servidor = descobrir_ip_local()
    porta_servidor = 5000

    print("📁 Procurando vídeos na pasta...")
    gerar_qrcodes_para_videos(ip_servidor, porta_servidor)

    print(f"\n🚀 Servidor web iniciado em: http://{ip_servidor}:{porta_servidor}")
    print("📲 Aponte seu celular para o QR Code para tocar uma cena\n")

    app.run(host="0.0.0.0", port=porta_servidor)