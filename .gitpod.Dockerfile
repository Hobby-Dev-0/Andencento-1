FROM python:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg python3-pip opus-tools
RUN git clone https://github.com/Andencento/Andencento.git /root/Andencento
WORKDIR /root/Andencento
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip install -r requirements.txt
CMD ["python3","-m","userbot"]
