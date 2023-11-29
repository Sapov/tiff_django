FROM nginx:latest

RUN mkdir persistentdata
RUN mkdir persistentdata/certbot
RUN mkdir persistentdata/certbot/conf
RUN mkdir persistentdata/certbot/www
RUN mkdir persistentdata/certbot/conf/live/
RUN mkdir persistentdata/certbot/conf/live/orders.san-cd.ru/ # adjust to your domain orders.san-cd.ru
RUN mkdir persistentdata/static
RUN mkdir persistentdata/media
RUN mkdir persistentdata/db
#RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

#COPY proxy_params /etc/nginx

#RUN #{ \
#      echo 'client_max_body_size 1G;'; \
#    } > /etc/nginx/conf.d/nginx.conf