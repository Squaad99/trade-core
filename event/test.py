import requests

r = requests.post('http://localhost:8000/api/event-start/', auth=('Squaad', 'Cofems89'))
r.status_code

print(r)