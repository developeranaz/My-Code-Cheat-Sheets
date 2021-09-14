FROM pingme998/pywebio:1
RUN apt update
RUN apt install git -y
COPY app.sh /app.sh
RUN chmod +x /app.sh
CMD /app.sh
