FROM pingme998/cr-yum:1
RUN apt install unzip -y
RUN unzip chromedriver_linux64.zip -d /usr/bin
RUN apt install git -y
WORKDIR /

#RUN apt install ffmpeg -y
RUN wget 'https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip'

COPY e.sh /e.sh
RUN chmod +x /e.sh
CMD /e.sh
