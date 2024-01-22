from django.shortcuts import render
from django import forms
from . import util
from django.contrib import messages


class NewPageForm(forms.Form):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': "Title of New Page", "autofocus": "true"}))
    content = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Enter Markdown Content for the new page...'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    
def search_results(request):
    results = None
    if request.method == "POST":
        query = request.POST["q"]
        if len(query) == 0:
             return render(request, "encyclopedia/search_results.html", {
                "results": results
            })

        entries = util.list_entries()
        for entry in entries:
            if query.upper() == entry.upper():
                content = util.get_entry(entry)
                return render(request, "encyclopedia/entry.html", {
                    "title": entry,
                    "content": content
                })
        
        for entry in entries:
            results = [entry for entry in entries if query.upper() in entry.upper()]
            return render(request, "encyclopedia/search_results.html", {
                "results": results
            })
    else: 
         return render(request, "encyclopedia/search_results.html", {
                "results": results
            })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": content
                })
            else: 
                messages.error(request, "A page with this title already exists.")
                #form.add_error("title", "A page with this title already exists.")
                return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })

