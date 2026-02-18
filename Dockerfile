# Use the official Python image
FROM python:3.13-slim

ARG HTTP_PORT

WORKDIR /app
# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code
COPY ./src ./src

RUN mkdir -p ./output

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE $HTTP_PORT

CMD ["python", "-m", "src.main"]