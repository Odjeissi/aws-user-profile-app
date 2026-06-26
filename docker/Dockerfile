FROM python:3.11-alpine

WORKDIR /usr/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 5000

CMD [ "python", "app.py" ]
