FROM python

COPY requirements.txt /

RUN pip install -r requirements.txt