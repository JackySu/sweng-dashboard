lmfao you know how to run this
## if you clone the repo
1. cd to the root folder
2. create a `.env` file in root folder, put `GITHUB_TOKEN={your_token}` 
3. 
```
py app.py
npm install
npm run dev
```
## if you pull from docker
`docker run -e GITHUB_TOKEN={your_token} --expose 50060 -p 50060:50060 --expose 4622 -p 4622:4622 --rm -ti --network=host iuxe/sweng-dashboard:latest`

happy 2023 :>
