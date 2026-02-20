import os
import datetime

def create_post(title, content):
    base_dir = "/Users/kimsungwuk/StudioProjects/chloe-blog"
    posts_dir = os.path.join(base_dir, "posts")
    
    # 1. 파일 이름 생성
    today = datetime.date.today().isoformat()
    filename = f"{today}-{title.replace(' ', '-').lower()}.html"
    filepath = os.path.join(posts_dir, filename)
    
    # 2. HTML 템플릿 작성 (Apple 디자인 스타일 적용)
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
        h1 {{ font-size: 48px; font-weight: 700; letter-spacing: -0.015em; margin: 0 0 40px 0; line-height: 1.1; }}
        .content {{ font-size: 21px; font-weight: 400; letter-spacing: -0.01em; color: #333; }}
        .back-link {{ display: block; margin-top: 60px; text-decoration: none; color: var(--accent-color); font-weight: 500; font-size: 17px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="meta">{today}</div>
    <h1>{title}</h1>
    <div class="content">
        {content.replace('\n', '<br>')}
    </div>
    <a href="../index.html" class="back-link">← 모든 포스팅 보기</a>
</div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"💰 [성공] 새 포스팅 생성 완료: {filename}")
    return filename

if __name__ == "__main__":
    # 나중에 내가 이 함수를 호출해서 글을 쓸 거야!
    pass
