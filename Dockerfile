# Use an official Python runtime as a parent image
FROM python:3.11.5

# Create the app directory
RUN mkdir /app

# Set the working directory in the container
WORKDIR /app

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Upgrade pip
RUN pip install --upgrade pip 

# Copy the requirements file into the container
COPY requirements.txt /app/

# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
# RUN \
#     apk add --no-cache postgresql-libs && \
#     apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
#     python3 -m pip install -r requirements.txt --no-cache-dir && \
#     apk --purge del .build-deps

# Copy the project files into the container
COPY . /app/

# Set environment variables - used for database settings and DEBUG
#ENV SECRET_KEY = "django-insecure-x-q637iz-(mlzuvbg*-_9bm60wos^#1-5m+eyp_vgl)qfm*1qh"
#ENV DEBUG = "True"
#ENV DATABASE_URL = "postgresql://postgres:8338@localhost:5432/interview_app"
#ENV REDIS_URL = "redis://127.0.0.1:6379/0"
#ENV CACHE_TTL_SECONDS = "60"
#ENV PAGINATION_PAGE_SIZE = "10"
#ENV ACCESS_TOKEN_EXPIRE_SECONDS = "3600"
#ENV REQUEST_PER_MIN = "30"

# Collect static files
# RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]