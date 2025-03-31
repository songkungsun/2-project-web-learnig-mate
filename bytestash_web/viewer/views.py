import requests
from django.shortcuts import render

def snippet_list(request):
    response = requests.get("http://localhost:8000/snippets/")
    snippets = response.json()

    filter_option = request.GET.get("filter", "all")
    search_query = request.GET.get("q", "")

    # error 필터
    if filter_option == "error":
        snippets = [s for s in snippets if "error" in s["title"].lower()]

    # 검색 필터
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
        response = requests.get(f"http://localhost:8000/snippets/{snippet_id}")
        snippet = response.json()
    except Exception:
        snippet = None

    return render(request, 'snippet_detail.html', {
        'snippet': snippet
    })
