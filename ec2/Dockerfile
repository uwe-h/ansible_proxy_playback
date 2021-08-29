FROM ubuntu:20.04
RUN apt-get update && TZ="Europe/Berlin" apt-get install -y curl less unzip cron python3.9 python3-distutils xxd

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
copy ./httpproxy/mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
RUN update-ca-certificates --fresh
RUN  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py && python3.9 -m pip install ansible boto3 certifi requests
RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.9 /usr/bin/python3 && cat /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt >> /usr/local/lib/python3.9/dist-packages/certifi/cacert.pem
RUN mkdir /downloads
VOLUME /ansible
WORKDIR /ansible
ENTRYPOINT /bin/bash