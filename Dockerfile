FROM ubuntu:latest

WORKDIR /sweng_dashboard

COPY package*.json ./
COPY . .

# update 
RUN apt-get update
# install curl 
RUN apt-get install -y curl
# get install script and pass it to execute: 
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash
RUN apt-get install -y nodejs
RUN apt-get install -y python3

RUN npm -f install
RUN npm run build
RUN npm run dev

RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn -b 0.0.0.0:50060 app:app

EXPOSE 50060
EXPOSE 4622
