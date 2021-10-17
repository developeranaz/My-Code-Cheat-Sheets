FROM developeranaz/aria2-webui
RUN apt update -y
COPY default /default
COPY supervisor.conf /
COPY index.html /index.html
RUN cat /index.html >/var/www/html/index.html
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
