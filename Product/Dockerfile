FROM python:3.8
RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install Django
RUN pip install gunicorn
RUN pip install mysqlclient
RUN mkdir -p /crm
ENV HOME=/crm
ENV APP_HOME=/crm/accounts
RUN mkdir $APP_HOME
WORKDIR $HOME
COPY . $HOME
CMD [ "python manage.py runserver" ]
