from db.conn import connect_to_db
from get_music_feature import get_music_feature
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_tracks_features_to_db(playlist_id):
    """
    save_tracks_features_to_db
    OrangestarのプレイリストIDを使って曲情報を取得し、データベースに保存する
    """
    # Orangestarの曲情報を取得
    tracks_features = get_music_feature(playlist_id)
    
    # 挿入するデータの件数をログに出力
    logger.info(f"Number of track features to insert: {len(tracks_features)}")

    # データベースに接続
    conn = connect_to_db()
    if conn is None:
        logger.error("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        inserted_count = 0  # 挿入した行数のカウンタ
        
        # 曲情報をデータベースに挿入
        for tracks_feature in tracks_features:
            
            cursor.execute(
                """
                INSERT INTO tracks_features (
                    track_id,
                    name, 
                    album, 
                    artist, 
                    popularity, 
                    key, 
                    mode, 
                    danceability, 
                    acousticness, 
                    energy,
                    instrumentalness, 
                    liveness, 
                    loudness, 
                    speechiness, 
                    tempo, 
                    time_signature, 
                    valence
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                );
                """, (
                    tracks_feature['track_id'], tracks_feature['name'], tracks_feature['album'], tracks_feature['artist'], tracks_feature['popularity'], 
                    tracks_feature['key'], tracks_feature['mode'], tracks_feature['danceability'], tracks_feature['acousticness'], 
                    tracks_feature['energy'], tracks_feature['instrumentalness'], tracks_feature['liveness'], tracks_feature['loudness'], 
                    tracks_feature['speechiness'], tracks_feature['tempo'], tracks_feature['time_signature'], tracks_feature['valence']
                )
            )
            inserted_count += 1

        # 変更をコミット
        conn.commit()
        logger.info(f"Successfully saved {inserted_count} tracks_feature records to the database.")

    except Exception as e:
        logger.error(f"An error occurred while saving to the database: {e}")
        conn.rollback()

    finally:
        conn.close()
        logger.info("Database connection closed.")

# メイン処理
if __name__ == "__main__":
    PLAYLIST_ID = "2wsP7AB3a7WUKvBoRvhesk"  # 使用するプレイリストID
    save_tracks_features_to_db(PLAYLIST_ID)
