import os, time, random, string, json, requests, pymysql, re, io
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, send_file
from pyngrok import ngrok
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import vision
import xml.etree.ElementTree as ET
from datetime import datetime


app = Flask(__name__)


def get_db_connection():
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#버블 DB 서버 채용 공고 등록
def bubble_job_post(user_id, job_id, pay_type, pay_min, pay_max, welfare, duedate, always):
    bubble_param = {
    'user_id': user_id,
    'job_id': job_id,
    'pay_type': pay_type,
    'pay_min': pay_min,
    'pay_max': pay_max,
    'welfare': welfare,
    'always': always,
    'duedate': duedate
    }
    BUBBLE_HEADERS = {
        'Authorization': f'Bearer {BUBBLE_KEY}',
        'Content-Type': 'application/json'
    }
    BUBBLE_API_URL = "https://koreaandme.bubbleapps.io/version-test/api/1.1/wf/job_post"
    response = requests.post(BUBBLE_API_URL, headers=BUBBLE_HEADERS, json = bubble_param)

    return jsonify({"message": "Data updated successfully"})

# Ensure the code runs within the app context

def process_date(input_text):
    # Initialize variables
    always = '아니오'
    duedate = None

    # Check if the input text contains "채용시까지"
    if "채용시까지" in input_text:
        always = '네'
        # Extract the date portion
        date_str = input_text.split(" ")[-1]
    else:
        date_str = input_text

    # Parse the date to datetime object
    try:
        date_obj = datetime.strptime(date_str, "%y-%m-%d")
        # Format the date as "Sep 14, 2024 12:00 pm"
        duedate = date_obj.strftime("%b %d, %Y 12:00 pm")
    except ValueError:
        raise ValueError("Invalid date format provided. Please use 'yy-mm-dd'.")

    return always, duedate


kakao_api_key = "ceae25b694002a3b0ee820bcd5952654"  # API 키를 문자열로 입력
def get_lat_lon(address, kakao_api_key):
    url = "https://dapi.kakao.com/v2/local/search/address.json"

    # Authorization 헤더와 KA 헤더를 함께 설정
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}",
    }

    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['documents']:
            lat = data['documents'][0]['y']
            lon = data['documents'][0]['x']
            return lat, lon
        else:
            return None
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def bubble_job_post(user_id, job_id, pay_type, pay_min, pay_max, welfare, always, duedate):
    bubble_param = {
    'user_id': user_id,
    'job_id': job_id,
    'welfare': welfare,
    'pay_type': pay_type,
    'pay_min': pay_min,
    'pay_max': pay_max,
    'always': always,
    'duedate': duedate
    }
    BUBBLE_KEY = "17451d9face39e057919c9f0a13a694e"
    BUBBLE_HEADERS = {
        'Authorization': f'Bearer {BUBBLE_KEY}',
        'Content-Type': 'application/json'
    }
    BUBBLE_API_URL = "https://koreaandme.bubbleapps.io/version-test/api/1.1/wf/job_post"
    try:
        response = requests.post(BUBBLE_API_URL, headers=BUBBLE_HEADERS, json=bubble_param)

        # Check if the request was successful
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    return jsonify({"message": "Data updated successfully"})



def extract_working_hours(input_string):
    # 한국어 시간 형식에서 시간을 추출하기 위한 정규 표현식
    match = re.search(r'(\(?오전\)?|\(?오후\)?)\s*(\d{1,2})\s*시\s*(\d{1,2})\s*분\s*~\s*(\(?오전\)?|\(?오후\)?)\s*(\d{1,2})\s*시\s*(\d{1,2})\s*분', input_string)

    if match:
        start_period, start_hour, start_minute, end_period, end_hour, end_minute = match.groups()

        # 오전/오후 처리
        if '오전' in start_period or '(오전)' in start_period:
            start_time = f"AM {int(start_hour):02}:{int(start_minute):02}"
        else:
            start_time = f"PM {int(start_hour):02}:{int(start_minute):02}"

        if '오후' in end_period or '(오후)' in end_period:
            end_time = f"PM {int(end_hour):02}:{int(end_minute):02}"
        else:
            end_time = f"AM {int(end_hour):02}:{int(end_minute):02}"

        return f"{start_time} ~ {end_time}"

    return None


