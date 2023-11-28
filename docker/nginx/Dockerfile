FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY proxy_params /etc/nginx

#RUN #{ \
#      echo 'client_max_body_size 1G;'; \
#    } > /etc/nginx/conf.d/nginx.conf