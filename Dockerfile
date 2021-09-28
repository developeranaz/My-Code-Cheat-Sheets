FROM pingme998/se-cr-vn:1
RUN apt install jupyter

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /system/sup*.sh
