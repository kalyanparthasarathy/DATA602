# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt contents into the container at /app
COPY requirements.txt Blotter.py ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the py file from Github
# RUN git clone https://github.com/kalyanparthasarathy/DATA602

# Run Blotter.py when the container launches
CMD [ "python", "./Blotter.py" ]
