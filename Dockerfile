FROM pingme998/pywebio:1
RUN apt update
COPY app.sh /app.sh
RUN chmod +x /app.sh
CMD /app.sh
