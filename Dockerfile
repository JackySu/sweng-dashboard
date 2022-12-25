FROM ubuntu:latest

WORKDIR /sweng-dashboard

COPY package*.json ./
COPY requirements.txt ./
COPY . .

ENV PATH /sweng-dashboard/node_modules/.bin:$PATH

# update 
RUN apt-get update
# install curl 
RUN apt-get install -y curl gcc g++ make apt-utils
# get install script and pass it to execute: 
RUN apt remove -y nodejs
RUN apt remove -y nodejs-doc
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 app.py &

RUN npm -f install
RUN npm run build
RUN npm run dev &

EXPOSE 50060
EXPOSE 4622

CMD ["/bin/bash"]