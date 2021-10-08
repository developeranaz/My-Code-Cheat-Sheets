FROM developeranaz/gecko-on-fire:2
RUN apt install git -y
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
