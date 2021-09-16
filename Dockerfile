FROM pingme998/pywebio:2
RUN apt update
RUN apt install git -y
RUN pip install flask
COPY app.sh /app.sh
COPY stream.sh /stream.sh
COPY stream1.sh /stream1.sh
COPY stream2.sh /stream2.sh
COPY stream3.sh /stream3.sh
RUN chmod +x /stream.sh
RUN chmod +x /app.sh
RUN chmod +x /stream1.sh
RUN chmod +x /stream2.sh
RUN chmod +x /stream3.sh
CMD /app.sh
