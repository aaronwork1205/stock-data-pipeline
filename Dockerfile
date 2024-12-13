# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set environment variables to configure Java and Spark
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Install dependencies: OpenJDK (required for Spark), wget, and curl
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Download and install Spark
RUN wget https://apache.mirror.digitalpacific.com.au/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz -O /tmp/spark.tgz \
    && tar -xvzf /tmp/spark.tgz -C /opt \
    && rm /tmp/spark.tgz

# Install PySpark
RUN pip install pyspark

# Set the working directory
WORKDIR /app

# Expose the Spark port (optional, based on how you want to interact with Spark)
EXPOSE 7077

# Start an interactive PySpark session
CMD ["pyspark"]

