# Use the official Python base image
FROM python:3.9-slim

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

# to build the dockerimage wwanted:
# docker run -d --name trendimpact_container --network host -v /path/to/local/database:/app/core_data/flowimpact_api_db.db --restart unless-stopped trendimpact
