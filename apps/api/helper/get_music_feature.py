import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_music_feature(playlist_id):
    """get_music_feature
    引数のplaylist_idから曲情報を取得する
    """
    CLIENT_ID = "3b115c1f660943a5afc790dfb626b46e"
    CLIENT_SECRET = "5587992fb25c4247b2801725afbb412f"
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    
    results = sp.playlist(playlist_id)
    items = results['tracks']['items']
    
    tracks_features = []  # ここで初期化
    
    for item in items:
        meta = item['track']
        features = sp.audio_features(meta['id'])[0]  # 特徴量の取得
        
        track_info = {
            'track_id': meta['id'],  # ここでトラックIDを追加
            'name': meta['name'],
            'album': meta['album']['name'],
            'artist': meta['album']['artists'][0]['name'],
            'popularity': meta['popularity'],
            'key': features['key'],
            'mode': features['mode'],
            'danceability': features['danceability'],
            'acousticness': features['acousticness'],
            'energy': features['energy'],
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'loudness': features['loudness'],
            'speechiness': features['speechiness'],
            'tempo': features['tempo'],
            'time_signature': features['time_signature'],
            'valence': features['valence']
        }
        tracks_features.append(track_info)  # 正しくリストに追加
    
    return tracks_features
