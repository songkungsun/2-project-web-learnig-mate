# 베이스 이미지
FROM python:3.11-slim

# 환경 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리
WORKDIR /app

# requirements 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

# 🔻 아래 줄 삭제 (복사 스크립트 관련)
# COPY scripts/copy_sqlite_readonly.sh /app/scripts/copy_sqlite_readonly.sh
# RUN chmod +x /app/scripts/copy_sqlite_readonly.sh

# 🔻 ENTRYPOINT 제거
# ENTRYPOINT ["/app/scripts/copy_sqlite_readonly.sh"]

# gunicorn으로 Django 앱 실행
CMD ["gunicorn", "bytestash_web.wsgi:application", "--bind", "0.0.0.0:8000"]