def split_job_input(job_input):
    # 마지막 괄호의 위치를 찾음
    last_open_paren = job_input.rfind('(')
    last_close_paren = job_input.rfind(')')

    # 마지막 괄호 안에 있는 것을 코드로 간주
    job_code = job_input[last_open_paren + 1:last_close_paren].strip()

    # 마지막 괄호 이전의 텍스트는 직업 텍스트로 간주
    job_text = job_input[:last_open_paren].strip()

    return job_text, job_code


#채용정보 개별 가공 및 번역
def each_post(authNo, item) :
    params_detail = {
      "authKey": worknet_key,
      "callTp": "D",
      "returnType": "XML",
      "wantedAuthNo" : authNo,
      "infoSvc" : "VALIDATION"
    }

    able = True;
    job_id = 0

    details = requests.get(worknet_url, params=params_detail) # 채용디테일 불러오기 (detail = 상세정보, item = 기본정보)
    details = ET.fromstring(details.content)
    detail = details.find(".//contactTelno").text if details.find(".//contactTelno") is not None else "N/A"
    print(detail)
    print(authNo)


    company = item.find('company').text if item.find('company') is not None else "N/A"

    user_id = 1;
    print("사용자번호 : " + str(user_id))

    c_no = item.find('busino').text if item.find('busino') is not None else "N/A"
    print("사업자번호 : " + c_no)

    c_name = item.find('company').text if item.find('company') is not None else "N/A"
    print("사업자명 : " + c_name)

    p_name = ''
    p_phone = details.find('.//contactTelno').text if details.find('.//contactTelno') is not None else "N/A"
    print("담당연락처 : " + str(p_phone))

    industry = details.find('.//indTpCdNm').text if details.find('.//indTpCdNm') is not None else "N/A"
    print("업종 : " + industry)

    size=details.find('.//totPsncnt').text if details.find('.//totPsncnt') is not None else "N/A"
    size = int(size.split(" ")[0])
    size_text = ""
    if size <= 5 :
        size_text = "1~5명"
    elif size <= 10 :
        size_text = "6~10명"
    elif size <= 50 :
        size_text = "11~50명"
    elif size <= 100 :
        size_text = "51~100명"
    elif size <= 150 :
        size_text = "101~150명"
    elif size <= 200 :
        size_text = "151~200명"
    elif size <= 300 :
        size_text = "201~300명"
    else :
        size_text = "301명 이상"
    print("직원수 : " + size_text)

    corp3 = ""
    corp_address=details.find('.//corpAddr').text if details.find('.//corpAddr') is not None else "N/A"
    print("회사주소 : " + corp_address)
    split_list = corp_address.split(' ', 1)
    corp1 = split_list[0]
    split_list = split_list[1].split(',', 1)
    corp2 = split_list[0].strip()
    if len(split_list) > 1 and split_list[1].strip():
        corp3 = split_list[1].strip()
    else :
        corp3 = ""
    print("회사주소1 : " + corp1)
    print("회사주소2 : " + corp2)
    print("회사주소3 : " + corp3)


    zipCd = item.find('zipCd').text if item.find('zipCd') is not None else "N/A"
    print("근무지 우편번호 : " + zipCd )

    basicAddr = item.find('basicAddr').text if item.find('basicAddr') is not None else "N/A"
    print("근무지 기본주소 : " + basicAddr)

    detailAddr = item.find('detailAddr').text if item.find('detailAddr') is not None else ""
    print(detailAddr)

    contract=details.find('.//empTpCd').text if details.find('.//empTpCd') is not None else "N/A"
    if contract == '10' : contract = '정규직'
    elif contract == '11' : contract = '정규직'
    elif contract == '20' : contract = '계약직'
    elif contract == '21' : contract = '아르바이트'
    else : able = False
    print("계약형태 : " + contract)

    minSal=item.find('minSal').text if item.find('minSal') is not None else "N/A"
    maxSal=item.find('maxSal').text if item.find('maxSal') is not None else "N/A"
    typeSal=item.find('salTpNm').text if item.find('salTpNm') is not None else "N/A"
    textSal = ""
    if typeSal == '연봉' or typeSal == '월급' :
        textSal = typeSal + " " + str(int(int(minSal)/10000)) + "만원 ~ " + str(int(int(maxSal)/10000)) + "만원"
    elif typeSal == '일급' or typeSal == '시급' :
        textSal = typeSal + " " + str(minSal) + "원 ~ " + str(maxSal) + "원"
    else : able = False
    print("임금 : " + textSal)
    pay = textSal

    occ=item.find('indTpNm').text if item.find('indTpNm') is not None else "N/A"
    print("직종 : " + occ)

    sector=details.find('.//jobsNm').text if details.find('.//jobsNm') is not None else "N/A"
    print("세부직종 : " + sector)

    job_code=split_job_input(sector)
    sector = job_code[0]
    print("직종코드 : " + job_code[1])


    korean = ''
    print("한국어능력 : " + korean)

    region = item.find('region').text[:2] if item.find('region') is not None else "N/A"
    print("근무지역 : " + region)

    closeDt = item.find('closeDt').text if item.find('closeDt') is not None else "N/A"
    duedate = process_date(closeDt)
    print("마감일 : " + duedate[1])
    print("채용시까지 여부 : " + duedate[0])


    title = item.find('title').text if item.find('title') is not None else "N/A"
    print("제목 : " + title)

    desc = details.find('.//jobCont').text if details.find('.//jobCont') is not None else "N/A"
    print("내용 : " + desc)

    treatment1 = details.find('.//compAbl').text if details.find('.//compAbl') is not None else ""
    treatment2 = details.find('.//pfCond').text if details.find('.//pfCond') is not None else ""
    treatment3 = details.find('.//etcPfCond').text if details.find('.//etcPfCond') is not None else ""
    treatment = (str(treatment1) + " " + str(treatment2) + " " + str(treatment3))
    treatment = treatment.replace("None", "").strip()
    print("우대사항 : " + treatment)

    address = basicAddr
    lat_lon = get_lat_lon(address, kakao_api_key)
    output = "(" + ", ".join(lat_lon) + ")" if lat_lon is not None else "N/A"
    print("위치 : " + output)

    career = item.find('career').text if item.find('career') is not None else "N/A"
    if career == '관계없음' : career = '경력무관'
    print("경력 : " + career)

    workdayWorkhrCont = details.find('.//workdayWorkhrCont').text if details.find('.//workdayWorkhrCont') is not None else "N/A"
    workTime = extract_working_hours(workdayWorkhrCont)
    print("근무시간 : " + str(workTime))
    holidayTpNm = item.find('holidayTpNm').text if item.find('holidayTpNm') is not None else "N/A"
    pattern = r"^주\d+일근무$"
    if not re.match(pattern, holidayTpNm):
        holidayTpNm = "기타"
    print("휴일 : " + str(holidayTpNm))

    etcWelfare = details.find('.//etcWelfare').text if details.find('.//etcWelfare') is not None else "N/A"
    print("복지 : " + str(etcWelfare))

    print("visa : " + "기본비자")

    print("출처 : " + "worknet")

    print("\n")

    connection = get_db_connection()
    id = 0

    try:
        with connection.cursor() as cursor:
            sql = """
            Insert Into job (user_id, c_no, c_name, p_name, p_phone, industry, size,
            postcode_kor, address_kor, address2_kor,
            contract, pay, job_code, occ, sector, korean, region, duedate, latlng, always, career,
            postcode_work, address_work, address2_work,
            treatment, authNo, source, workday, worktime, minSal, maxSal, typeSal)
            Value (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, c_no, c_name, p_name, p_phone, industry, size_text,
                                  corp1, corp2, corp3,
                                  contract, pay, job_code[1], occ, sector, korean, region, duedate[1], output, duedate[0], career,
                                  zipCd, basicAddr, detailAddr,
                                  treatment, authNo, "worknet", holidayTpNm, workTime, minSal, maxSal, typeSal))
            connection.commit()

            id = cursor.lastrowid

            lang_list = ['en', 'zh', 'th', 'vi', 'ru' , 'my']
            targets = [title, desc, treatment]

            t_title = [title]
            t_desc = [desc]
            t_treatment = [treatment]

            for lang in lang_list:
                try:
                    # 배치 번역 요청
                    result = service.translations().list(
                        q=targets,
                        target=lang
                    ).execute()
                    translations = [item2['translatedText'] for item2 in result['translations']]
                    t_title.append(translations[0])
                    t_desc.append(translations[1])
                    t_treatment.append(translations[2])

                except Exception as e:
                  return 'error'

            tuple_content = (id, ) + tuple(t_title) + tuple(t_desc) + tuple(t_treatment)

            sql = """
            Insert Into job_content (job_id, title_ko, title_en, title_zh, title_th, title_vi, title_ru, title_my,
            desc_ko, desc_en, desc_zh, desc_th, desc_vi, desc_ru, desc_my, tr_ko, tr_en, tr_zh, tr_th, tr_vi, tr_ru, tr_my)
            Value (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s)
            """
            cursor.execute(sql, tuple_content)
            connection.commit()


            sql = "Insert Into job_notice (job_id, n0, n1, n2, n3, n4) Value (%s, %s, %s, %s, %s, %s)"
            text0 = "해당 직무에 관심을 갖고 지원해주셔서 감사합니다. 안타깝게도 귀하의 합격 소식을 전해드리지 못하게 되었습니다."
            text1 = "제출하신 서류가 성공적으로 등록되었습니다. 서류전형 결과를 기다려 주십시오."
            text2 = "서류전형에 합격하셨습니다. 상세한 면접일정은 추후에 안내하겠습니다."
            text3 = "면접전형에 합격하셨습니다. 추후 일정은 개별적으로 안내하겠습니다."
            text4 = "축하합니다. 채용이 확정되었습니다."
            cursor.execute(sql, (id, text0, text1, text2, text3, text4))
            connection.commit()

            with app.app_context():
                bubble_job_post(user_id, id, typeSal, int(minSal), int(maxSal), etcWelfare, duedate[0], duedate[1])

            return str(id)
    finally:
        connection.close()



#당일 외부 채용공고 수집 및 자사 DB 연동
@app.route('/worknet_post', methods=['POST']) 
def worknet_post():
    start_page = int(request.form.get('start_page'))
    display_count = int(request.form.get('display_count'))
    keyword = request.form.get('keyword')
    reg_date = request.form.get('reg_date')

    params = {
        "authKey": worknet_key,
        "callTp": "L",
        "returnType": "XML",
        "startPage": start_page,
        "display": display_count,
        "keyword": keyword,
        "regDate": reg_date
    }

    response = requests.get(worknet_url, params=params)

    if response.status_code == 200:
        # XML 데이터 파싱
        root = ET.fromstring(response.content)

        # 오늘 하루 외국인 관련 공고 수
        total =  root.find('total').text if root.find('total') is not None else "N/A"
        print(f"Toal Count: {total}\n")

        # 각종 배열 정의
        authNoList = list();
        count = 0;

        # 각 개별 항목(item)을 반복하여 출력
        for idx, item in enumerate(root.findall('.//wanted')):  # 'item' 태그에 맞게 수정
            wantNo = item.find('wantedAuthNo').text if item.find('wantedAuthNo') is not None else "N/A"  # 예시 필드 1
            authNoList.append(wantNo)
            each_post(wantNo, item)
    else:
        return jsonify({"message": "Failed to fetch data from Worknet API"}), 500

    return jsonify({"message": "Data updated successfully"}), 200


# "채용시 마감" 공고의 채용 상태 점검 및 최신화
@app.route('/check_close', methods=['PATCH'])
def check_close():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = """
            SELECT
                job.authNo, job.id  -- job.id도 함께 선택
            FROM
                job
            WHERE
                job.always = %s AND job.onoff = %s AND job.source = %s;
            """
            # 조건에 맞는 값을 SQL 쿼리로 전달
            cursor.execute(sql, ('네', 'yes', 'worknet'))
            result = cursor.fetchall()

            # 결과를 JSON 형식으로 반환
            job_auth = [row['authNo'] for row in result]
            job_id = [row['id'] for row in result]

            for (n, id) in zip(job_auth, job_id):  # 두 리스트를 병렬로 순회
                params_detail = {
                    "authKey": worknet_key,
                    "callTp": "D",
                    "returnType": "XML",
                    "wantedAuthNo": n,
                    "infoSvc": "VALIDATION"
                }
                details = requests.get(worknet_url, params=params_detail)  # 채용 디테일 불러오기
                details = ET.fromstring(details.content)  # XML 데이터를 파싱
                code = details.find('.//messageCd').text if details.find('.//messageCd') is not None else "N/A"

                # 메시지 코드가 '006'인 경우, 해당 공고 마감
                if code == '006':
                    job_close(id)

            return jsonify({"message": "Data updated successfully"}), 200
    finally:
        connection.close()

def job_close(job_id):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = "Update job Set onoff='no' Where id = %s"
            cursor.execute(sql, (job_id))
            connection.commit()

            return jsonify({"message": "Job off successfully"})
    finally:
        connection.close()

if __name__ == "__main__":
    http_tunnel = ngrok.connect(5001, subdomain="koreamedevelop")
    print(f"ngrok tunnel \"{http_tunnel.public_url}\" -> \"http://127.0.0.1:5001\"")
    app.run(port=5001)
