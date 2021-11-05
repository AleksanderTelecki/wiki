from logging import PlaceHolder
from random import random
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from markdown2 import Markdown
import random

from . import util

class NewForm(forms.Form):
    title = forms.CharField(max_length=40,label="",widget=forms.TextInput(attrs={"placeholder": "Title","class": "form-control"}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":24,"placeholder": "Description","class": "form-control"}))
    check = forms.BooleanField(required=False)



def index(request):
    if request.GET.get('q',''):
        return searchValue(request)
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "name": "All page"
    })




def findEntries(name):
    stringList = []
 
    for entry in util.list_entries():
        if entry.lower().find(name.lower()) != -1:
            stringList.append(entry)
    
    return stringList

def searchValue(request):
    searchedValue = request.GET.get('q','')
    if searchedValue.lower() not in util.list_entries_lowercase():

        findedValues = findEntries(searchedValue)
        if len(findedValues) != 0:
            return render(request, "encyclopedia/index.html", {
                "entries": findedValues,
                "name": "Maybe you looking for:"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": findedValues,
                "name": "Page not found 404"
            })

    else:
        entryName = util.list_entries()[util.list_entries_lowercase().index(searchedValue.lower())]
        url = reverse('showEntry', kwargs={'entryName': entryName })
        return HttpResponseRedirect(url)







def showEntry(request, entryName):

    if request.GET.get('q',''):
        return searchValue(request)


    markdowner = Markdown()

    if  entryName in util.list_entries():
        html = markdowner.convert(util.get_entry(entryName))
    else:
        html = markdowner.convert("# Page not found 404")

    return render(request, "encyclopedia/entries.html", {
        "html": html,
        "name":entryName
    })

def newPage(request):


    if request.GET.get('q',''):
        return searchValue(request)

    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            util.save_entry(title,description)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"encyclopedia/newpage.html",{
                "form":form
            })

    return render(request,"encyclopedia/newpage.html",{
        "form": NewForm()

    })

def editPage(request,entryName):


    if request.GET.get('q',''):
        return searchValue(request)




    if request.method == "POST":
        form = NewForm(request.POST)

       #TODO: Add deletion
       # if request.POST.get('check', True):
       #     util.delete_entry(entryName)
        #    return HttpResponseRedirect(reverse("index"))

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            util.save_entry(title,description)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"encyclopedia/editpage.html",{
                "form":form,
                "entryName":entryName
            })

    entry = util.get_entry(entryName)
    form = NewForm(initial={'title': entryName,'description':entry})
   
    return render(request,"encyclopedia/editpage.html",{
        "form": form,
        "entryName":entryName

    })

def RandomPage(request):
    entryName = random.choice(util.list_entries())
    url = reverse('showEntry', kwargs={'entryName': entryName })
    return HttpResponseRedirect(url)





