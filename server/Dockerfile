# Use an official Python runtime as a parent image
FROM python:3.8-slim

LABEL maintainer="Marco Romanelli <marco.romanelli@epfl.ch>"

# Run as non-root user
RUN useradd -ms /bin/bash appuser
USER appuser

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
RUN mkdir -p /home/appuser/app
WORKDIR /home/appuser/app

ENV PYTHONPATH=/home/appuser/app
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install packages from requirements.txt
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the current directory contents into the container at /app
COPY --chown=appuser:appuser gunicorn.conf.py .
COPY --chown=appuser:appuser assets/ ./assets/
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser database.py .
COPY --chown=appuser:appuser index.py .

EXPOSE 8080

CMD ["gunicorn", "--config", "gunicorn.conf.py", "index:server"]
