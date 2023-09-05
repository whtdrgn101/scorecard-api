# Dockerfile

# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SCORECARD_USER scorecard
ENV SCORECARD_PASS Abc@123
ENV SCORECARD_HOST 192.168.2.40
ENV SCORECARD_DB scorecard_db
ENV JWT_SECRET_KEY f3e_Q7nex
ENV JWT_REFRESH_SECRET_KEY f3e_Q7neM3x1c4nF00d

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0"]