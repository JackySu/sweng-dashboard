lmfao you know how to run this
## if you clone the repo
1. cd to the root folder
2. create a `.env` file in root folder, put `GITHUB_TOKEN={your_token}` 
3. follow 5 or 6  

## if you pull from docker
4. `docker run -e GITHUB_TOKEN={your_token} --expose 50060 -p 50060:50060 --expose 4622 -p 4622:4622 --rm -ti iuxe/sweng-dashboard:latest`
you can choose to whether
5. `uvicorn app:app --host 0.0.0.0 --port 50060 --loop uvloop & npm run dev`  
which will run the back-end with built-in ASGI uvicorn
6. `gunicorn app:app -b 0.0.0.0:50060 -w 4 -k uvicorn.workers.UvicornWorker & npm run dev`  
or use gunicorn as a more efficient solution as above  

apache bench is integrated in the docker image so feel free to test the speed
but uvloop won't work out as fast as expected since the bottleneck lies in aiohttp when I request the github repo API
### flask is really impressive but async just better when it comes to requesting 80+ pages of big repos
happy 2023 :>
