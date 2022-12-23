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


from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Line, Pie, Bar, Bar3D


JSON_COMMITS = {}


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

CORS(app, resources={r'/*': {'origins': '*'}})


REPO_OWNER = "pyecharts"
REPO_NAME = "pyecharts"

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


def search_github_repository(repo_name):
    base_url = "https://api.github.com/search/repositories"

    params = {
        "q": repo_name,  # The search query is the repository name
        "sort": "stars",  # Sort the results by number of stars
        "order": "desc"   # Order the results in descending order
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()["items"]
        return results[0] if len(results) > 0 else None
    else:
        return None


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            print(f"\033[0;31;40m{func.__name__} throws exception as {e}\033[0m")
    return inner_function


@exception_handler
def fetch_json(category):

    param = params[category]
    link = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{category}'

    if category == 'commits':
        streams = []
        i = 1
        while True:
            link_final = link + f'?per_page=999&page={i}'
            response = requests.get(link_final, headers=headers)
            if response.status_code == 200:
                byteStream = response.content
                if byteStream.decode('utf-8') == '[]':
                    break
                streams.append(byteStream)
                i += 1
            else:
                raise RuntimeWarning(f"[Back-end] Error when requesting {category} with status code {response.status_code}\n{response.content}")
        results = []
        for stream in streams:
            results.extend(json.loads(stream))
        return results

    else:
        if param:
            link = link + '?' + '&'.join([str(key) + '=' + str(value) for key, value in param.items()])

        while True:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                byteStream = response.content
                return json.loads(byteStream)
            else:
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
    data = fetch_json("stats/contributors")

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
    data = fetch_json("issues")
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
    data = fetch_json("stats/code_frequency")

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


@exception_handler
@app.route("/commits")
def get_commits_data():
    data = fetch_json("commits")

    for commit in data:
        name = commit['commit']['author']['name']
        time_ = commit['commit']['author']['date']
        JSON_COMMITS[time_] = name

    response = jsonify(JSON_COMMITS)
    return response


@exception_handler
@app.route('/filter_commits', methods=['POST', 'GET'])
def filter_commits():
    start_time = request.args.get('start', formatted_utc_time(0)[:10])
    end_time = request.args.get('end', formatted_utc_time()[:10])

    get_commits_data()
    # assume data key is time
    result = {}
    for date in JSON_COMMITS.keys():
        day = date[:10]
        if day >= start_time and day <= end_time:
            name = str(JSON_COMMITS[date])
            result[f'{day} {name}'] = result[f'{day} {name}'] + 1 if f'{day} {name}' in result.keys() else 1

    datas = []
    for k, v in result.items():
        ls = list(k.split(' '))
        datas.append([ls[0], ls[1], v])

    b3d = (
        Bar3D()
        .add(
            "Commits",
            datas,
            xaxis3d_opts=opts.Axis3DOpts([d[0] for d in datas], type_="category"),
            yaxis3d_opts=opts.Axis3DOpts([d[1] for d in datas], type_="category"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=20),
            title_opts=opts.TitleOpts(title="Commits Heatmap"),
        )
        .set_series_opts(tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} made {b}<br/>on {c} times"
                ),
        )
    )

    return b3d.dump_options_with_quotes()


@exception_handler
@app.route("/selectRepo", methods=["POST"])
def select_repo():
    params = request.form

    global REPO_OWNER
    global REPO_NAME

    repo = search_github_repository(params['repo_name'])
    if repo:
        owner_name = list(repo['full_name'].split('/'))
        REPO_OWNER, REPO_NAME = owner_name[0], owner_name[1]
        return 'Success'
    else:
        return 'Invalid'


token = os.getenv("GITHUB_TOKEN")
if not token:
    raise RuntimeError("No token has been specified in .env")

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
