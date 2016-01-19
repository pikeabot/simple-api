FROM nginx

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf  /etc/nginx/nginx.conf
COPY index.html /html/index.html
RUN service nginx restart