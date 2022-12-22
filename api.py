import requests
import time
import datetime
import os


JSON_FILES_PATH = "./jsonfiles/"
REPO_OWNER = "pyecharts"
REPO_NAME = "pyecharts"
UPDATE_INTERVAL = 1000  # secs
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


def store_all_data():
    for file_name in params.keys():
        file_path = f"{JSON_FILES_PATH}{'/'.join(list(file_name.split('/')[:-1]))}"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            print(f"\033[0;34;40m[Back-end] {file_path} does not exist and has been created\033[0m")

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("No token has been specified in .env")

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
    }

    while 1:

        for category in params.keys():
            try:
                param = params[category]
                link = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{category}'
                if category == 'commits':
                    i = 1
                    while 1:
                        link_final = link + f'?page={i}'
                        response = requests.get(link_final, headers=headers)
                        if response.status_code == 200:
                            byteStream = response.content
                            if byteStream.decode('utf-8') == '[]':
                                break
                            mode = 'wb+' if i == 1 else 'ab+'
                            with open(f'{JSON_FILES_PATH}{category}.json', mode=mode) as f:
                                f.write(byteStream)
                                f.write(str.encode('\n'))
                            i += 1
                        else:
                            raise RuntimeWarning(f"[Back-end] Error when requesting {category} with status code {response.status_code}\n{response.content}")
                else:
                    if param:
                        link = link + '?' + '&'.join([str(key) + '=' + str(value) for key, value in param.items()])
                    response = requests.get(link, headers=headers)
                    if response.status_code == 200:
                        byteStream = response.content
                        with open(f'{JSON_FILES_PATH}{category}.json', 'wb+') as f:
                            f.write(byteStream)
                    else:
                        raise RuntimeWarning(f"[Back-end] {formatted_local_time()} Error when requesting {category} with status code {response.status_code}\ncontent: {response.content}")
            except Exception as e:
                print(f"\033[0;31;40m{e}\033[0m")

        print(f"\033[0;32;40m[Back-end] {formatted_local_time()} .json files updated, next update in {UPDATE_INTERVAL} secs\033[0m")
        # sleep for 10 secs
        time.sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    store_all_data()
