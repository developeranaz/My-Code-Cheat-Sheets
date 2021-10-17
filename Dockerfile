FROM developeranaz/aria2-webui
RUN apt update -y
COPY 
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
