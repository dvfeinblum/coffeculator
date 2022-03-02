.PHONY: local clean

local: clean
	docker compose up -d

run-alembic:
	alembic upgrade head

brew:
	./brew.py

clean:
	docker stop coffeeculator-postgres-1 || true
	docker rm coffeeculator-postgres-1 || true
