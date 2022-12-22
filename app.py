import psutil
import logging
import datetime
import threading
import os
import api
import json


from flask.json import jsonify
from flask import Flask, request
from flask_cors import CORS


from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Line, Pie, Bar, Bar3D


JSON_COMMITS = {}
COMMITS_INIT = False


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

CORS(app, resources={r'/*': {'origins': '*'}})


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            print(f"[Front-end] {func.__name__} throws exception as {e}")
    return inner_function


@exception_handler
def bar_base() -> Bar:
    with open(f'{api.JSON_FILES_PATH}stats/code_frequency.json', 'rb') as f:
        data = json.loads(f.read())

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

        b = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(timeline)
            .add_yaxis("Additions", addition, stack="stack1", category_gap="30%", label_opts=opts.LabelOpts(position="top"),
                itemstyle_opts=opts.ItemStyleOpts(color="#FFBF00")
            )
            .add_yaxis("Deletions", deletion, stack="stack1", category_gap="30%", label_opts=opts.LabelOpts(position="bottom"),
                itemstyle_opts=opts.ItemStyleOpts(color="#5484AB")
            )
            .set_global_opts(
                datazoom_opts=opts.DataZoomOpts(
                    is_show=True,
                    is_zoom_lock=False,
                    range_start=0,
                    range_end=10,
                ),
            )
        )

        return b


@exception_handler
def pie_base() -> Pie:
    with open(f'{api.JSON_FILES_PATH}stats/contributors.json', 'rb') as f:

        temp_dict = {}
        data = json.loads(f.read())

        for item in data:
            contributor = item['author']['login']
            commits = item['total']
            temp_dict[contributor] = commits

        data_pair = [list(z) for z in zip(temp_dict.keys(), temp_dict.values())]

        # sort by number of commits
        data_pair.sort(key=lambda x: x[1])

        pie = (
            Pie(init_opts=opts.InitOpts(width="600px", height="500px"))
            .add(
                series_name="Contributor commits",
                data_pair=data_pair,
                rosetype="radius",
                radius="55%",
                center=["50%", "50%"],
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Contribution Graph",
                    pos_left="center",
                    pos_bottom=20,
                    title_textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                label_opts=opts.LabelOpts(color="rgba(145, 145, 145, 0.9)"),
            )
        )

        return pie


@exception_handler
def line_base() -> Line:

    line = (
        Line(init_opts=opts.InitOpts(width="500px", height="300px"))
        .add_xaxis(
            xaxis_data=[api.formatted_local_time()],
        )
        .add_yaxis(
            series_name="CPU Usage",
            y_axis=[psutil.cpu_percent(percpu=False)],
            is_smooth=True,
        )
        .add_yaxis(
            series_name="RAM Usage",
            y_axis=[psutil.virtual_memory().percent],
            is_smooth=True,
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                is_show=True,
                pos_left="50%",
            ),
            title_opts=opts.TitleOpts(title="Resources Monitor", pos_left="10%"),
            xaxis_opts=opts.AxisOpts(
                is_show=True,
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                min_interval=20,
                max_=100,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,
                is_zoom_lock=False,
                range_start=0,
                range_end=100,
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=False),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False, formatter="{@[1]}%", position="top"),  # set is_show=True to display
                         markpoint_opts=opts.MarkPointOpts(
                             data=[
                                 opts.MarkPointItem(type_="max")
                             ]
                         ),
                         markline_opts=opts.MarkLineOpts(
                             data=[
                                 opts.MarkLineItem(type_="average")
                             ]
                         ),
        )
    )
    return line


@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@app.route("/lineDynamicData")
def update_line_data():
    data = {"name": api.formatted_local_time(), "cpu_usage": psutil.cpu_percent(percpu=False), "ram_usage": psutil.virtual_memory().percent}
    # print(f"{formatted_local_time()}: {data}")
    response = jsonify(data)
    return response


# stats/punch_card -> hourly commit count for each day
# stats/participation -> weekly commit count
# stats/code_frequency -> a weekly aggregate of the number of additions and deletions pushed to a repository


@exception_handler
@app.route("/stats/contributors")
def get_stats_contributors_data():
    p = pie_base()
    return p.dump_options_with_quotes()


@exception_handler
@app.route("/issues")
def get_issues_data():
    with open(f'{api.JSON_FILES_PATH}issues.json', 'rb') as f:
        data = f.read()
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
    b = bar_base()
    return b.dump_options_with_quotes()



@exception_handler
@app.route("/commits")
def get_commits_data():
    datas = [json.loads(line) for line in open(f'{api.JSON_FILES_PATH}commits.json', 'rb')]

    for data in datas:
        for commit in data:
            name = commit['commit']['author']['name']
            time_ = commit['commit']['author']['date']
            url = commit['commit']['url']
            JSON_COMMITS[time_] = [name, url]

    global COMMITS_INIT
    COMMITS_INIT = True
    response = jsonify(JSON_COMMITS)
    return response


@exception_handler
@app.route('/filter_commits', methods=['POST', 'GET'])
def filter_commits():
    global COMMITS_INIT
    start_time = request.args.get('start', api.formatted_utc_time(0)[:10])
    end_time = request.args.get('end', api.formatted_utc_time()[:10])

    if not COMMITS_INIT:
        get_commits_data()
    # assume data key is time
    result = {}
    for date in JSON_COMMITS.keys():
        day = date[:10]
        if day >= start_time and day <= end_time:
            name = str(JSON_COMMITS[date][0])
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
@app.route("/stats/punch_card")
def get_stats_punch_card_data():
    with open(f'{api.JSON_FILES_PATH}stats/punch_card.json', 'rb') as f:
        return jsonify(f.read())


@exception_handler
@app.route("/stats/participation")
def get_stats_participation_data():
    with open(f'{api.JSON_FILES_PATH}stats/participation.json', 'rb') as f:
        return jsonify(f.read())


if __name__ == '__main__':
    update = threading.Thread(target=api.store_all_data)
    update.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
