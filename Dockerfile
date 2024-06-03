FROM python:3.12
LABEL authors="gabriel.cerioni"

# Set the working directory in the container
WORKDIR /usr/src

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files and folders to the container
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /usr/src/

# Make entrypoint.sh executable
RUN chmod +x /usr/src/entrypoint.sh

# Set PYTHONPATH environment variable
ENV PYTHONPATH="/usr/src"

# Define environment variables with default values
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=""

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entrypoint script
ENTRYPOINT ["/usr/src/entrypoint.sh"]
