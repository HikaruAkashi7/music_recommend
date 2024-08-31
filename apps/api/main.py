from fastapi import FastAPI
from apps.api.recommend import router as recommend_router

app = FastAPI()

# 推論ルーターを登録
app.include_router(recommend_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Orangestar Recommendation API!"}
