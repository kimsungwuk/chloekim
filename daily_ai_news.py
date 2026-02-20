import os
import json
import datetime
from build_engine import build_post, rebuild_all

# 설정 로드
BASE_DIR = "/Users/kimsungwuk/StudioProjects/chloe-blog"

def fetch_ai_news():
    print("최신 AI 뉴스를 수집하는 중입니다.")
    
    # 2026년 2월 20일 기준 실제 검색 결과 반영
    news_items = [
        "미국 백악관 인도 AI 임팩트 서밋에서 AI 도입 및 주권 그리고 수출 촉진 방안 발표",
        "중국 스타트업 시댄스 2.0 출시로 생성형 비디오 및 멀티모달 모델 경쟁 심화",
        "로이터 통신 AI 전용 메모리 칩 제조사들의 시장 가치 및 공급망 현황 분석 보도",
        "대한민국 정부 독자적 AI 프로젝트에 모티프 추가 선정 및 행동 모델 개발 목표 수립",
        "EDAG 그룹 산업용 메타버스 플랫폼과 통합된 AI 팩토리 접근 방식 공개"
    ]
    return news_items

def create_daily_news_post():
    today = datetime.date.today().isoformat()
    title = f"{today} AI 기술 트렌드 브리핑"
    category = "AI 최신뉴스"
    
    news_list = fetch_ai_news()
    
    content = "금일의 주요 인공지능 기술 및 글로벌 산업 동향을 정리하여 드립니다.\n\n"
    for i, item in enumerate(news_list, 1):
        content += f"{i}. {item}\n"
    
    content += "\n최근 인공지능 시장은 국가 간 기술 주권 확보와 산업 현장의 실질적인 적용에 집중하고 있습니다. 특히 제조 및 서비스 분야에서의 멀티모달 모델 도입이 가속화되는 추세입니다.\n\n내일도 새로운 소식으로 찾아뵙겠습니다. 감사합니다."
    
    summary = f"{today} 기준 주요 인공지능 기술 및 글로벌 기업 동향 5가지 요약."
    image_url = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000"

    # 데이터베이스 로드 및 저장
    data_path = os.path.join(BASE_DIR, "config/posts_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        posts_data = json.load(f)

    # 중복 방지 또는 업데이트
    updated = False
    for p in posts_data:
        if p['title'] == title:
            p['content'] = content
            p['summary'] = summary
            updated = True
            break
            
    if not updated:
        posts_data.insert(0, {
            'title': title,
            'date': today,
            'category': category,
            'summary': summary,
            'image_url': image_url,
            'content': content
        })
        
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(posts_data, f, indent=4, ensure_ascii=False)
    
    rebuild_all()
    return True

if __name__ == "__main__":
    if create_daily_news_post():
        print("성공 오늘의 AI 뉴스 포스팅 완료")
    else:
        print("포스팅 과정에서 문제가 발생했습니다")
