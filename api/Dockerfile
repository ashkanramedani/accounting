FROM python:3.10.12

WORKDIR /app

COPY . .
 
RUN python -m pip install --upgrade pip 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6695"]
