import aiohttp
import asyncio
import psutil
import datetime
import time
import os
import uvicorn


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from functools import lru_cache
from collections import defaultdict


MAX_ERROR_TIMES = 10


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


REPO_OWNER = "Apache"
REPO_NAME = "echarts"

# stats/punch_card -> hourly commit count for each day
# stats/participation -> weekly commit count
# stats/code_frequency -> a weekly aggregate of the number of additions and deletions pushed to a repository
params = {
    "stats/contributors": {},
    "issues": {},
    "stats/code_frequency": {},
    # this actually fetches all commits by setting per page commit to 1
    "commits": {},
    "stats/punch_card": {},
    "stats/participation": {}
}


def formatted_local_time() -> str:
    time_stamp = time.time()
    time_array = time.localtime(time_stamp)
    res = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return res


def formatted_utc_time(t=None) -> str:
    d = datetime.datetime.utcnow() if t is None else datetime.datetime.fromtimestamp(t)
    # eg. 2017-08-30T16:49:47Z
    return d.strftime('%Y-%m-%dT%H:%M:%SZ')


def async_lru_cache(*lru_cache_args, **lru_cache_kwargs):
    def async_lru_cache_decorator(async_function):
        @lru_cache(*lru_cache_args, **lru_cache_kwargs)
        def cached_async_function(*args, **kwargs):
            coroutine = async_function(*args, **kwargs)
            return asyncio.ensure_future(coroutine)
        return cached_async_function
    return async_lru_cache_decorator


async def fetch(session, url):
    errors = 0
    while errors < MAX_ERROR_TIMES:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                errors += 1
                await asyncio.sleep(1)

    raise RuntimeWarning(f"[Back-end] ≥{MAX_ERROR_TIMES} Errors when requesting {url}")


@async_lru_cache(maxsize=30)
async def fetch_json(category: str, owner: str = None, name: str = None):
    if not owner or not name:
        owner = REPO_OWNER
        name = REPO_NAME

    param = params[category]
    link = f'https://api.github.com/repos/{owner}/{name}/{category}'

    errors = 0
    if category == 'commits':

        i = 1
        while errors < MAX_ERROR_TIMES:
            link_final = link + f'?per_page=999&page={i}'
            async with aiohttp.ClientSession() as session:
                tasks = []
                for url in [link + f'?per_page=999&page={i}' for i in range(20)]:
                    tasks.append(fetch(session, url))
                contents = await asyncio.gather(*tasks)

                results = []
                for content in contents:
                    if content == '[]':
                        continue
                    results.extend(content)
                return results

    else:

        link_final = link + '?' + '&'.join([str(key) + '=' + str(value) for key, value in param.items()]) if param else link

        while errors < MAX_ERROR_TIMES:
            async with aiohttp.ClientSession() as session:
                return await fetch(session, link_final)


@app.get("/lineDynamicData")
async def update_line_data():
    data = {"name": formatted_local_time(), "cpu_usage": psutil.cpu_percent(percpu=False), "ram_usage": psutil.virtual_memory().percent}
    # print(f"{formatted_local_time()}: {data}")
    return data


# stats/punch_card -> hourly commit count for each day
# stats/participation -> weekly commit count
# stats/code_frequency -> a weekly aggregate of the number of additions and deletions pushed to a repository


@app.get("/stats/contributors")
async def get_stats_contributors_data(owner: str = None, name: str = None):
    temp_dict = {}
    data = await fetch_json("stats/contributors", owner, name)

    for item in data:
        contributor = item['author']['login']
        commits = item['total']
        temp_dict[contributor] = commits

    data_pair = sorted(temp_dict.items(), key=lambda x: x[1])
    res = []
    legends = []
    for data_point in data_pair:
        legends.append(data_point[0])
        res.append({
            'name': data_point[0],
            'value': data_point[1]
        })

    return {'proportions': res, 'legends': legends}


@app.get("/issues")
async def get_issues_data(owner: str = None, name: str = None):
    data = await fetch_json("issues", owner, name)
    issues = {}
    for item in data:
        issue = {}
        issue['closed'] = False if item['closed_at'] is None else True
        # T Z means UTC time
        issue['created_time'] = item['created_at']
        issue['updated_time'] = item['updated_at']
        issues[item['number']] = issue

    return issues


@app.get("/stats/code_frequency")
async def get_stats_code_frequency_data(owner: str = None, name: str = None):
    data = await fetch_json("stats/code_frequency", owner, name)

    addition = []
    deletion = []
    timeline = []
    for item in data:
        dt = datetime.datetime.fromtimestamp(item[0])
        timeline.append(dt)
        if (item[1] + item[2] == 0):
            addition.append({'value': item[1], 'percent': item[1]})
            deletion.append({'value': item[2], 'percent': item[2]})
        else:
            addition.append({'value': item[1], 'percent': item[1] / (item[1] - item[2])})
            deletion.append({'value': item[2], 'percent': item[2] / (item[2] - item[1])})

    return {'timeline': timeline, 'addition': addition, 'deletion': deletion}


async def get_commits_data(owner=None, name=None):
    data = await fetch_json("commits", owner, name)

    result = {}
    for commit in data:
        name = commit['commit']['author']['name']
        time_ = commit['commit']['author']['date']
        result[time_] = name

    return result


@app.get('/filter_commits')
async def filter_commits(owner: str = None, name: str = None, start_time: str = None, end_time: str = None):

    if start_time is None:
        start_time = formatted_utc_time(0)[:10]
    if end_time is None:
        end_time = formatted_utc_time()[:10]

    result = await get_commits_data(owner, name)
    # assume data key is time
    counter = defaultdict(lambda: defaultdict(int))
    names = set()
    for date in result.keys():
        day = date[:10]
        if day <= end_time:
            if day >= start_time:
                name = str(result[date])
                names.add(name)
                counter[day][name] += 1
            else:
                break

    result = []
    for day in counter.keys():
        for name, count in counter[day].items():
            result.append([day, name, count])
    return {'result': result, 'names': list(names)}


token = os.getenv("GITHUB_TOKEN")
if not token:
    raise RuntimeError("GITHUB_TOKEN not declared in env variables")


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
}


# in gunicorn __name__ does not necessarily equal to __main__
# gunicorn -b 0.0.0.0:XXXX app:{__name__}
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 50060))
    uvicorn.run(app='app:app', host='localhost', port=port, reload=True)
