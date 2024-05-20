from .models import Ouvrage, Categorie, Exemplaire, Review
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateOuvrages(request, ouvrages, results):

    page = request.GET.get('page')
    paginator = Paginator(ouvrages, results)

    try:
        ouvrages = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        ouvrages = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        ouvrages = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, ouvrages

def paginateExemplaires(request, exemplaires, results):

    page = request.GET.get('page')
    paginator = Paginator(exemplaires, results)

    try:
        exemplaires = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        exemplaires = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        exemplaires = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, exemplaires

def paginateReviews(request, reviews, results):

    page = request.GET.get('page')
    paginator = Paginator(reviews, results)

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        reviews = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        reviews = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, reviews

def searchOuvrages(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    categories = Categorie.objects.filter(name__icontains=search_query)

    ouvrages = Ouvrage.objects.distinct().filter(
        Q(categories__name__icontains=search_query) |
        Q(titre__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(auteurs__nomComplet__icontains=search_query)|
        Q(categories__in=categories)
    )
    return ouvrages, search_query

def searchExemplaires(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    exemplaires = Exemplaire.objects.distinct().filter(
        Q(ouvrage__titre__icontains=search_query) |
        Q(ouvrage__description__icontains=search_query) |
        Q(ouvrage__auteurs__nomComplet__icontains=search_query) |
        Q(id__icontains=search_query) 
    )
    return exemplaires, search_query
