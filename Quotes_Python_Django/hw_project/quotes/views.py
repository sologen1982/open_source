from bson import ObjectId
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from pymongo import MongoClient
from .forms import AuthorForm, QuoteForm
# from .models import Author, Quote

# Create your views here.
from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author_data = form.cleaned_data
            db = get_mongodb()
            db.authors.insert_one({
                'fullname': author_data['fullname'],
                'born_date': author_data['born_date'].isoformat(),
                'born_location': author_data['born_location'],
                'description': author_data['description']
            })
            return redirect('quotes:root')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_data = form.cleaned_data
            db = get_mongodb()

            author = quote_data['author']

            author_document = db.authors.find_one({'fullname': author.fullname})
            if not author_document:
                # Add the author to the database if it doesn't exist
                author_document = db.authors.insert_one({
                    'fullname': author.fullname,
                    'born_date': author.born_date.isoformat(),
                    'born_location': author.born_location,
                    'description': author.description
                })

            # Insert the quote into the database
            db.quotes.insert_one({
                'quote': quote_data['quote'],
                'author': ObjectId(author_document['_id']),
                'tags': quote_data['tags'].split(',')
            })
            return redirect('quotes:root')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def author_detail(request, fullname):
    db = get_mongodb()
    author_document = db.authors.find_one({'fullname': fullname})
    if not author_document:
        raise Http404("Author does not exist")

    author_data = {
        'fullname': author_document['fullname'],
        'born_date': author_document['born_date'],
        'born_location': author_document['born_location'],
        'description': author_document['description']
    }

    return render(request, 'quotes/author_detail.html', {'author': author_data})
