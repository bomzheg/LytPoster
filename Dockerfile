FROM python:3.7-buster
COPY ./requirements.txt /lyt_poster/requirements.txt
RUN pip install --no-cache-dir -r lyt_poster/requirements.txt
VOLUME /lyt_poster/log
COPY . /lyt_poster
EXPOSE 8000
CMD [ "python", "lyt_poster" ]