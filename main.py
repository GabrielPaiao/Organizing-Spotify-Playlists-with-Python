'''ordenando playlists pela ordem de lançamento das músicas
código por: Gabriel Pereira Paião'''
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Função para obter entradas seguras do usuário
def get_input(prompt):
    return input(prompt)

# Solicitar entradas do usuário
client_id = get_input("Digite seu client_id do Spotify: ")
client_secret = get_input("Digite seu client_secret do Spotify: ")
redirect_uri = get_input("Digite seu redirect_uri: ")
playlist_id = get_input("Digite o ID da playlist que deseja organizar: ")

# Configure o Spotipy com as credenciais fornecidas
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope='playlist-modify-public playlist-read-private'
))

# Obtenha o ID do usuário
def get_user_id():
    user_info = sp.current_user()
    return user_info['id']

user_id = get_user_id()
print(f"Seu ID de usuário do Spotify é: {user_id}")

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def organize_playlist_by_release_date(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    
    # Filtrar apenas os itens que têm a chave 'track'
    valid_tracks = [t for t in tracks if t['track'] is not None]
    
    # Ordenar pelas informações da data de lançamento do álbum
    tracks_sorted = sorted(valid_tracks, key=lambda t: t['track']['album']['release_date'])
    
    # Criar uma nova playlist
    new_playlist = sp.user_playlist_create(user=user_id, name='Organizada por Data de Lançamento')
    new_playlist_id = new_playlist['id']
    
    # Adicionar as faixas organizadas à nova playlist em blocos de no máximo 100 faixas
    track_ids = [t['track']['id'] for t in tracks_sorted if t['track']['id'] is not None]
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(new_playlist_id, track_ids[i:i+100])
    print(f"Playlist organizada criada com ID: {new_playlist_id}")

# Organizar a playlist pelo ID fornecido
organize_playlist_by_release_date(playlist_id)
