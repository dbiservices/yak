FROM python:3.11

COPY sync.py .

RUN pip install boto3 azure-storage-blob azure-identity oci

CMD ["python", "-u", "./sync.py"]