import requests
from django.shortcuts import render

def snippet_list(request):
    response = requests.get("http://localhost:8000/snippets/")
    snippets = response.json()

    # 필터링
    filter_option = request.GET.get("filter", "all")
    if filter_option == "error":
        snippets = [s for s in snippets if "error" in s["title"].lower()]

    return render(request, 'snippet_list.html', {
        'snippets': snippets,
        'filter_option': filter_option,
    })

def snippet_detail(request, snippet_id):
    try:
        response = requests.get(f"http://localhost:8000/snippets/{snippet_id}")
        snippet = response.json()
    except Exception as e:
        snippet = None

    return render(request, 'snippet_detail.html', {
        'snippet': snippet
    })


