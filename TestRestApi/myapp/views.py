from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    if request.method == 'POST':
        url = "http://localhost:8000/api/books"
        querystring = { "title": request.POST.get('title', ''),
                        "author": request.POST.get('author', ''),
                        "isbn": request.POST.get('isbn', ''),
                        "publisher": request.POST.get('publisher', '')
                    }
        response = requests.post(url, data=querystring)
        print(response)
        msg = "Book added successfully!"
        response = requests.get(url)
        data = response.json()
        return render(request, 'index.html', {'books': data, 'msg': msg})

    else:
        url = "http://localhost:8000/api/books"
        response = requests.get(url)
        data = response.json()
        return render(request, 'index.html', {'books': data})