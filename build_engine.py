import os
import json
import datetime
import re
import hashlib
import requests
from bs4 import BeautifulSoup

# 설정 로드
BASE_DIR = "/Users/kimsungwuk/StudioProjects/chloe-blog"
with open(os.path.join(BASE_DIR, "config/settings.json"), "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def get_link_metadata(url):
    try:
        print(f"🔍 링크 데이터 수집 중: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Open Graph 메타데이터 추출
        title_meta = soup.find("meta", property="og:title")
        image_meta = soup.find("meta", property="og:image")
        
        title = title_meta["content"] if title_meta else "Google Play Store"
        image = image_meta["content"] if image_meta else ""
        
        # 제목이 너무 길면 자르기
        if len(title) > 50:
            title = title[:47] + "..."
            
        return {"title": title, "image": image}
    except Exception as e:
        print(f"⚠️ 메타데이터 수집 실패: {e}")
        return {"title": "Google Play Store", "image": ""}

def auto_link_and_format(text):
    # 구글 플레이 스토어 링크 패턴
    url_pattern = r'(https?://play\.google\.com/store/apps/details\?id=[^\s\n<]+)'
    
    def replace_with_rich_preview(match):
        url = match.group(1)
        meta = get_link_metadata(url)
        
        return f"""
        <div class="rich-link-card">
            <a href="{url}" target="_blank">
                <div class="card-image" style="background-image: url('{meta['image']}');"></div>
                <div class="card-body">
                    <div class="card-title">{meta['title']}</div>
                    <div class="card-url">play.google.com</div>
                </div>
            </a>
        </div>
        """

    # 1. 플레이스토어 링크 변환
    text = re.sub(url_pattern, replace_with_rich_preview, text)
    
    # 2. 일반 링크 처리 (이미 변환된 건 제외)
    # (생략: 이번엔 플레이스토어 리치 카드에 집중)
    
    return text.replace('\n', '<br>')

def build_post(title, content, category, summary, image_url, date=None):
    if not date:
        date = datetime.date.today().isoformat()
    
    post_hash = hashlib.md5(title.encode()).hexdigest()[:8]
    filename = f"post-{date}-{post_hash}.html"
    
    image_tag = f'<img src="{image_url}" alt="{title}" style="width:100%; border-radius:18px; margin-bottom:40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">' if image_url else ""
    visitor_badge = f'<img src="https://hits.dwyl.com/kimsungwuk/chloekim/{post_hash}.svg?style=flat-square&color=0066cc" style="margin-bottom:20px;">'

    with open(os.path.join(BASE_DIR, "templates/post_layout.html"), "r", encoding="utf-8") as f:
        template = f.read()
    
    rendered = template.replace("{{title}}", title)\
                       .replace("{{blog_title}}", CONFIG["blog_title"])\
                       .replace("{{author}}", CONFIG["author"])\
                       .replace("{{base_url}}", CONFIG["base_url"])\
                       .replace("{{filename}}", filename)\
                       .replace("{{summary}}", summary or (content[:150] + "..."))\
                       .replace("{{og_image}}", image_url or "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1000")\
                       .replace("{{category}}", category)\
                       .replace("{{date}}", date)\
                       .replace("{{content}}", auto_link_and_format(content))\
                       .replace("{{image_tag}}", image_tag)\
                       .replace("{{visitor_badge}}", visitor_badge)\
                       .replace("{{github_repo}}", CONFIG["github_repo"])

    output_path = os.path.join(BASE_DIR, f"posts/{filename}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    
    return {
        "title": title, "date": date, "category": category,
        "summary": summary or (content[:100] + "..."),
        "image": image_url, "url": f"posts/{filename}"
    }

def rebuild_all():
    data_path = os.path.join(BASE_DIR, "config/posts_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        posts_data = json.load(f)
    
    posts_dir = os.path.join(BASE_DIR, "posts")
    if os.path.exists(posts_dir):
        for f_name in os.listdir(posts_dir):
            if f_name.endswith(".html"):
                os.remove(os.path.join(posts_dir, f_name))
    else:
        os.makedirs(posts_dir)

    processed_posts = []
    for post in posts_data:
        p_info = build_post(post["title"], post["content"], post["category"], post["summary"], post["image_url"], post.get("date"))
        processed_posts.append(p_info)
    
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    start_marker = "const posts = ["
    end_marker = "];"
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        posts_js = "const posts = " + json.dumps(processed_posts, indent=8, ensure_ascii=False)
        new_html = html[:start_idx] + posts_js + html[end_idx + 1:]
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_html)

    print("🚀 [Engine] Rebuilt with Rich Link Preview support.")

if __name__ == "__main__":
    rebuild_all()
