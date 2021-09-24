FROM pingme998/seleniumchdr:1
RUN apt update -y
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh
