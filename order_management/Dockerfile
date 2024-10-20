# Dockerfile for OMS using SQLite

# Step 1: Use an official Python runtime as a parent image
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the project files into the container
COPY . /app

# Step 4: Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Expose the OMS application port
EXPOSE 8000

# Step 6: Run the Django development server for OMS
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
