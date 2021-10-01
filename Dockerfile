FROM ubuntu
RUN apt install python3 -y
RUN apt install firefox -y
RUN apt install jupyter -y
RUN apt install pip -y
RUN pip install selenium
RUN apt install git -y
RUN apt install aria2 -y
RUN apt install rclone -y
RUN wget 'https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz'
RUN tar -xf geckodriver-v0.30.0-linux64.tar.gz

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /en*.sh
