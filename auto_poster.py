import os
import datetime
import re

def create_post(title, content, category="AI를 활용한 개발정보", summary="", image_url=""):
    base_dir = "/Users/kimsungwuk/StudioProjects/chloe-blog"
    posts_dir = os.path.join(base_dir, "posts")
    
    # 0. 날짜 정의
    today = datetime.date.today().isoformat()
    
    # 1. 파일 이름 생성 (특수문자 제거 및 슬래시 처리)
    safe_title = re.sub(r'[^\w\s-]', '', title.replace('/', '-')).strip()
    filename = f"{today}-{safe_title.replace(' ', '-').lower()}.html"
    filepath = os.path.join(posts_dir, filename)
    
    # 이미지 태그 생성
    image_tag = f'<img src="{image_url}" alt="{title}" style="width:100%; border-radius:18px; margin-bottom:40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">' if image_url else ""
    
    # 방문자 카운터 배지 생성
    visitor_badge = f'<img src="https://hits.dwyl.com/kimsungwuk/chloekim/{filename}.svg?style=flat-square&color=0066cc" style="margin-bottom:20px;">'

    # 2. HTML 템플릿 작성 (Apple 디자인 스타일 적용 + Giscus 고정)
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Chloe Dev Log</title>
    <style>
        :root {{ --bg-color: #ffffff; --text-primary: #1d1d1f; --text-secondary: #86868b; --accent-color: #0066cc; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif; background-color: var(--bg-color); color: var(--text-primary); margin: 0; padding: 0; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 80px 20px; }}
        .meta {{ font-size: 14px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 8px; }}
        h1 {{ font-size: 48px; font-weight: 700; letter-spacing: -0.015em; margin: 0 0 10px 0; line-height: 1.1; }}
        .content {{ font-size: 21px; font-weight: 400; letter-spacing: -0.01em; color: #333; }}
        .back-link {{ display: block; margin-top: 60px; text-decoration: none; color: var(--accent-color); font-weight: 500; font-size: 17px; }}
        .comment-section {{ margin-top: 80px; padding-top: 40px; border-top: 1px solid #e5e5e5; }}
    </style>
</head>
<body>
<div class="container">
    <div class="meta">{category} · {today}</div>
    <h1>{title}</h1>
    {visitor_badge}
    {image_tag}
    <div class="content">
        {content.replace('\n', '<br>')}
    </div>

    <div class="comment-section">
        <script src="https://giscus.app/client.js"
                data-repo="kimsungwuk/chloekim"
                data-repo-id="R_kgDORUWviQ"
                data-category="General"
                data-category-id="DIC_kwDORUWvic4C206U"
                data-mapping="pathname"
                data-strict="0"
                data-reactions-enabled="1"
                data-emit-metadata="0"
                data-input-position="bottom"
                data-theme="preferred_color_scheme"
                data-lang="ko"
                crossorigin="anonymous"
                async>
        </script>
    </div>

    <a href="../index.html" class="back-link">← 모든 포스팅 보기</a>
</div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    # 3. index.html 업데이트 (자동으로 posts 배열에 추가)
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content_index = f.read()

    new_post_json = f"""{{
            title: "{title}",
            date: "{today}",
            category: "{category}",
            summary: "{summary or (content[:100] + '...')}",
            image: "{image_url}",
            url: "posts/{filename}"
        }},"""
    
    # posts 배열의 시작 부분에 삽입
    if new_post_json not in content_index:
        updated_index = content_index.replace("const posts = [", f"const posts = [\n        {new_post_json}")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(updated_index)

    print(f"💰 [성공] 새 포스팅 생성 및 인덱스 업데이트 완료: {filename}")
    return filename

if __name__ == "__main__":
    pass
