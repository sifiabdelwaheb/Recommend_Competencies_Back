FROM python:3.8.10

ARG DEFAULT_PORT=81

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# 80 Is the default value and can be edited with --env PORT=?
ENV PORT $DEFAULT_PORT

# Dollar sign indicate docker that's name of env variable
EXPOSE $PORT
ENV FLASK_APP annotator.py


# VOLUME [ "/app/node_modules" ]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
