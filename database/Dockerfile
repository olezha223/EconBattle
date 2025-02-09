FROM postgres:17

# Замена переменных в файле init.sql
RUN apt-get update && apt-get install -y gettext

# Установка gosu
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends gosu; \
    rm -rf /var/lib/apt/lists/*


COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Установка прав на выполнение скрипта
RUN chmod +x /usr/local/bin/entrypoint.sh

# Установка кастомного entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Экспонирование порта
EXPOSE ${PGPORT:-5432}