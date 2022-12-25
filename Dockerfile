FROM ubuntu:latest

WORKDIR /sweng_dashboard

COPY package*.json ./
COPY . .

RUN apt remove -y nodejs
RUN apt remove -y nodejs-doc 
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs python3

RUN npm -f install
RUN npm run build
RUN npm run dev

RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn -b 0.0.0.0:50060 app:app

EXPOSE 50060
EXPOSE 4622
