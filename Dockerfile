FROM pingme998/gecko-on-fire:1
RUN apt install git -y
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
