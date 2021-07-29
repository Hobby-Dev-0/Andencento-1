
FROM python:3.9
WORKDIR .
ENV PYTHONUNBUFFERED=1
RUN pip3 install -r requirements.txt
COPY . .
CMD ["bash", "start"]
