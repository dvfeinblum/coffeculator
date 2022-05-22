.PHONY: local clean

local: clean
	docker compose up -d

run-alembic:
	alembic upgrade head

brew:
	./coffeeculator.py

clean:
	docker stop coffeeculator-postgres-1 || true
	docker rm coffeeculator-postgres-1 || true

db-dump:
	./scripts/db-dump.sh

db-restore:
	pg_restore -h localhost -U postgres -d coffeeculator
