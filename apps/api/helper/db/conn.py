import psycopg2
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# データベース接続情報
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def connect_to_db():
    """connect_to_db
    dbに接続する共通メソッド
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()  # カーソルを作成
        logger.info("DB connection is successful.")
        return conn, cursor  # 接続とカーソルの両方を返す
    except Exception as e:
        logger.error(f"DB connection failed: {e}")
        return None, None

if __name__ == "__main__":
    conn, cursor = connect_to_db()
    if conn and cursor:
        logger.info("Connection to the database was successful.")
        cursor.close()
        conn.close()
    else:
        logger.error("Failed to connect to the database.")
