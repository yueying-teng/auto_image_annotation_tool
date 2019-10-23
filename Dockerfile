FROM tensorflow/tensorflow:1.14.0-py3
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y \
					--fix-missing \
                    build-essential \
                    git \
                    wget \
                    vim \
                    libopencv-dev \
                    ffmpeg \
                    && apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

ADD $PWD/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN mkdir -p /inception/model/
RUN mkdir -p /inception/scripts/
RUN mkdir -p /inception/data/
RUN mkdir -p /inception/output/

ENV PATH=$PATH:/inception/scripts

WORKDIR /inception/scripts

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 8080 8501