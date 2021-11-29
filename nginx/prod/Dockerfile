FROM nginx:1.19.9-alpine
COPY prod/prod.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]