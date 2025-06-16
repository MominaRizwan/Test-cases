# Use Python base image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    xdg-utils \
    libgbm-dev \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (compatible version with Chrome 137)
RUN CHROME_DRIVER_VERSION=`curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])"` && \
    wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/*

# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome \
    PATH=$PATH:/usr/local/bin/chromedriver

# Set work directory
WORKDIR /app

# Copy test script and requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY test.py .

# Run the tests
CMD ["python", "test.py"]
