FROM python 

WORKDIR /project_ads

COPY requirements.txt requirements.txt

RUN python -m venv venv

ENV PATH="/project_ads/venv/bin:$PATH"

RUN pip3 install -r requirements.txt 

COPY . .

EXPOSE 8000

CMD [ "python3","manage.py","runserver" ]