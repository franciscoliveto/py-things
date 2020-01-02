FROM torizon/arm32v7-debian-base:buster

ARG APPNAME

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-setuptools && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

#RUN pip3 install -r ./requirements.txt
RUN pip3 install pyserial

ENV ENVAPPNAME ${APPNAME}

COPY py-things/$ENVAPPNAME .

CMD python3 $ENVAPPNAME