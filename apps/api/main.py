from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.recommend import router as recommend_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のドメインに限定
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

# 推論ルーターを登録
app.include_router(recommend_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Orangestar Recommendation API!"}
