FROM python:3.10

WORKDIR /fapi_tz

COPY . /fapi_tz/

RUN pip install --no-cache-dir --upgrade -r requirements.txt
