FROM mitmproxy/mitmproxy
COPY httpproxy/recorder_controller.py recorder_controller.py
#COPY httpproxy/mitmproxy/httpproxy.pem .
COPY httpproxy/mitmproxy/* /home/mitmproxy/.mitmproxy/
#COPY localstackcerts/server.test.pem .
VOLUME /recordings
#RUN chmod 777 /recordings
CMD ["mitmdump", "-s", "recorder_controller.py","-k", "--set", "connection_strategy=lazy"]
