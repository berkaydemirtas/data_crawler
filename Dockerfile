FROM python:3.9

ADD main.py .

RUN pip install requests
RUN pip install psycopg2
RUN pip install beautifulsoup4
RUN pip install lxml

CMD ["python", "./main.py"]