# Makefile

# Docker Compose のビルドを行うコマンド
build:
	docker-compose build

# Docker Compose のコンテナをビルドして起動するコマンド
up:
	docker-compose up --build

# Docker Compose のコンテナを停止するコマンド
down:
	docker-compose down

# Docker Compose のコンテナをバックグラウンドで起動するコマンド
up-detach:
	docker-compose up --build -d
