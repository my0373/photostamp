# Use Fedora 41 as the base image
FROM fedora:41

# Set the working directory in the container
WORKDIR /app

# Install Python, pip, and ImageMagick
RUN dnf update -y && \
    dnf install -y python3 python3-pip ImageMagick tree && \
    dnf clean all

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY watermark.py .

# Set the entrypoint
ENTRYPOINT ["python3", "watermark.py"]
