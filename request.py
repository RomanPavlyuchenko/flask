import requests
import time

json = {
    'user_ids': [1,6,7]
}

resp = requests.post('http://127.0.0.1:5051/send/', json=json)
print(resp)
print(resp.json())
task_id = resp.json().get('task_id')
print(task_id)

status = 'PENDING'

while status == 'PENDING':
    resp = requests.get(f'http://127.0.0.1:5051/send/{task_id}')
    print(resp.json())
    status = resp.json().get('status')
    time.sleep(5)

