FROM tensorflow/tensorflow:2.0.0-gpu-py3

RUN apt-get update && apt-get install -y --no-install-recommends \
  software-properties-common \
  language-pack-ja \
  locales \
  git \
  && add-apt-repository ppa:kelleyk/emacs \
  && apt-get update && apt-get install -y --no-install-recommends emacs26 \
  && locale-gen ja_JP.UTF-8 \
  && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc \ 
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/tsukudamayo/dotfiles.git \
  && cp -r ./dotfiles/linux/.emacs.d/ ~/ \
  && cp -r ./dotfiles/.fonts ~/ 

RUN pip install virtualenv \
  epc \
  numpy \
  matplotlib \
  pillow \
  scipy \
  opencv-python

WORKDIR /workspace
RUN chmod -R a+w .
