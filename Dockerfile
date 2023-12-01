# FROM mysql:latest
# COPY create-table.sql /docker-entrypoint-initdb.d/

# Use an official Python runtime as a parent image
FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

# CMD ["app.py" ]
CMD ["flask", "run"]