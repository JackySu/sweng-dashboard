import requests
import psutil
import logging
import datetime
import time
import os
import json


from flask.json import jsonify
from flask import Flask, request
from flask_cors import CORS


from collections import defaultdict


MAX_ERROR_TIMES = 10


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

CORS(app, resources={r'/*': {'origins': '*'}})


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


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            print(f"\033[0;31;40m{func.__name__} throws exception as {e}\033[0m")
    return inner_function


@exception_handler
def fetch_json(owner, name, category):

    param = params[category]
    link = f'https://api.github.com/repos/{owner}/{name}/{category}'

    errors = 0
    if category == 'commits':
        streams = []
        i = 1
        while errors < MAX_ERROR_TIMES:
            link_final = link + f'?per_page=999&page={i}'
            response = requests.get(link_final, headers=headers)
            if response.status_code == 200:
                byteStream = response.content
                if byteStream.decode('utf-8') == '[]':
                    break
                streams.append(byteStream)
                i += 1
            else:
                errors += 1
                time.sleep(1)

        if errors >= MAX_ERROR_TIMES:
            raise RuntimeWarning(f"[Back-end] ≥{MAX_ERROR_TIMES} Errors when requesting {category} with status code {response.status_code}\n{response.content}")

        results = []
        for stream in streams:
            results.extend(json.loads(stream))
        return results

    else:
        if param:
            link = link + '?' + '&'.join([str(key) + '=' + str(value) for key, value in param.items()])

        while errors < MAX_ERROR_TIMES:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                byteStream = response.content
                return json.loads(byteStream)
            else:
                errors += 1
                time.sleep(1)

        if errors >= MAX_ERROR_TIMES:
            raise RuntimeWarning(f"[Back-end] {formatted_local_time()} Error when requesting {category} with status code {response.status_code}\ncontent: {response.content}")


@app.route("/lineDynamicData")
def update_line_data():
    data = {"name": formatted_local_time(), "cpu_usage": psutil.cpu_percent(percpu=False), "ram_usage": psutil.virtual_memory().percent}
    # print(f"{formatted_local_time()}: {data}")
    response = jsonify(data)
    return response


# stats/punch_card -> hourly commit count for each day
# stats/participation -> weekly commit count
# stats/code_frequency -> a weekly aggregate of the number of additions and deletions pushed to a repository


@exception_handler
@app.route("/stats/contributors")
def get_stats_contributors_data():
    temp_dict = {}
    owner = request.args.get('owner')
    name = request.args.get('name')
    data = fetch_json(owner, name, "stats/contributors")

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


@exception_handler
@app.route("/issues")
def get_issues_data():
    owner = request.args.get('owner')
    name = request.args.get('name')
    data = fetch_json(owner, name, "issues")
    issues = {}
    for item in data:
        issue = {}
        issue['closed'] = False if item['closed_at'] is None else True
        # T Z means UTC time
        issue['created_time'] = item['created_at']
        issue['updated_time'] = item['updated_at']
        issues[item['number']] = issue

    response = jsonify(issues)
    return response


@exception_handler
@app.route("/stats/code_frequency")
def get_stats_code_frequency_data():
    owner = request.args.get('owner')
    name = request.args.get('name')
    data = fetch_json(owner, name, "stats/code_frequency")

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


def get_commits_data(owner=None, name=None):
    if owner is None and name is None:
        owner = REPO_OWNER
        name = REPO_NAME

    data = fetch_json(owner, name, "commits")

    result = {}
    for commit in data:
        name = commit['commit']['author']['name']
        time_ = commit['commit']['author']['date']
        result[time_] = name

    return result


@exception_handler
@app.route('/filter_commits', methods=['POST', 'GET'])
def filter_commits():

    start_time = request.args.get('start', formatted_utc_time(0)[:10])
    end_time = request.args.get('end', formatted_utc_time()[:10])
    owner = request.args.get('owner')
    name = request.args.get('name')

    result = get_commits_data(owner, name)
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
    raise RuntimeError("GITHUB_TOKEN not in environmental variables")


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
}


# in gunicorn __name__ does not necessarily equal to __main__
# gunicorn -b 0.0.0.0:XXXX app:{__name__}
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 50060))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
