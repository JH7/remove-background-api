FROM python:3.8.5-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install curl libfontconfig1 libx11-6 libharfbuzz-dev libfribidi-dev -y
RUN curl -o magick https://imagemagick.org/archive/binaries/magick
RUN chmod a+x magick
RUN ./magick --appimage-extract
RUN pip3 install -r requirements.txt

ENV MAGICK_CONFIGURE_PATH /app/squashfs-root/usr/etc/ImageMagick-7/
ENV MAGICK_BIN /app/squashfs-root/usr/bin/magick

COPY . .

EXPOSE 8080

CMD [ "python3", "app.py"]