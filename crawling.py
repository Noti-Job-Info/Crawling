import requests

import pprint


def crawl_data(limit=100, offset=0):
    url = 'https://www.wanted.co.kr/api/v4/jobs?' # Wanted Job API URL

    # tag_type_ids=10110&  # 소프트웨어 엔지니어
    # tag_type_ids=873&  # 웹 개발자
    # tag_type_ids=872&  # 서버 개발자
    # tag_type_ids=899&  # 파이썬 개발자
    
    # skill_tags=1554&  # python
    # skill_tags=1444&  # django
    # skill_tags=1452&  # flask
    # skill_tags=10291&  # fastapi
    # skill_tags=2217  # docker
        
    params ={
        'country': 'kr',
        'tag_type_ids': [10110, 873, 872, 899], # 직무
        'skill_tags': [1554, 1444, 1452, 10291, 2217], # 기술스택
        'job_sort': 'job.latest_order', # 최신순 정렬
        'locations': 'all',
        'years': 0, # 경력 이상 경력상관없이 검색하려면 -1 , 신입은0
        'years': 2, # 경력 이하 경력상관없이 검색하려면 -1 , 신입은0
        'limit': limit,    # 한 번에 조회 가능한 수 (최대100)
        'offset': offset     # 조회할 게시물의 첫 index  ex) limit=100 offset=10  => 10번게시물부터 110번게시물까지 크롤링
    }
    req = requests.get(url, params=params)
    
    req_json_data = req.json()
    
    return filtering_data(req_json_data)

    
def filtering_data(req_json_data):
    '''크롤링 데이터 필터링
    company 
        id, industry_name, name #회사 아이디, 산업 이름, 회사 이름
    due_time # 공고 마감 기한
    id # 공고 아이디
    address # 주소
    position #포지션 이름
    category_tag #직무    
    detail_url: https://www.wanted.co.kr/wd/{int:detail_id} #상세 페이지 URL
    '''
    formatted_data = dict()
    
    if not req_json_data:
        return None
    
    for data in req_json_data['data']:
        job_id = data['id']
        company_id = data['company'].get('id')
        industry_name = data['company'].get('industry_name')
        company_name = data['company'].get('name')
        due_time = data['due_time']
        address_location = data['address']['location']
        position = data['position']
        category_tags = data['category_tags']
        
        formatted_data[job_id] = dict()

        formatted_data[job_id]['company'] = dict()
        formatted_data[job_id]['company']['id'] = company_id
        formatted_data[job_id]['company']['industry_name'] = industry_name
        formatted_data[job_id]['company']['name'] = company_name
        
        formatted_data[job_id]['address'] = address_location
        formatted_data[job_id]['due_time'] = due_time
        formatted_data[job_id]['position'] = position
        formatted_data[job_id]['category_tags'] = category_tags
        formatted_data[job_id]['wanted_detail_page_url'] = f'https://www.wanted.co.kr/wd/{job_id}'
        
        pprint.pprint(formatted_data)


def crawl_all_data(limit=100, offset=0):
    try:
        while True:
            crawl_data(limit, offset)
            offset += limit
    except:
        if limit != 1:
            return crawl_all_data(limit/10, offset)

pprint.pprint(crawl_all_data())
