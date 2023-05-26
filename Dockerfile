FROM python:3.6.15

COPY requirement.txt /tmp/requirement.txt
RUN cd /tmp && python -m pip install -r requirement.txt

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

CMD python main.py