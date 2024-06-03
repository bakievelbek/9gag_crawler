import re
import json
import datetime
import logging as logger


def images(response, url):
    script_tags = response.css('script::text').getall()

    pattern = r'"images\\":\{.+?\}\}'

    for script in script_tags:
        match = re.search(pattern, script)
        if match:
            json_like_str = match.group(0)
            json_like_str = json_like_str.replace('\\', '')
            try:
                json_data = json.loads(f"{{{json_like_str}}}")
                return json_data['images']
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON-like string. Post url: {url}")

    return None


def interaction_statistics(response, url):
    script_tags = response.css('script::text').getall()

    pattern = r'"interactionStatistic":'

    return_data = {
        'likes': 0,
        'dislikes': 0,
        'comments': 0
    }

    for script in script_tags:
        match = re.search(pattern, script)
        if match:
            script = script.replace('\\', '')

            try:
                json_data = json.loads(script)
                return_data['comments'] = json_data.get('interactionStatistic')[2].get('userInteractionCount')
                return_data['dislikes'] = json_data.get('interactionStatistic')[1].get('userInteractionCount')
                return_data['likes'] = json_data.get('interactionStatistic')[0].get('userInteractionCount')
                return return_data
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON-like string. Post url: {url}")
                return None


def convert_ts(ts):
    dt = datetime.datetime.fromtimestamp(int(ts))

    return dt.strftime('%Y-%m-%d %H:%M:%S')


def created_datetime(response, url):
    script_tags = response.css('script::text').getall()
    pattern = r'\\\"creationTs\\\":(\d+),'
    creation_ts = None
    for script in script_tags:
        match = re.search(pattern, script)
        if match:
            creation_ts = match.group(1)

    if not creation_ts:
        logger.error(f"Unable to fetch creation datetime. Post url: {url}")
        return None

    return convert_ts(creation_ts)
