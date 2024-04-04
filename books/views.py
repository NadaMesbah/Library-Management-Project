from django.shortcuts import render

# Create your views here.
booksList = [
    {
        'id': '1',
        'title': 'Python Book',
        'description': 'Full Python Guide'
    },
    {
        'id': '2',
        'title': 'Django Book',
        'description': 'A personal guide to learn django'
    },
    {
        'id': '3',
        'title': 'Computer Vision Book',
        'description': 'An open source book for computer vision'
    }
]

def books(request):
    context = {'books': booksList}
    return render(request, 'books/books.html', context)

def book(request, pk):
    bookObj = None
    for i in booksList:
        if i['id'] == str(pk):
            bookObj = i
    context = {'book': bookObj}
    return render(request, 'books/single-book.html', context)