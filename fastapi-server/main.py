from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List
from pydantic import BaseModel

app = FastAPI()

# ✅ SQLite 읽기 전용 (mode=ro)
# DB_PATH = "file:/data/snippets/snippets.db?mode=ro"
DB_PATH = "file:/home/soldesk/learning-mate/bytestash-docker/data/snippets/snippets.db?mode=ro"  # 테스트용 배포때는 지우기

class Snippet(BaseModel):
    id: int
    title: str
    description: str
    updated_at: str

@app.get("/snippets/", response_model=List[Snippet])
def get_snippets():
    conn = sqlite3.connect(DB_PATH, uri=True)
    cursor = conn.cursor()

    # 기본 쿼리
    query = """
        SELECT s.id, s.title, s.description, s.updated_at
        FROM snippets s
    """
    
    # 최신순으로 정렬
    query += " ORDER BY s.updated_at DESC"
    
    # 쿼리 실행
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2] or "",
            "updated_at": row[3]
        } for row in rows
    ]

@app.get("/snippets/{snippet_id}")
def get_snippet_detail(snippet_id: int):
    conn = sqlite3.connect(DB_PATH, uri=True)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.id, s.title, s.description, s.updated_at,
           u.username, f.code, f.language
    FROM snippets s
    LEFT JOIN users u ON s.user_id = u.id
    LEFT JOIN fragments f ON f.snippet_id = s.id
    WHERE s.id = ?
    ORDER BY f.position
    """, (snippet_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Snippet not found")

    first = rows[0]
    return {
        "id": first[0],
        "title": first[1],
        "description": first[2] or "",
        "updated_at": first[3],
        "username": first[4] or "익명",
        "code_blocks": [
            {
                "language": row[6] or "unknown",
                "code": row[5] or ""
            } for row in rows if row[5]
        ]
    }
