FROM python:3.8
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./pokeapi /app/pokeapi
COPY ./.envars /app/.envars
