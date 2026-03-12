import requests

headers ={
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzczODc5ODQzfQ.qDzNxibBOMOIMNyYDCyRvHc1-W8zJj8quXiIgYV1Py0"
}

request = requests.post("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(request)
print(request.json())