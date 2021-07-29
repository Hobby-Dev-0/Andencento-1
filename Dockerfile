
FROM python:3.9
WORKDIR .
ENV PYTHONUNBUFFERED=1
COPY requirements.txt
RUN pip3 install -r -U requirements.txt
COPY . .
CMD ["bash", "start"]
