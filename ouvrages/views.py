from django.shortcuts import render, redirect, get_object_or_404
from .models import Ouvrage, Categorie
from .forms import OuvrageForm
from django.db.models import Q
# Business Logic

def index(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') != None else ''
    ouvrages = Ouvrage.objects.filter(
        Q(categories__name__icontains=keyword) |
        Q(titre__icontains=keyword) |
        Q(description__icontains=keyword)
    )
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count}
    return render(request, 'ouvrages/index.html', context)

def browse(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') != None else ''
    ouvrages = Ouvrage.objects.filter(
        Q(categories__name__icontains=keyword) |
        Q(titre__icontains=keyword) |
        Q(description__icontains=keyword)
    )
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count}
    return render(request, 'ouvrages/browse-ouvrages.html', context)

def topicsDetail(request):
    return render(request, 'ouvrages/topics-detail.html')

def topicsListing(request):
    return render(request, 'ouvrages/topics-listing.html')

def contact(request):
    return render(request, 'ouvrages/contact.html')

def home(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') != None else ''
    ouvrages = Ouvrage.objects.filter(
        Q(categories__name__icontains=keyword) |
        Q(titre__icontains=keyword) |
        Q(description__icontains=keyword)
    )          
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count}
    return render(request, 'ouvrages/home.html', context)
    
def ouvrages(request):
    ouvrages = Ouvrage.objects.all()
    context = {'ouvrages': ouvrages}
    return render(request, 'ouvrages/ouvrages.html', context)

#whatever we name the parameter here <str:pk> we should name it here :
def ouvrage(request, pk):
    ouvrageObj = Ouvrage.objects.get(id=pk)
    #categories = ouvrageObj.categories.all()
    context = {'ouvrage': ouvrageObj}
    return render(request, 'ouvrages/single-ouvrage.html', context)

def createOuvrage(request):
    form = OuvrageForm()
    if request.method == 'POST':
        form = OuvrageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ouvrages')
    context = {'form': form}
    return render(request, 'ouvrages/ouvrage_form.html', context)

def updateOuvrage(request, pk):
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    form = OuvrageForm(instance=ouvrage)
    if request.method == 'POST':
        form = OuvrageForm(request.POST, request.FILES ,instance=ouvrage)
        if form.is_valid():
            form.save()
            return redirect('ouvrages')
    context = {'form': form}
    return render(request, 'ouvrages/ouvrage_form.html', context)

def deleteOuvrage(request, pk):
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        ouvrage.delete()
        return redirect('ouvrages')
    # If the request is not POST, render the confirmation page
    context = {'ouvrage': ouvrage}
    return render(request, 'ouvrages/delete_ouvrage.html', context)
