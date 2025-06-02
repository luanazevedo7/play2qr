# -----------------------------------------------------------
# Play2QR - Sistema de Reprodução de Vídeos via QR Code
# Autor: Luan Azevedo
# Versão: Beta
# -----------------------------------------------------------
# Descrição:
# Este programa permite a exibição de vídeos locais através
# da leitura de QR Codes. O app cria um pequeno servidor
# local e gera QR Codes para cada vídeo encontrado na pasta
# "videos". Ao escanear um QR Code, o vídeo correspondente
# é executado em tela cheia com o VLC Player.
# -----------------------------------------------------------

import os
import socket
import subprocess
from flask import Flask
import qrcode

# Inicializa o app Flask que atuará como servidor web
app = Flask(__name__)

# Define os caminhos para as pastas de vídeos e QR Codes
caminho_pasta_videos = os.path.join(os.getcwd(), "videos")
caminho_pasta_qrcodes = os.path.join(os.getcwd(), "qrcodes")

# Garante que as pastas necessárias existam
os.makedirs(caminho_pasta_videos, exist_ok=True)
os.makedirs(caminho_pasta_qrcodes, exist_ok=True)


# -----------------------------------------------------------
# Função que retorna um dicionário com os vídeos disponíveis.
# Exemplo de retorno:
# {'cena1': 'videos/cena1.mp4'}
# -----------------------------------------------------------
def obter_videos_disponiveis():
    dicionario_videos = {}
    for nome_arquivo in os.listdir(caminho_pasta_videos):
        if nome_arquivo.endswith(".mp4"):
            nome_id = os.path.splitext(nome_arquivo)[0]
            caminho_absoluto = os.path.join(caminho_pasta_videos, nome_arquivo)
            dicionario_videos[nome_id] = caminho_absoluto
    return dicionario_videos


# -----------------------------------------------------------
# Função que descobre o IP local da máquina onde o programa
# está sendo executado. Este IP é usado para gerar as URLs
# dos QR Codes.
# -----------------------------------------------------------
def descobrir_ip_local():
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soquete.connect(("8.8.8.8", 80))  # Conecta ao Google DNS
        endereco_ip = soquete.getsockname()[0]
    finally:
        soquete.close()
    return endereco_ip


# -----------------------------------------------------------
# Função responsável por abrir o VLC Media Player em tela cheia
# e executar o vídeo correspondente.
# -----------------------------------------------------------
def executar_video_vlc(caminho_do_video):
    caminho_vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

    subprocess.Popen([
        caminho_vlc,
        "--fullscreen",
        "--play-and-exit",
        caminho_do_video
    ])


# -----------------------------------------------------------
# Rota principal do Flask: acessa http://<IP>:5000/<id>
# e executa o vídeo correspondente ao ID.
# -----------------------------------------------------------
@app.route('/<string:id_video>')
def rota_tocar_video(id_video):
    videos_dict = obter_videos_disponiveis()

    if id_video in videos_dict:
        executar_video_vlc(videos_dict[id_video])
        return f"🎬 Tocando vídeo: {id_video}"
    else:
        return "❌ Vídeo não encontrado.", 404


# -----------------------------------------------------------
# Função que gera QR Codes para todos os vídeos disponíveis
# na pasta "videos". Salva os QR Codes na pasta "qrcodes".
# -----------------------------------------------------------
def gerar_qrcodes_para_videos(ip_local, porta_http):
    videos_encontrados = obter_videos_disponiveis()

    for identificador, caminho_arquivo in videos_encontrados.items():
        url_completa = f"http://{ip_local}:{porta_http}/{identificador}"
        imagem_qr = qrcode.make(url_completa)

        nome_arquivo_qr = f"{identificador}.png"
        caminho_qr = os.path.join(caminho_pasta_qrcodes, nome_arquivo_qr)
        imagem_qr.save(caminho_qr)

        print(f"✅ QR Code salvo: {caminho_qr}")


# -----------------------------------------------------------
# Execução principal do programa. Inicia o servidor,
# gera os QR Codes e exibe as instruções no terminal.
# -----------------------------------------------------------
if __name__ == "__main__":
    ip_servidor = descobrir_ip_local()
    porta_servidor = 5000

    print("📁 Procurando vídeos na pasta...")
    gerar_qrcodes_para_videos(ip_servidor, porta_servidor)

    print(f"\n🚀 Servidor web iniciado em: http://{ip_servidor}:{porta_servidor}")
    print("📲 Aponte seu celular para o QR Code para tocar uma cena\n")

    app.run(host="0.0.0.0", port=porta_servidor)
