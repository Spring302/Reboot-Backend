FROM python:3.10
WORKDIR /app
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD [ "python",  "manage.py", "runserver", "0.0.0.0:8000" ]