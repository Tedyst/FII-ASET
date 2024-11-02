FROM python:3.12-slim AS runner

WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt --no-cache-dir && \
    apt-get purge -y --auto-remove g++

COPY backend gunicorn.conf.py /app/backend/

EXPOSE 8000

RUN chmod +x /app/backend/entrypoint.sh

FROM runner AS development

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]

FROM runner AS production

LABEL org.opencontainers.image.source=https://github.com/Tedyst/FII-ASET
LABEL org.opencontainers.image.description="FII-ASET Project"
LABEL org.opencontainers.image.licenses=MIT

ARG user=django
ARG group=django
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group} && \
    useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} && \
    chown -R ${uid}:${gid} /app

USER ${uid}:${gid}

RUN [ "python", "/app/backend/manage.py", "collectstatic", "--noinput" ]
ENV DJANGO_SETTINGS_MODULE=backend.settings.prod

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]

FROM nginxinc/nginx-unprivileged:1.27.2-alpine AS nginx

USER nginx

COPY --from=production --chown=nginx /app/backend/staticfiles /var/www/static/
COPY --chown=nginx nginx.conf /etc/nginx/nginx.conf

RUN chmod -R 555 /var/www/static/ && \
    chmod 444 /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
