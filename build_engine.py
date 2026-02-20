import os
import json
import datetime
import re
import hashlib

# 설정 로드
BASE_DIR = "/Users/kimsungwuk/StudioProjects/chloe-blog"
with open(os.path.join(BASE_DIR, "config/settings.json"), "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def build_post(title, content, category, summary, image_url, date=None):
    if not date:
        date = datetime.date.today().isoformat()
    
    post_hash = hashlib.md5(title.encode()).hexdigest()[:12]
    filename = f"post-{date}-{post_hash}.html"
    
    # 이미지 태그
    image_tag = f'<img src="{image_url}" alt="{title}" style="width:100%; border-radius:18px; margin-bottom:40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">' if image_url else ""
    
    # 방문자 카운터 배지
    visitor_badge = f'<img src="https://hits.dwyl.com/kimsungwuk/chloekim/{post_hash}.svg?style=flat-square&color=0066cc" style="margin-bottom:20px;">'

    # 템플릿 로드
    with open(os.path.join(BASE_DIR, "templates/post_layout.html"), "r", encoding="utf-8") as f:
        template = f.read()
    
    # 변수 치환
    rendered = template.replace("{{title}}", title)\
                       .replace("{{blog_title}}", CONFIG["blog_title"])\
                       .replace("{{category}}", category)\
                       .replace("{{date}}", date)\
                       .replace("{{content}}", content.replace('\n', '<br>'))\
                       .replace("{{image_tag}}", image_tag)\
                       .replace("{{visitor_badge}}", visitor_badge)\
                       .replace("{{github_repo}}", CONFIG["github_repo"])\
                       .replace("{{post_id}}", post_hash)\
                       .replace("{{g_repo_id}}", CONFIG["giscus"]["repo_id"])\
                       .replace("{{g_category}}", CONFIG["giscus"]["category"])\
                       .replace("{{g_category_id}}", CONFIG["giscus"]["category_id"])\
                       .replace("{{g_mapping}}", CONFIG["giscus"]["mapping"])\
                       .replace("{{g_reactions}}", CONFIG["giscus"]["reactions_enabled"])\
                       .replace("{{g_theme}}", CONFIG["giscus"]["theme"])\
                       .replace("{{g_lang}}", CONFIG["giscus"]["lang"])

    # 파일 저장
    output_path = os.path.join(BASE_DIR, f"posts/{filename}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    
    return {
        "title": title,
        "date": date,
        "category": category,
        "summary": summary or (content[:100] + "..."),
        "image": image_url,
        "url": f"posts/{filename}"
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
        p_info = build_post(
            post["title"], 
            post["content"], 
            post["category"], 
            post["summary"], 
            post["image_url"],
            post.get("date")
        )
        processed_posts.append(p_info)
    
    # Update index.html
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

    print("🚀 [Engine] Site rebuilt with General category and dynamic settings.")

if __name__ == "__main__":
    rebuild_all()
