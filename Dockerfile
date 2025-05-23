FROM python:3-slim
WORKDIR /programas/ingesta
RUN pip install pymysql boto3
COPY . .
CMD ["python3", "./ingesta.py"]
