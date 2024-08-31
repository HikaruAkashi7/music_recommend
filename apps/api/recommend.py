from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.api.helper.db.conn import connect_to_db
import logging
from numpy import dot
from numpy.linalg import norm
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import math

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ユーザーの回答を受け取るためのモデル
class UserResponse(BaseModel):
    danceability: str
    acousticness: str
    energy: str
    instrumentalness: str
    liveness: str
    loudness: str
    speechiness: str
    tempo: str
    time_signature: str
    valence: str

@router.post("/recommend")
def recommend_song(response: UserResponse):
    """
    recommend_song
    ユーザーの回答に基づいて推奨する曲を返す
    """
    # データベースに接続
    conn, cursor = connect_to_db()
    if conn is None or cursor is None:
        raise HTTPException(status_code=500, detail="Failed to connect to the database.")
    
    try:
        # データベースから曲の特徴量を取得
        tracks_features = fetch_tracks_features(cursor)

        # ユーザーの回答
        user_response = {
            'danceability': response.danceability,
            'acousticness': response.acousticness,
            'energy': response.energy,
            'instrumentalness': response.instrumentalness,
            'liveness': response.liveness,
            'loudness': response.loudness,
            'speechiness': response.speechiness,
            'tempo': response.tempo,
            'time_signature': response.time_signature,
            'valence': response.valence
        }

        # 推論結果
        recommendation = infer_recommendation(tracks_features, user_response)
        
        # NaNやInfinityをチェックして除去
        recommendation = sanitize_recommendation(recommendation)

        # 推論結果のデバッグ
        logger.info(f"Recommended track details: {recommendation}")

        return {"recommended_track": recommendation}

    except Exception as e:
        logger.error(f"An error occurred during inference: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during inference.")

    finally:
        cursor.close()
        conn.close()
        logger.info("Database connection closed.")

def fetch_tracks_features(cursor):
    """
    fetch_tracks_features
    データベースから曲の特徴量を取得する
    """
    cursor.execute("""
    SELECT 
        track_id, name, album, artist, popularity, key, mode, 
        danceability, acousticness, energy, instrumentalness, 
        liveness, loudness, speechiness, tempo, time_signature, 
        valence, duration_ms
    FROM tracks_features;
    """)
    tracks = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    return [dict(zip(colnames, track)) for track in tracks]

def infer_recommendation(tracks_features, user_response):
    """
    infer_recommendation
    曲の特徴量に基づき、ユーザーの回答に合う曲を推論しておすすめする。
    
    Args:
        tracks_features (list of dict): 曲の特徴量のリスト。
        user_response (dict): ユーザーの回答。
    
    Returns:
        dict: 推奨する曲の情報。
    """
    # ユーザーの回答に基づく重み設定
    weights = {
        'はい': 1,
        'どちらかといえばはい': 0.5,
        'どちらともいえない': 0,
        'どちらかといえばいいえ': -0.5,
        'いいえ': -1
    }
    
    # ユーザーの回答をスコアリングに変換
    user_preference = {feature: weights[user_response[feature]] for feature in user_response}

    # 特徴量のスケーリングと欠損値の補完
    imputer = SimpleImputer(strategy='constant', fill_value=0)  # 欠損値を0で補完
    scaler = MinMaxScaler()
    features_array = [
        [
            track['popularity'], track['key'], track['mode'], track['danceability'], track['acousticness'], 
            track['energy'], track['instrumentalness'], track['liveness'], track['loudness'], track['speechiness'], 
            track['tempo'], track['time_signature'], track['valence'], track['duration_ms'] if track['duration_ms'] else 0
        ]
        for track in tracks_features
    ]
    
    # 補完とスケーリング
    features_array = imputer.fit_transform(features_array)
    scaled_features = scaler.fit_transform(features_array)

    # ユーザーの回答も同様に特徴量の次元を調整
    preference_values = np.array(list(user_preference.values()) + [0] * (len(scaled_features[0]) - len(user_preference)))

    # 各曲のスコアを計算（コサイン類似度計算）
    for i, track in enumerate(tracks_features):
        track_features = scaled_features[i]
        track['score'] = calculate_cosine_similarity(track_features, preference_values)
        # スコア計算のデバッグログ
        logger.info(f"Track: {track['name']}, Score: {track['score']}")

    # スコアが最も高い曲を選択
    best_match = max(tracks_features, key=lambda x: x['score'])

    return best_match

def calculate_cosine_similarity(track_features, preference_values):
    """
    calculate_cosine_similarity
    ユーザーの好みと曲の特徴量の間のコサイン類似度を計算する。
    
    Args:
        track_features (list): 曲の特徴量。
        preference_values (list): ユーザーの好みの特徴量。
    
    Returns:
        float: コサイン類似度スコア。
    """
    # コサイン類似度の計算
    cos_sim = dot(track_features, preference_values) / (norm(track_features) * norm(preference_values))
    # NaNやInfinityが発生した場合に備えてチェック
    if math.isnan(cos_sim) or math.isinf(cos_sim):
        return 0.0
    return cos_sim

def sanitize_recommendation(recommendation):
    """
    sanitize_recommendation
    推論結果からNaNやInfinityを除去する。
    
    Args:
        recommendation (dict): 推奨される曲の情報。
    
    Returns:
        dict: 修正された推奨曲情報。
    """
    sanitized = {}
    for key, value in recommendation.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            sanitized[key] = 0.0  # NaNやInfinityを0に置き換え
        else:
            sanitized[key] = value
    return sanitized
