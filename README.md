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
`docker run -e GITHUB_TOKEN={your_token} --expose 50060 -p 50060:50060 --expose 4622 -p 4622:4622 --rm -ti iuxe/sweng-dashboard:latest`
you can choose to whether
* `python3 app.py & npm run dev &`
which will run the back-end with built-in wsgi unicorn, or
* `gunicorn app:app -b 0.0.0.0:50060 -w 4 -k uvicorn.workers.UvicornWorker & npm run dev &`
use gunicorn as a more efficient solution, -w 4 means 4 processes (better be the number of your cpu cores)
### well I abandoned Flask, async just better
happy 2023 :>
