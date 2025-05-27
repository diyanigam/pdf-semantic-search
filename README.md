# PDF Semantic Search

This enables users to perform text retrieval from a pdf with semantic search.

## how to use api:
Terminal:
```
curl -X POST http://localhost:8000/ \
  -F "file=@filename.pdf" \
  -F "question=What is this PDF about?" \
  -F "k=5"
```

Python:
```
import requests

url = "http://localhost:8000/"
files = {
    "file": ("filename.pdf", open("filename.pdf", "rb"), "application/pdf")
}

data = {
    "question": "What is this PDF about?",
    "k": "5"
}

response = requests.post(url, files=files, data=data)

print(response.status_code)
print(response.json())
```
k is the number of top matches returned
