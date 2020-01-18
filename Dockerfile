FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001
CMD python manage.py runserver 0.0.0.0:3001
