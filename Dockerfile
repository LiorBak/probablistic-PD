FROM python:3.10-alpine

ADD ./ /opt/otree
ADD ./entrypoint.sh /entrypoint.sh
ADD ./pg_ping.py /pg_ping.py
ADD ./requirements.txt /opt/otree/requirements.txt

RUN apk update \
 && apk add  --no-cache bash \
                          curl \
                          gcc \
                          musl-dev \
                          postgresql \
                          postgresql-dev \
                          libffi \
                          libffi-dev \
    && pip install --no-cache-dir -r /opt/otree/requirements.txt \
    && pip3 uninstall -y uvicorn \
    && pip3 install uvicorn[standard] \
    && mkdir -p /opt/init \
    && chmod +x /entrypoint.sh \
    && apk del curl gcc musl-dev postgresql-dev libffi-dev

WORKDIR /opt/otree
VOLUME /opt/init
ENTRYPOINT ["bash", "/entrypoint.sh"]
CMD ["otree", "runprodserver", "--port=80"]
EXPOSE 80
