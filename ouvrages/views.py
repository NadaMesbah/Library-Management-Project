from django.shortcuts import render, redirect, get_object_or_404
from .models import Ouvrage, Categorie, Exemplaire
from .forms import OuvrageForm, ExemplaireForm
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
    best_ouvrage = Ouvrage.objects.exclude(vote_total=0).order_by('-vote_ratio').first()
    newest_ouvrage = Ouvrage.objects.order_by('-date_achat').first()
    recommended_ouvrages = Ouvrage.objects.filter(recommended=True)
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count, 'best_ouvrage' : best_ouvrage, 
               'newest_ouvrage': newest_ouvrage , 'recommanded_ouvrages' : recommended_ouvrages}
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
 
## CRUD FOR OUVRAGES   
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
            return redirect('ouvrages:ouvrages')
    context = {'form': form}
    return render(request, 'ouvrages/ouvrage_form.html', context)

def updateOuvrage(request, pk):
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    form = OuvrageForm(instance=ouvrage)
    if request.method == 'POST':
        form = OuvrageForm(request.POST, request.FILES ,instance=ouvrage)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:ouvrages')
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

## CRUD FOR EXEMPLAIRES
def exemplaires(request):
    exemplaires = Exemplaire.objects.all()
    context = {'exemplaires': exemplaires}
    return render(request, 'ouvrages/exemplaires.html', context)

def exemplaire(request, pk):
    exemplaireObj = Exemplaire.objects.get(id=pk)
    context = {'exemplaire': exemplaireObj}
    return render(request, 'ouvrages/single-exemplaire.html', context)

def createExemplaire(request):
    form = ExemplaireForm()
    if request.method == 'POST':
        form = ExemplaireForm(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            ouvrage_instance = form.cleaned_data['ouvrage']

            exemplaires_data = [
                {'ouvrage': ouvrage_instance,
                 'etat': form.cleaned_data['etat'],
                 'emprunte': form.cleaned_data['emprunte'],
                 'reserve': form.cleaned_data['reserve']}
                for _ in range(quantite)
            ]
            
            Exemplaire.objects.bulk_create([Exemplaire(**data) for data in exemplaires_data])
            return redirect('ouvrages:exemplaires')
    context = {'form': form}
    return render(request, 'ouvrages/exemplaire_form.html', context)

def updateExemplaire(request, pk):
    exemplaire = get_object_or_404(Exemplaire, id=pk)
    form = ExemplaireForm(instance=exemplaire)
    if request.method == 'POST':
        form = ExemplaireForm(request.POST ,instance=exemplaire)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:exemplaires')
    context = {'form': form}
    return render(request, 'ouvrages/exemplaire_form.html', context)

def deleteExemplaire(request, pk):
    exemplaire = get_object_or_404(Exemplaire, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        exemplaire.delete()
        return redirect('ouvrages:exemplaires')
    # If the request is not POST, render the confirmation page
    context = {'exemplaire': exemplaire}
    return render(request, 'ouvrages/delete_exemplaire.html', context)