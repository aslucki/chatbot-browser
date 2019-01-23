IMAGE_NAME=chatbot
PORT=8000

build:
	docker build -t $(IMAGE_NAME) .

start_app:
	docker run --rm -ti -p $(PORT):$(PORT) $(IMAGE_NAME) \
		   gunicorn -b 0.0.0.0:$(PORT) web:app

dev:
	docker run --rm -ti -p $(PORT):$(PORT) \
	       -v $(PWD)/app:/app $(IMAGE_NAME) \
		   gunicorn -b 0.0.0.0:$(PORT) web:app