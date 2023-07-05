import csv
import json

from ktask_4.config import Config


def from_csv_to_json(csv_path, json_path):
    with open(csv_path, 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers

        data = [row for row in reader]

    data.sort(key=lambda x: x[1])

    data = [
        {
            'name': item[1] + ' ' + item[0],
            'task': item[2],
            'picture_1_url': item[3],
            'picture_2_url': item[4],
            'picture_1_description': item[5],
            'picture_2_description': item[6],
            'number': i + 1
        }
        for i, item in enumerate(data) if item[0]]

    children_data = {}

    for item in data:
        if item['name'] not in children_data:
            children_data[item['name']] = [{
                'picture_1_description': item['picture_1_description'],
                'picture_1_url': item['picture_1_url'],
                'picture_2_description': item['picture_2_description'],
                'picture_2_url': item['picture_2_url'],
                'task': item['task']
            }]
        else:
            children_data[item['name']].append({
                'picture_1_description': item['picture_1_description'],
                'picture_1_url': item['picture_1_url'],
                'picture_2_description': item['picture_2_description'],
                'picture_2_url': item['picture_2_url'],
                'task': item['task']
            })

    result = {}
    current_id = 55
    # current_id = 1400
    # parent_id = 1154

    for k, v in children_data.items():

        result[current_id] = {
            'id': current_id,
            'name': k,
            'children': v
        }

        current_id += 1

    with open(json_path, 'w', encoding='utf-8') as fp:
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        fp.write(json_data)
