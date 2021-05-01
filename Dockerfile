FROM python:3.7
LABEL MAINTAINER="Anirban Bhattacherji <anirbanbhattacherji@gmail.com>"
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
RUN python setup.py install
ENV HOST "0.0.0.0'
ENV PORT 5000
ENV SERVER_NAME "0.0.0.0:5000"
ENV MONGODB_HOST = "localhost"
EXPOSE 5000
# ENTRYPOINT ["python"]
# CMD [ "userapp/app.py" ]
CMD [ "python", "userapp/app.py" ]