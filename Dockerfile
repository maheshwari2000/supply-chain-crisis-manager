# Use a base image with Python
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Copy environment file (if using .env)
COPY .env .

# Set environment variables for AWS (alternative to .env)
# ENV AWS_REGION=us-east-1
# ENV BEDROCK_AGENT_ID=your_agent_id_here

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]