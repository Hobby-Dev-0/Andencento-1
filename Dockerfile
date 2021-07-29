
FROM python:3.9
WORKDIR .
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
COPY . .
CMD ["bash", "start"]
