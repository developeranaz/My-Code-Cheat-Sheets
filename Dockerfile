FROM pingme998/ch-se-vn:1
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /system/sup*.sh
