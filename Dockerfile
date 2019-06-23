FROM debian:stretch-slim

RUN apt update -y && apt install -y wget 

RUN wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz \
    -O edgetpu_api.tar.gz --trust-server-names && \
    tar xzf edgetpu_api.tar.gz && \
    cd edgetpu_api && \
    mkdir -p /etc/udev/rules.d && \
    sed "s/sudo//g" install.sh > install_tmp.sh && \
    echo y | bash install_tmp.sh

RUN mkdir -p /Downloads && \
    cd /Downloads && \
    wget https://dl.google.com/coral/canned_models/all_models.tar.gz && \
    tar xzf all_models.tar.gz && \
    rm all_models.tar.gz

RUN pip3 install opencv-python pillow 

CMD ["python3", "app.py"]


