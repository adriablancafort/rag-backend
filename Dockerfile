# Use an official Python runtime as a parent image
FROM python:latest

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose the port uvcorn will listen on
EXPOSE 8000

# Run the application:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]