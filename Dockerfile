FROM nginx:1.31.2-alpine

WORKDIR /usr/share/nginx/html
COPY --exclude=Dockerfile --exclude=README.md --exclude=nginx.conf . .
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
