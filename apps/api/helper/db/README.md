# テーブル情報

```sql
CREATE TABLE tracks_features (
    id SERIAL PRIMARY KEY,                 -- 自動インクリメントの主キー
    track_id VARCHAR(255) UNIQUE NOT NULL, -- トラックID (一意)
    name VARCHAR(255),                     -- 曲名
    album VARCHAR(255),                    -- アルバム名
    artist VARCHAR(255),                   -- アーティスト名
    popularity INTEGER,                    -- 人気度
    key INTEGER,                           -- 曲のキー
    mode INTEGER,                          -- モード（メジャー: 1、マイナー: 0）
    danceability FLOAT,                    -- ダンスしやすさ
    acousticness FLOAT,                    -- アコースティック度
    energy FLOAT,                          -- エネルギー量
    instrumentalness FLOAT,                -- 器楽度
    liveness FLOAT,                        -- ライブ感
    loudness FLOAT,                        -- 音量
    speechiness FLOAT,                     -- スピーチ度
    tempo FLOAT,                           -- テンポ
    time_signature INTEGER,                -- 拍子
    valence FLOAT,                         -- 感情的なポジティブ度
    duration_ms INTEGER,                   -- 曲の長さ（ミリ秒）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 作成日時
);
```