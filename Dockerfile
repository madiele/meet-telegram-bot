# base image
FROM python:3.8

# set the working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt .

# install the required packages
RUN pip install -r requirements.txt

# copy the application code
COPY . .

# specify the port on which the server will run
EXPOSE 5000

RUN python manage.py collectstatic

# run the server using the Procfile
CMD ["gunicorn", "-b", "0.0.0.0:5000", "letsMeetBot.wsgi", "--log-file", "-", "--workers", "1"]
