FROM pingme998/cr-yum:1
RUN apt install git -y
COPY e.sh /e.sh
RUN chmod +x /e.sh
CMD /e.sh
