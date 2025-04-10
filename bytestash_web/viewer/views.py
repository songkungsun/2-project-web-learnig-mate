import requests
from django.shortcuts import render
from django.conf import settings

API_BASE_URL = settings.SNIPPET_API_URL

def snippet_list(request):
    filter_option = request.GET.get("filter", "all")
    search_query = request.GET.get("q", "")

    try:
        response = requests.get(f"{API_BASE_URL}/snippets/")
        response.raise_for_status()
        snippets = response.json()
    except Exception:
        snippets = []

    if filter_option == "error":
        snippets = [s for s in snippets if "error" in s["title"].lower()]

    if search_query:
        snippets = [
            s for s in snippets
            if search_query.lower() in s["title"].lower()
            or search_query.lower() in s["description"].lower()
        ]

    return render(request, 'snippet_list.html', {
        'snippets': snippets,
        'filter_option': filter_option,
        'search_query': search_query,
    })


def snippet_detail(request, snippet_id):
    try:
        response = requests.get(f"{API_BASE_URL}/snippets/{snippet_id}")
        response.raise_for_status()
        snippet = response.json()
    except Exception:
        snippet = None

    return render(request, 'snippet_detail.html', {
        'snippet': snippet
    })
