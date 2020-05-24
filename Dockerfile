FROM python:3.7-buster
LABEL maintainer="bomzheg <bomzheg@gmail.com>" \
      description="Lytkarino Online Telegram Bot"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
VOLUME log
EXPOSE 8000
COPY . .
CMD [ "python","-m", "app" ]