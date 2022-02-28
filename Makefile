local:
	docker compose up -d

run-alembic:
	alembic upgrade head

brew:
	./brew.py
