FROM debain:buster-slim

RUN apt-get update -y && apt install -y wget libopencv-dev python-opencv

RUN wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz \
    -O edgetpu_api.tar.gz --trust-server-names && \
    tar xzf edgetpu_api.tar.gz && \
    cd edgetpu_api && \
    sed "s/sudo//g" install.sh > install.sh && \
    mkdir -p /etc/udev/rules.d && \
    echo y | bash ./install.sh

RUN mkdir -p /Downloads && \
    cd /Downloads && \
    wget https://dl.google.com/coral/canned_models/all_models.tar.gz && \
    tar xzf all_models.tar.gz && \
    rm all_models.tar.gz



RUN pip install opencv-python pillow 

RUN apt install -y openssh-server rsync tmux
CMD ["/bin/bash", "-c" , "mkdir -p /var/run/sshd && /usr/sbin/sshd -D"]


