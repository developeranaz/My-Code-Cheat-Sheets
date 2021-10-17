FROM developeranaz/aria2-webui
RUN apt update -y
COPY default /default
COPY supervisor.conf /
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
