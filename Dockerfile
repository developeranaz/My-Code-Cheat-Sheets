FROM ubuntu:latest
RUN apt update
RUN apt install python3 -y
RUN apt install pip3 -y
RUN pip install pywebio
COPY app.sh /app.sh
chmod +x /app.sh
CMD /app.sh
