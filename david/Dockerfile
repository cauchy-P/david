FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80"]