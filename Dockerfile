
FROM python:3.9
WORKDIR .
ENV PYTHONUNBUFFERED=1
RUN pip install -r https://raw.githubusercontent.com/Andencento/Andencento/main/requirements.txt
COPY . .
CMD ["bash", "start"]
