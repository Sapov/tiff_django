FROM jwilder/nginx-proxy:1.6
COPY default_location /etc/nginx/vhost.d/default_location

#RUN rm /etc/nginx/conf.d/default.conf
#COPY nginx.conf /etc/nginx/conf.d
#COPY proxy_params /etc/nginx
RUN rm /etc/nginx/conf.d/default.conf

RUN { \
      echo 'client_max_body_size 1G;'; \
    } > /etc/nginx/conf.d/nginx.conf
