# Use the official Python base image
FROM python:3.9-slim

# Install libxml2 and libxslt development packages
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Start the FastAPI app with auto-restart using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# starts the container good, forever end don 
# build 
# docker build -t trendimpact .
# run 
# docker run -d --name trendimpact_container --network host -v trendimpact_volume:/app/core_data --restart unless-stopped trendimpact

