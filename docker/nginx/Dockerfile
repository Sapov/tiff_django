FROM jwilder/nginx-proxy:1.2

COPY default_location /etc/nginx/vhost.d/default_location
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN { \
      echo 'server_tokens off;'; \
      echo 'client_max_body_size 100m;'; \
    } > /etc/nginx/conf.d/nginx.conf