FROM python:3.9

WORKDIR /fapi_tz

COPY . /fapi_tz/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
