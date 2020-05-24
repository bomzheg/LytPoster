FROM python:3.7-buster
LABEL maintainer="bomzheg <bomzheg@gmail.com>" \
      description="Lytkarino Online Telegram Bot"
COPY requirements.txt /lyt_poster/requirements.txt
RUN pip install --no-cache-dir -r lyt_poster/requirements.txt
VOLUME /lyt_poster/log
EXPOSE 8000
COPY . /lyt_poster
CMD [ "python", "lyt_poster/app" ]