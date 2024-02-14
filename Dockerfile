FROM python:3.9-alpine

# Install necessary libraries
RUN apk add --no-cache mesa-dri-gallium mesa-glapi build-base libffi-dev openssl-dev

WORKDIR /app

COPY requirements.txt .

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install PyQt6 manually
RUN pip install --no-cache-dir PyQt6==6.6.1

COPY . .

CMD [ "python", "./main.py" ]
