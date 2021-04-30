FROM python:3.8-slim-buster
LABEL MAINTAINER="Anirban Bhattacherji <anirbanbhattacherji@gmail.com>"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python setup.py install
ENV PORT 5000
ENV SERVER_NAME "0.0.0.0:5000"
EXPOSE 5000
ENTRYPOINT ["python"]
CMD [ "userapp/app.py" ]