FROM pingme998/pywebio:2
RUN apt update
RUN apt install git -y
RUN pip install flask
COPY app.sh /app.sh
COPY stream.sh /stream.sh
COPY /
RUN chmod +x /stream.sh
RUN chmod +x /app.sh
RUN chmod +x /stream1.sh
RUN chmod +x /stream2.sh
RUN chmod +x /stream3.sh
CMD /app.sh
