from django.shortcuts import render, redirect, get_object_or_404
from .models import Ouvrage
from .forms import OuvrageForm
# Business Logic

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
        form = OuvrageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ouvrages')
    context = {'form': form}
    return render(request, 'ouvrages/ouvrage_form.html', context)

def updateOuvrage(request, pk):
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    form = OuvrageForm(instance=ouvrage)
    if request.method == 'POST':
        form = OuvrageForm(request.POST, instance=ouvrage)
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