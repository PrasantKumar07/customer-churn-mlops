FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining project files
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py", "--server.address=0.0.0.0"]