#!/bin/bash
set -e

PGPORT=${PGPORT:-5432}
export PGPORT

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Инициализация базы данных..."

  # Запускаем стандартную инициализацию
  gosu postgres /usr/local/bin/docker-entrypoint.sh postgres &

  # Ждем запуска сервера
  until gosu postgres pg_isready -h localhost -p $PGPORT; do
    echo "Ожидание запуска PostgreSQL..."
    sleep 2
  done

  export PGPASSWORD="$POSTGRES_PASSWORD"

  # Создаем базы данных с явным указанием хоста и порта
  gosu postgres psql -U "$POSTGRES_USER" -h localhost -p $PGPORT -c "CREATE DATABASE \"${DBNAME}\";"
  gosu postgres psql -U "$POSTGRES_USER" -h localhost -p $PGPORT -c "CREATE DATABASE \"${TEST_DBNAME}\";"

  # Остановка сервера
  gosu postgres pg_ctl -D "$PGDATA" -m fast -w stop
fi

# Запуск сервера на переднем плане под пользователем postgres
exec gosu postgres /usr/local/bin/docker-entrypoint.sh postgres