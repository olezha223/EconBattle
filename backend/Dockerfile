FROM python:3.11.5

RUN mkdir "api"

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /api/requirements.txt

WORKDIR api

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:main", "--host", "0.0.0.0", "--port", "8000"]