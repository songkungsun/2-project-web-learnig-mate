import requests
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Comment
from .forms import CommentForm
from .models import ResolvedSnippet

# # API_BASE_URL = getattr(settings, "SNIPPET_API_URL", "http://api.tripk.net")
API_BASE_URL = "http://localhost:8001"  # 테스트용, 배포 시 설정 파일에서 가져오기

def snippet_list(request):
    filter_option = request.GET.get("filter", "all")
    search_query = request.GET.get("q", "")

    try:
        response = requests.get(f"{API_BASE_URL}/snippets/")
        response.raise_for_status()
        snippets = response.json()
    except Exception:
        snippets = []

    # 해결된 스니펫 ID 가져오기 (ResolvedSnippet에 저장된 snippet_id)
    resolved_ids = set(ResolvedSnippet.objects.values_list('snippet_id', flat=True))

    # 필터링 옵션 적용
    if filter_option == "error":
        snippets = [s for s in snippets if "error" in s["title"].lower()]
    elif filter_option == "resolved":
        # 해결된 코드만 필터링 (ResolvedSnippet에 있는 snippet_id와 매칭)
        snippets = [s for s in snippets if s["id"] in resolved_ids]

    # 검색어로 필터링
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
    # ByteStash에서 API로 가져오기
    try:
        response = requests.get(f"{API_BASE_URL}/snippets/{snippet_id}")
        response.raise_for_status()
        snippet = response.json()
    except requests.exceptions.RequestException:
        snippet = None

    # 댓글 가져오기
    comments = Comment.objects.filter(snippet_id=snippet_id).order_by('-created_at')
    
    # 해결된 스니펫 상태 체크
    is_resolved = ResolvedSnippet.objects.filter(snippet_id=snippet_id).exists()

    # 댓글 작성 처리
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.snippet_id = snippet_id
            comment.save()
            return redirect('snippet_detail', snippet_id=snippet_id)

        # 해결 버튼 처리
        elif 'resolve' in request.POST:
            # 스니펫을 해결됨으로 마크
            try:
                ResolvedSnippet.objects.get_or_create(snippet_id=snippet_id)
            except Exception as e:
                print(f"Error resolving snippet: {e}")  # 에러 로그 확인
                raise
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = CommentForm()

    return render(request, 'snippet_detail.html', {
        'snippet': snippet,
        'comments': comments,
        'form': form,
        'is_resolved': is_resolved,
    })