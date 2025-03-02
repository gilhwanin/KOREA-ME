
    ### 개발메인


###라이브러리
import os, time, random, string, json, requests, pymysql, re, io
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, send_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import vision



###전역변수 선언
countries_dict = {
    "AFG": "AFGHANISTAN",
    "ALA": "ALAND ISLANDS",
    "ALB": "ALBANIA",
    "DZA": "ALGERIA",
    "ASM": "AMERICAN SAMOA",
    "AND": "ANDORRA",
    "AGO": "ANGOLA",
    "AIA": "ANGUILLA",
    "ATA": "ANTARCTICA",
    "ATG": "ANTIGUA AND BARBUDA",
    "ARG": "ARGENTINA",
    "ARM": "ARMENIA",
    "ABW": "ARUBA",
    "AUS": "AUSTRALIA",
    "AUT": "AUSTRIA",
    "AZE": "AZERBAIJAN",
    "BHS": "BAHAMAS",
    "BHR": "BAHRAIN",
    "BGD": "BANGLADESH",
    "BRB": "BARBADOS",
    "BLR": "BELARUS",
    "BEL": "BELGIUM",
    "BLZ": "BELIZE",
    "BEN": "BENIN",
    "BMU": "BERMUDA",
    "BTN": "BHUTAN",
    "BOL": "BOLIVIA",
    "BIH": "BOSNIA HERCEGOVINA",
    "BWA": "BOTSWANA",
    "BVT": "BOUVET ISLAND",
    "BRA": "BRAZIL",
    "IOT": "BRITISH INDIAN OCEAN TERRITORY",
    "BRN": "BRUNEI DARUSSALAM",
    "BGR": "BULGARIA",
    "BFA": "BURKINA FASO",
    "BDI": "BURUNDI",
    "KHM": "CAMBODIA",
    "CMR": "CAMEROON",
    "CAN": "CANADA",
    "CPV": "CAPE VERDE",
    "CYM": "CAYMAN ISLANDS",
    "CAF": "CENTRAL AFRICAN REPUBLIC",
    "TCD": "CHAD",
    "CHL": "CHILE",
    "CHN": "CHINA",
    "CXR": "CHRISTMAS ISLAND",
    "CCK": "COCOS ISLANDS",
    "COL": "COLOMBIA",
    "COM": "COMOROS",
    "COG": "CONGO",
    "COK": "COOK ISLANDS",
    "CRI": "COSTA RICA",
    "CIV": "COTE D'IVOIRE",
    "HRV": "CROATIA",
    "CUB": "CUBA",
    "CYP": "CYPRUS",
    "CZE": "CZECH REPUBLIC",
    "COD": "DEMOCRATIC REPUBLIC OF THE CONGO",
    "DNK": "DENMARK",
    "DJI": "DJIBOUTI",
    "DMA": "DOMINICA",
    "DOM": "DOMINICAN REPUBLIC",
    "TLS": "EAST TIMOR",
    "ECU": "ECUADOR",
    "EGY": "EGYPT",
    "SLV": "EL SALVADOR",
    "GNQ": "EQUATORIAL GUINEA",
    "ERI": "ERITREA",
    "EST": "ESTONIA",
    "ETH": "ETHIOPIA",
    "FLK": "FALKLAND ISLANDS",
    "FRO": "FAROE ISLANDS",
    "FJI": "FIJI",
    "FIN": "FINLAND",
    "FRA": "FRANCE",
    "GUF": "FRENCH GUIANA",
    "PYF": "FRENCH POLYNESIA",
    "ATF": "FRENCH SOUTHERN TERRITORIES",
    "GAB": "GABON",
    "GMB": "GAMBIA",
    "GEO": "GEORGIA",
    "DEU": "GERMANY",
    "GHA": "GHANA",
    "GIB": "GIBRALTAR",
    "GRC": "GREECE",
    "GRL": "GREENLAND",
    "GRD": "GRENADA",
    "GLP": "GUADELOUPE",
    "GUM": "GUAM",
    "GTM": "GUATEMALA",
    "GGY": "GUERNSEY",
    "GIN": "GUINEA",
    "GNB": "GUINEA-BISSAU",
    "GUY": "GUYANA",
    "HTI": "HAITI",
    "HMD": "HEARD AND MC DONALD ISLANDS",
    "HND": "HONDURAS",
    "HKG": "HONG KONG",
    "HUN": "HUNGARY",
    "ISL": "ICELAND",
    "IND": "INDIA",
    "IDN": "INDONESIA",
    "IRN": "IRAN",
    "IRQ": "IRAQ",
    "IRL": "IRELAND",
    "IMN": "ISLE OF MAN",
    "ISR": "ISRAEL",
    "ITA": "ITALY",
    "JAM": "JAMAICA",
    "JPN": "JAPAN",
    "JEY": "JERSEY",
    "JOR": "JORDAN",
    "KAZ": "KAZAKHSTAN",
    "KEN": "KENYA",
    "KIR": "KIRIBATI",
    "PRK": "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
    "KOR": "KOREA, REPUBLIC OF",
    "KWT": "KUWAIT",
    "KGZ": "KYRGYZSTAN",
    "LAO": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
    "LVA": "LATVIA",
    "LBN": "LEBANON",
    "LSO": "LESOTHO",
    "LBR": "LIBERIA",
    "LBY": "LIBYAN ARAB JAMAHIRIYA",
    "LIE": "LIECHTENSTEIN",
    "LTU": "LITHUANIA",
    "LUX": "LUXEMBOURG",
    "MAC": "MACAU",
    "MDG": "MADAGASCAR",
    "MWI": "MALAWI",
    "MYS": "MALAYSIA",
    "MDV": "MALDIVES",
    "MLI": "MALI",
    "MLT": "MALTA",
    "MHL": "MARSHALL ISLANDS",
    "MTQ": "MARTINIQUE",
    "MRT": "MAURITANIA",
    "MUS": "MAURITIUS",
    "MYT": "MAYOTTE",
    "MEX": "MEXICO",
    "FSM": "MICRONESIA",
    "MDA": "MOLDOVA, REPUBLIC OF",
    "MCO": "MONACO",
    "MNG": "MONGOLIA",
    "MNE": "MONTENEGRO",
    "MSR": "MONTSERRAT",
    "MAR": "MOROCCO",
    "MOZ": "MOZAMBIQUE",
    "MMR": "MYANMAR",
    "NAM": "NAMIBIA",
    "NRU": "NAURU",
    "NPL": "NEPAL",
    "NLD": "NETHERLANDS",
    "ANT": "NETHERLANDS ANTILLES",
    "NCL": "NEW CALEDONIA",
    "NZL": "NEW ZEALAND",
    "NIC": "NICARAGUA",
    "NER": "NIGER",
    "NGA": "NIGERIA",
    "NIU": "NIUE",
    "NFK": "NORFOLK ISLAND",
    "MNP": "NORTHERN MARIANA ISLANDS",
    "NOR": "NORWAY",
    "OMN": "OMAN",
    "PAK": "PAKISTAN",
    "PLW": "PALAU",
    "PSE": "PALESTINE",
    "PAN": "PANAMA",
    "PNG": "PAPUA NEW GUINEA",
    "PRY": "PARAGUAY",
    "PER": "PERU",
    "PHL": "PHILIPPINES",
    "PCN": "PITCAIRN",
    "POL": "POLAND",
    "PRT": "PORTUGAL",
    "PRI": "PUERTO RICO",
    "QAT": "QATAR",
    "MKD": "REPUBLIC OF MACEDONIA",
    "SSD": "REPUBLIC OF SOUTH SUDAN",
    "REU": "REUNION",
    "ROU": "ROMANIA",
    "RUS": "RUSSIAN FEDERATION",
    "RWA": "RWANDA",
    "KNA": "SAINT KITTS AND NEVIS",
    "LCA": "SAINT LUCIA",
    "VCT": "SAINT VINCENT AND THE GRENADINES",
    "WSM": "SAMOA",
    "SMR": "SAN MARINO",
    "STP": "SAO TOME AND PRINCIPE",
    "SAU": "SAUDI ARABIA",
    "SEN": "SENEGAL",
    "SRB": "SERBIA",
    "SYC": "SEYCHELLES",
    "SLE": "SIERRA LEONE",
    "SGP": "SINGAPORE",
    "SVK": "SLOVAKIA",
    "SVN": "SLOVENIA",
    "SLB": "SOLOMON ISLANDS",
    "SOM": "SOMALIA",
    "ZAF": "SOUTH AFRICA",
    "SGS": "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS",
    "ESP": "SPAIN",
    "LKA": "SRI LANKA",
    "SHN": "ST. HELENA",
    "SPM": "ST. PIERRE AND MIQUELON",
    "SDN": "SUDAN",
    "SUR": "SURINAME",
    "SJM": "SVALBARD AND JAN MAYEN ISLANDS",
    "SWZ": "SWAZILAND",
    "SWE": "SWEDEN",
    "CHE": "SWITZERLAND",
    "SYR": "SYRIAN ARAB REPUBLIC",
    "TWN": "TAIWAN, PROVINCE OF CHINA",
    "TJK": "TAJIKISTAN",
    "TZA": "TANZANIA, UNITED REPUBLIC OF",
    "THA": "THAILAND",
    "TGO": "TOGO",
    "TKL": "TOKELAU",
    "TON": "TONGA",
    "TTO": "TRINIDAD AND TOBAGO",
    "TUN": "TUNISIA",
    "TUR": "TURKEY",
    "TKM": "TURKMENISTAN",
    "TCA": "TURKS AND CAICOS ISLANDS",
    "TUV": "TUVALU",
    "UGA": "UGANDA",
    "UKR": "UKRAINE",
    "ARE": "UNITED ARAB EMIRATES",
    "GBR": "UNITED KINGDOM",
    "USA": "UNITED STATES",
    "UMI": "UNITED STATES MINOR OUTLYING ISLANDS",
    "URY": "URUGUAY",
    "UZB": "UZBEKISTAN",
    "VUT": "VANUATU",
    "VAT": "VATICAN CITY STATE",
    "VEN": "VENEZUELA",
    "VNM": "VIET NAM",
    "VGB": "VIRGIN ISLANDS, BRITISH",
    "VIR": "VIRGIN ISLANDS, U.S.",
    "WLF": "WALLIS AND FUTUNA ISLANDS",
    "ESH": "WESTERN SAHARA",
    "YEM": "YEMEN, REPUBLIC OF",
    "ZMB": "ZAMBIA",
    "ZWE": "ZIMBABWE"
}

characters = string.digits

app = Flask(__name__)

db_host = 'korea-me-aws-db.cl2cki8esp8b.ap-northeast-2.rds.amazonaws.com'
db_user = 'admin'
db_password = '9120ssf3'
db_name = 'db1'
db_port= 3306



###Google Console API 연결
KEY_FILE = '/home/ubuntu/stable-course-440718-q6-62101337dec5.json'

# Google Translation API
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-translation"]
)

# Google Cloud Vision API
service = build('translate', 'v2', credentials=credentials)

credentials2 = service_account.Credentials.from_service_account_file(
    KEY_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-vision"]
)
client = vision.ImageAnnotatorClient(credentials=credentials2)



###함수정의
@app.before_request
def check_authentication():
    token = request.headers.get('Authorization')
    if token != "2c2fd5eb8962611a79799ae8a0bd8ad209fbb90d52d0dfd10f0be48fb22384e9":
        return jsonify({"message": "Unauthorized"}), 401



def get_db_connection():
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



def detect_language(text):   #언어감지함수
    try:
        # 언어 감지 요청
        detection = service.detections().list(
            q=[text]
        ).execute()

        # 결과에서 감지된 언어 추출
        language_code = detection['detections'][0][0]['language']

        return language_code

    except Exception as e:
        print(f"Error during language detection: {e}")
        return None



def translate_text(text, source_language, target_language):   #번역함수
    # 번역 요청
    request = service.translations().list(
        q=text,
        source=source_language,
        target=target_language,
        format='text'
    )
    response = request.execute()

    # 번역 결과 반환
    translated_text = response['translations'][0]['translatedText']
    return translated_text



def detect_text_from_image(image_path):

    content = image_path.read()

    image = vision.Image(content=content)

    # 문서 텍스트 감지 요청
    response = client.document_text_detection(image=image)

    # 응답에서 전체 텍스트를 추출
    document_text = response.full_text_annotation.text

    if response.error.message:
        raise Exception(f'Error: {response.error.message}')

    return document_text



def parse_mrz_data(mrz_lines):
    """
    MRZ 데이터에서 여권 정보를 추출합니다.

    Args:
        mrz_lines (list): 여권 MRZ 2줄 데이터를 포함하는 리스트.

    Returns:
        dict: 추출된 여권 정보.
    """
    if len(mrz_lines) != 2:
        raise ValueError("MRZ 데이터는 두 줄이어야 합니다.")

    # 첫 번째 줄에서 타입, 발급 국가, 이름 추출
    mrz_line1 = mrz_lines[0]
    document_type = mrz_line1[0]  # 문서 타입 (보통 'P')
    issuing_country = mrz_line1[2:5]  # 발급 국가 코드 (ISO 3166-1 alpha-3)

    # 이름 (성과 이름은 '<'로 구분됨)
    names = mrz_line1[5:].split('<<')
    surname = names[0].replace('<', ' ').strip()  # 성 (공백은 '<'로 처리됨)
    given_names = names[1].replace('<', ' ').strip()  # 이름 (공백은 '<'로 처리됨)

    # 두 번째 줄에서 여권 번호, 국적, 생년월일, 성별, 여권 만료일 추출
    mrz_line2 = mrz_lines[1]
    passport_number = mrz_line2[0:9].replace('<', '')  # 여권 번호
    nationality = countries_dict.get(mrz_line2[10:13])  # 국적 코드
    birth_date = mrz_line2[13:19]  # 생년월일 (YYMMDD)
    gender = mrz_line2[20]  # 성별 (M or F)
    expiry_date = mrz_line2[22:28]  # 여권 만료일 (YYMMDD)

    # 발급 국가 또는 여권 소유자의 개인 ID 번호 (존재할 수 있음)
    personal_number = mrz_line2[28:42].replace('<', '')

    # 생년월일, 만료일을 사람이 읽기 쉬운 형식으로 변환
    birth_date = f"19{birth_date[:2]}-{birth_date[2:4]}-{birth_date[4:]}"
    expiry_date = f"20{expiry_date[:2]}-{expiry_date[2:4]}-{expiry_date[4:]}"

    # 성별 처리
    if gender == 'M':
        gender = '남자'
    elif gender == 'F':
        gender = '여자'
    else:
        gender = '남자'

    # 결과 반환
    return {
        "Document Type": document_type,
        "Issuing Country": issuing_country,
        "Surname": surname,
        "Given Names": given_names,
        "Passport Number": passport_number,
        "Nationality": nationality,
        "Birth Date": birth_date,
        "Gender": gender,
        "Expiry Date": expiry_date,
        "Personal Number": personal_number
    }



@app.route('/passport_OCR', methods=['POST'])   #여권 OCR
def passport_OCR():
    file = request.files.get('file')  # form-data의 'file' key에서 이미지 가져오기
    if file and file.filename.endswith(('png', 'jpg', 'jpeg', 'gif')):  # 이미지 파일인지 확인
        text = detect_text_from_image(file)
        if len(text[-1]+text[-2]) == 44:
            text[-1] = text[-1] + text[-2]
            text.pop(-2)
        if len(text[-2]+text[-3]) == 44:
            text[-2] = text[-2] + text[-3]
            text.pop(-3)

        MRZ = text.split("
")[-2:]

        result = parse_mrz_data(MRZ)
        return jsonify(result)

    return "Invalid image format", 400


@app.route('/randomcode', methods=['GET'])   #랜덤스트링 생성
def randomcode():
    random_string = ''.join(random.choice(characters) for _ in range(4))
    return str(random_string)


@app.route('/server_test', methods=['GET'])   #서버응답테스트
def server_test():
    return jsonify({"message": "success"})





###API
@app.route('/sign_in', methods=['POST'])  #일반회원가입
def sign_in():
    connection = get_db_connection()
    email = request.form.get('email')
    try:
        with connection.cursor() as cursor:
            sql = "Insert Into account (email) Value (%s)"
            cursor.execute(sql, email)
            connection.commit()
            sql = "Select id from account Where email = %s"
            cursor.execute(sql, email)
            result = cursor.fetchall()
            id = result[0].get('id')
            sql = "Insert Into profile (user_id) Value (%s)"
            cursor.execute(sql, id)
            connection.commit()
            sql = "Insert Into profile_image (user_id) Value (%s)"
            cursor.execute(sql, id)
            connection.commit()
            return str(id)
    finally:
        connection.close()


@app.route('/sign_in_company', methods=['POST'])   #기업회원가입
def sign_in_company():
    connection = get_db_connection()
    email = request.form.get('email')
    try:
        with connection.cursor() as cursor:
            sql = "Insert Into account_company (email) Value (%s)"
            cursor.execute(sql, email)
            connection.commit()
            sql = "Select id from account_company Where email = %s"
            cursor.execute(sql, email)
            result = cursor.fetchall()
            id = result[0].get('id')
            sql = "Insert Into company (user_id) Value (%s)"
            cursor.execute(sql, id)
            connection.commit()
            return str(id)

    finally:
        connection.close()


@app.route('/sign_out', methods=['DELETE'])   #회원탈퇴
def sign_out():
    connection = get_db_connection()
    id = request.form.get('id')
    isCompany = request.form.get('isCompany')

    try:
        with connection.cursor() as cursor:
            sql = ""
            if isCompany == '0':
                sql = "Delete from account where id = %s;"
            else:
                sql = "Delete from account_company where id = %s;"
            cursor.execute(sql, id)
            connection.commit()

            return jsonify({"message": "Account removed successfully"})
    finally:
        connection.close()




 ###일반회원###


@app.route('/resume2_put', methods=['POST'])   #이력서2 등록 -------------------------------------------------------------------
def resume2_put():
    connection = get_db_connection()
    user_id = request.form.get('user_id')
    job_id = request.form.get('job_id')
    created_date = request.form.get('created_date')

    try:
        with connection.cursor() as cursor:
            sql = """
            Insert Into resume2 (user_id, job_id)
            Value (%s, %s)
            """
            cursor.execute(sql, (user_id, job_id))
            connection.commit()

            id = cursor.lastrowid

            sql = """
            Insert into applications (user_id, resume2_id, job_id, status, message, created_date)
            Value (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (user_id, id, job_id, 1, "제출하신 서류가 성공적으로 등록되었습니다. 서류전형 결과를 기다려 주십시오.", created_date))
            connection.commit()
            return str(id)
    finally:
        connection.close()


@app.route('/resume2_out', methods=['DELETE'])   #이력서2 삭제
def resume2_out():
    connection = get_db_connection()
    id = request.form.get('id')

    try:
        with connection.cursor() as cursor:
            sql = "Delete from resume2 where id = %s;"
            cursor.execute(sql, id)
            connection.commit()

            return jsonify({"message": "Data removed successfully"})
    finally:
        connection.close()


@app.route('/resume2_get', methods=['GET'])   #이력서2 가져오기
def resume2_get():
    connection = get_db_connection()
    id = request.args.get('id')
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT * FROM resume2
            WHERE resume2.id = %s
            """
            cursor.execute(sql, id)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()


###기업회원###


@app.route('/job_put', methods=['POST'])   #채용공고 등록
def job_put():
    connection = get_db_connection()
    user_id = request.form.get('user_id')
    c_no = request.form.get('c_no')
    c_name = request.form.get('c_name')
    p_name = request.form.get('p_name')
    p_phone = request.form.get('p_phone')
    industry = request.form.get('industry')
    size = request.form.get('size')
    postcode_kor = request.form.get('postcode_kor')
    address_kor = request.form.get('address_kor')
    address2_kor = request.form.get('address2_kor')
    contract = request.form.get('contract')
    pay = request.form.get('pay')
    occ = request.form.get('occ')
    sector = request.form.get('sector')
    korean= request.form.get('korean')
    region = request.form.get('region')
    duedate = request.form.get('duedate')
    title = request.form.get('title')
    desc = request.form.get('desc')
    latlng = request.form.get('latlng')
    always = request.form.get('always')
    career = request.form.get('career')
    region2 = request.form.get('region2')
    postcode_work = request.form.get('postcode_work')
    address_work = request.form.get('address_work')
    address2_work = request.form.get('address2_work')
    treatment = request.form.get('treatment')
    source = request.form.get('source')
    workday = request.form.get('workday')
    worktime = request.form.get('worktime')
    job_code = request.form.get('job_code')
    minSal = request.form.get('minSal')
    maxSal = request.form.get('maxSal')
    typeSal = request.form.get('typeSal')


    try:
        with connection.cursor() as cursor:
            sql = """
            Insert Into job (user_id, c_no, c_name, p_name, p_phone, industry, size,
            postcode_kor, address_kor, address2_kor,
            contract, pay, job_code, occ, sector, korean, region, duedate, latlng, always, career, postcode_work, address_work, address2_work,
            treatment, source, workday, worktime, minSal, maxSal, typeSal)
            Value (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, c_no, c_name, p_name, p_phone, industry, size, postcode_kor, address_kor, address2_kor,
            contract, pay, job_code, occ, sector, korean, region, duedate, latlng, always, career, postcode_work, address_work, address2_work,
            treatment, source, workday, worktime, minSal, maxSal, typeSal))
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
                    translations = [item['translatedText'] for item in result['translations']]
                    t_title.append(translations[0])
                    t_desc.append(translations[1])
                    t_treatment.append(translations[2])

                except Exception as e:
                  return 'error'

            tuple_content = (id, ) + tuple(t_title) + tuple(t_desc) + tuple(t_treatment)

            sql = """
            Insert Into job_content (job_id, title_ko, title_en, title_zh, title_th, title_vi, title_ru, title_my,
            desc_ko, desc_en, desc_zh, desc_th, desc_vi, desc_ru, desc_my, tr_ko, tr_en, tr_zh, tr_th, tr_vi, tr_ru, tr_my)
            Value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            return str(id)
    finally:
        connection.close()


@app.route('/job_set', methods=['PUT'])   #채용공고 세부직무 수정
def job_set():
    connection = get_db_connection()
    id = request.form.get('id')
    duedate = request.form.get('duedate')
    desc = request.form.get('desc')
    isDuedate = request.form.get('isDuedate')

    try:
        with connection.cursor() as cursor:

            if isDuedate == '네':
                sql = "Update job Set duedate = %s Where id = %s"
                cursor.execute(sql, (duedate, id))
                connection.commit()

            if isDuedate == '아니오':
                lang_list = ['en', 'zh', 'th', 'vi']
                targets = [desc]
                t_desc = [desc]

                for lang in lang_list:
                    try:
                        # 배치 번역 요청
                        result = service.translations().list(
                            q=targets,
                            target=lang
                        ).execute()
                        translations = [item['translatedText'] for item in result['translations']]
                        t_desc.append(translations[0])

                    except Exception as e:
                      return 'error'

                tuple_content = tuple(t_desc) + (id, )

                sql = """
                Update job_content Set desc_ko=%s, desc_en=%s, desc_zh=%s, desc_th=%s, desc_vi=%s Where job_id = %s"""
                cursor.execute(sql, tuple_content)
                connection.commit()

            return jsonify({"message": "Data updated successfully"})
    finally:
        connection.close()


@app.route('/job_get', methods=['GET'])   # 채용공고 가져오기
def job_get():
    connection = get_db_connection()
    job_id = request.args.get('id')
    lang = request.args.get('lang')

    # 언어 코드에 따라 job_content에서 쿼리할 필드 설정
    field_map = {
        'ko_kr': ['title_ko', 'desc_ko', 'tr_ko'],  # ko_kr도 선택 가능하지만 항상 고정 출력됨
        'en_us': ['title_en', 'desc_en', 'tr_en'],
        'zh_cn': ['title_zh', 'desc_zh', 'tr_zh'],
        'vi_vn': ['title_vi', 'desc_vi', 'tr_vi'],
        'th_th': ['title_th', 'desc_th', 'tr_th'],
        'ru_ru': ['title_ru', 'desc_ru', 'tr_ru'],
        'my_my': ['title_my', 'desc_my', 'tr_my']
    }

    # lang 값이 유효한지 확인
    if lang not in field_map:
        return jsonify({"error": "Invalid language code"}), 400

    # ko_kr 필드는 항상 출력
    fixed_fields = field_map['ko_kr']

    # 선택된 언어의 필드
    selected_fields = field_map[lang]

    # SQL 쿼리에서 선택된 필드에 대한 alias 설정
    selected_content_fields_str = ", ".join([
        f"{fixed_fields[0]} AS title_ko",  # 고정된 한국어 필드
        f"{fixed_fields[1]} AS desc_ko",
        f"{fixed_fields[2]} AS tr_ko",
        f"{selected_fields[0]} AS title_selected",  # 선택된 언어 필드 -> title_selected, desc_selected, tr_selected로 출력
        f"{selected_fields[1]} AS desc_selected",
        f"{selected_fields[2]} AS tr_selected"
    ])

    try:
        with connection.cursor() as cursor:
            # 동적으로 쿼리 구성
            sql = f"""
            SELECT job.*, {selected_content_fields_str}
            FROM job
            INNER JOIN job_content ON job.id = job_content.job_id
            WHERE job.id = %s
            """
            cursor.execute(sql, (job_id,))
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()


@app.route('/job_list', methods=['GET'])   #채용공고 가져오기
def job_list():
    connection = get_db_connection()
    user_id = request.args.get('user_id')
    try:
        with connection.cursor() as cursor:
            sql ="""
            SELECT
                j.id,
                jc.title_ko,
                j.contract,
                j.onoff,
                j.always,
                j.duedate,
                IFNULL(status_counts.`0`, 0) AS status_0,
                IFNULL(status_counts.`1`, 0) AS status_1,
                IFNULL(status_counts.`2`, 0) AS status_2,
                IFNULL(status_counts.`3`, 0) AS status_3,
                IFNULL(status_counts.`4`, 0) AS status_4
            FROM
                job j
            INNER JOIN
                job_content jc ON j.id = jc.job_id
            LEFT JOIN
                (SELECT
                    job_id,
                    SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS '0',
                    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS '1',
                    SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS '2',
                    SUM(CASE WHEN status = 3 THEN 1 ELSE 0 END) AS '3',
                    SUM(CASE WHEN status = 4 THEN 1 ELSE 0 END) AS '4'
                FROM
                    applications
                GROUP BY
                    job_id) AS status_counts ON j.id = status_counts.job_id
            WHERE
                j.user_id = %s
            ORDER BY
                j.id DESC;
            """
            cursor.execute(sql, user_id)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()


@app.route('/job_toggle', methods=['POST'])   #채용상태 전환
def job_toggle():
    connection = get_db_connection()
    job_id = request.form.get('job_id')
    toggle = request.form.get('toggle')
    toChange = ''
    if toggle == '네':
        toChange = 'no'
    else:
        toChange = 'yes'
    try:
        with connection.cursor() as cursor:
            sql = "Update job Set onoff=%s Where id = %s"
            cursor.execute(sql, (toChange, job_id))
            connection.commit()

            return jsonify({"message": "Data toggled successfully"})
    finally:
        connection.close()

@app.route('/job_close', methods=['PATCH'])   #채용마감
def job_close():
    connection = get_db_connection()
    job_id = request.form.get('job_id')

    try:
        with connection.cursor() as cursor:
            sql = "Update job Set onoff='no' Where id = %s"
            cursor.execute(sql, (job_id))
            connection.commit()

            return jsonify({"message": "Job off successfully"})
    finally:
        connection.close()


@app.route('/applicant_list', methods=['GET'])   #지원자 특정단계 리스트 가져오기
def applicant_list():
    connection = get_db_connection()
    id = request.args.get('id')
    status = request.args.get('status')

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT * FROM applications
            WHERE applications.job_id = %s And applications.status = %s
            """
            cursor.execute(sql, (id, status))
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()

@app.route('/applicant_all', methods=['GET'])   #지원자 전체리스트 가져오기 + 해당유저의 모든공고 (회원탈퇴시 이용)
def applicant_all():
    connection = get_db_connection()
    user_id = request.args.get('user_id')
    job_id = request.args.get('job_id')
    isAll = request.args.get('isAll')

    try:
        with connection.cursor() as cursor:
            sql = ""
            if isAll == 'yes':
                sql = """
                SELECT resume2_id
                FROM applications
                WHERE job_id IN (
                    SELECT id
                    FROM job
                    WHERE user_id = %s)"""
                cursor.execute(sql, (user_id,))
                result = cursor.fetchall()
                return jsonify(result)
            else :
                sql = """
                SELECT resume2_id FROM applications WHERE job_id = %s
                """
                cursor.execute(sql, (job_id,))
                result = cursor.fetchall()
                return jsonify(result)
    finally:
        connection.close()


@app.route('/apply_get', methods=['GET'])   #지원한 공고 지원결과 가져오기
def apply_get():
    connection = get_db_connection()
    resume2_id = request.args.get('resume2_id')

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT applications.*, job_content.title_ko FROM applications
            Inner JOIN job_content ON applications.job_id = job_content.job_id
            WHERE applications.resume2_id = %s
            """
            cursor.execute(sql, resume2_id)
            result = cursor.fetchall()

            if result[0]['status'] == 0 :
                result[0]['status'] = '불합격'
            elif result[0]['status'] == 1 :
                result[0]['status'] = '서류지원'
            elif result[0]['status'] == 2 :
                result[0]['status'] = '서류합격'
            elif result[0]['status'] == 3 :
                result[0]['status'] = '면접합격'
            elif result[0]['status'] == 4 :
                result[0]['status'] = '최종합격'

            return jsonify(result)
    finally:
        connection.close()


@app.route('/apply_check', methods=['GET'])   #중복지원체크
def apply_check():
    connection = get_db_connection()
    user_id = request.args.get('user_id')
    job_id = request.args.get('job_id')

    try:
        with connection.cursor() as cursor:
            max = 30
            isFull = "no"
            sql = """
            SELECT count(*) As 'sum' FROM applications
            Inner JOIN resume2 ON applications.resume2_id = resume2.id
            And resume2.user_id = %s
            """
            cursor.execute(sql, user_id)
            result = cursor.fetchone()
            if result['sum'] >= max:
                isFull = "yes"
            else:
                isFull = "no"

            sql = """
            SELECT applications.id FROM applications
            Inner JOIN resume2 ON applications.resume2_id = resume2.id
            Where applications.job_id = %s
            And resume2.user_id = %s
            """
            cursor.execute(sql, (job_id, user_id))
            result = cursor.fetchall()

            if len(result) == 0:
                return jsonify({"response": "지원가능", "full" : isFull})
            else:
                return jsonify({"response": "지원불가", "full" : isFull})
    finally:
        connection.close()


@app.route('/apply_board', methods=['GET'])   #대시보드 구직현황 보드판
def apply_board():
    connection = get_db_connection()
    user_id = request.args.get('user_id')

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT
                COALESCE(SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END), 0) AS status_0,
                COALESCE(SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END), 0) AS status_1,
                COALESCE(SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END), 0) AS status_2,
                COALESCE(SUM(CASE WHEN status = 3 THEN 1 ELSE 0 END), 0) AS status_3,
                COALESCE(SUM(CASE WHEN status = 4 THEN 1 ELSE 0 END), 0) AS status_4
            FROM applications
            WHERE user_id = %s """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()



@app.route('/AM_statusChange1', methods=['PATCH'])   #지원자 단계변경 서류지원자 --------------------------------------------------------------------------------
def AM_statusChange1():
    connection = get_db_connection()
    apply_id = request.form.get('apply_id')
    isPass= request.form.get('isPass')
    score = request.form.get('score')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            destination = 0
            if isPass == 'yes' :
                destination = 2

            sql = f"Update applications Set status=%s, message=%s, score1=%s Where id = %s"
            cursor.execute(sql, (destination, message, score, apply_id))
            connection.commit()

            return jsonify({"message": "Data Updated successfully"})

    finally:
        connection.close()

@app.route('/AM_statusChange2', methods=['PATCH'])  #지원자 단계변경 서류합격자
def AM_statusChange2():
    connection = get_db_connection()
    apply_id = request.form.get('apply_id')
    isPass= request.form.get('isPass')
    score = request.form.get('score')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            destination = 0
            if isPass == 'yes' :
                destination = 3

            sql = f"Update applications Set status=%s, message=%s, score2=%s Where id = %s"
            cursor.execute(sql, (destination, message, score, apply_id))
            connection.commit()

            return jsonify({"message": "Data Updated successfully"})

    finally:
        connection.close()


@app.route('/AM_statusChange3', methods=['PATCH'])  #지원자 단계변경 면접합격자
def AM_statusChange3():
    connection = get_db_connection()
    apply_id = request.form.get('apply_id')
    isPass= request.form.get('isPass')
    score = request.form.get('score')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            destination = 0
            if isPass == 'yes' :
                destination = 4

            sql = f"Update applications Set status=%s, message=%s Where id = %s"
            cursor.execute(sql, (destination, message, apply_id))
            connection.commit()

            return jsonify({"message": "Data Updated successfully"})

    finally:
        connection.close()


@app.route('/AM_statusChange4', methods=['PATCH'])   #지원자 최종합격 취소
def AM_statusChange4():
    connection = get_db_connection()
    apply_id = request.form.get('apply_id')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            sql = f"Update applications Set status=0, message=%s Where id = %s"
            cursor.execute(sql, (message, apply_id))
            connection.commit()

            return jsonify({"message": "Data Updated successfully"})

    finally:
        connection.close()


@app.route('/AM_editMessage', methods=['PATCH'])   #지원자메시지
def AM_editMessage():
    connection = get_db_connection()
    apply_id = request.form.get('apply_id')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            sql = "Update applications Set message=%s Where id = %s"
            cursor.execute(sql, (message, apply_id))
            connection.commit()
            return jsonify({"message": "Data updated successfully"})
    finally:
        connection.close()



@app.route('/AM_editMessage_bulk', methods=['PATCH'])   #지원자 단체메시지
def AM_editMessage_bulk():
    connection = get_db_connection()
    status = request.form.get('status')
    message = request.form.get('message')

    try:
        with connection.cursor() as cursor:
            sql = "Update applications Set message=%s Where status = %s"
            cursor.execute(sql, (message, status))
            connection.commit()
            return jsonify({"message": "Data updated successfully"})
    finally:
        connection.close()

@app.route('/AM_setMessage_bulk', methods=['PUT'])   #메시지 기본값 변경
def AM_setMessage_bulk():
    connection = get_db_connection()
    text0 = request.form.get('text0')
    text1 = request.form.get('text1')
    text2 = request.form.get('text2')
    text3 = request.form.get('text3')
    text4 = request.form.get('text4')
    job_id = request.form.get('job_id')

    try:
        with connection.cursor() as cursor:
            sql = "Update job_notice Set n0=%s, n1=%s, n2=%s, n3=%s, n4=%s Where job_id = %s"
            cursor.execute(sql, (text0, text1, text2, text3, job_id))
            connection.commit()
            return jsonify({"message": "Data updated successfully"})
    finally:
        connection.close()

@app.route('/job_search', methods=['GET']) ###직업검색  ------------------------------------------------------------------------------------
def job_search():
    connection = get_db_connection()
    sectors = request.args.get('sectors').split(',') if request.args.get('sectors') else []
    regions = request.args.get('regions').split(',') if request.args.get('regions') else []
    keyword = request.args.get('keyword')
    contract = request.args.get('contract')
    size = request.args.get('size')
    korean = request.args.get('korean')
    duedate = request.args.get('duedate')
    career = request.args.get('career')
    occAll = request.args.get('occAll')
    regAll = request.args.get('regAll')
    lang = request.args.get('lang')  # 언어 코드 추가

    # 언어 코드에 따라 title 필드 설정
    field_map = {
        'ko_kr': 'title_ko',
        'en_us': 'title_en',
        'zh_cn': 'title_zh',
        'vi_vn': 'title_vi',
        'th_th': 'title_th',
        'ru_ru': 'title_ru',
        'my_my': 'title_my'
    }

    # lang 값이 유효한지 확인
    if lang not in field_map:
        return jsonify({"error": "Invalid language code"}), 400

    title_selected_field = field_map[lang]

    try:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT job_content.{title_selected_field} AS title_selected,
                   job.id, job.contract, job.occ, job.sector, job.always,
                   job.career, job.korean, job.size, job.c_name,
                   job.pay, job.typeSal, job.minSal, job.maxSal, job.job_code
            FROM job
            INNER JOIN job_content ON job.id = job_content.job_id
            """

            tupleList = []
            sqlList = []

            if occAll != '네':
                if sectors:
                    # 각 3자리 검색 코드에서 앞 두 자리만 추출하여 조건문 생성
                    sql_conditions = [f"LEFT(job.job_code, 3) = %s" for _ in sectors]

                    # 조건들을 OR로 결합
                    sqlList.append(f"({' OR '.join(sql_conditions)})")

                    # 각 섹터의 앞 두 자리를 추출하여 tupleList에 추가
                    tupleList.extend([code[:3] for code in sectors])

            if regAll != '네':
                if regions:
                    sqlList.append(f"job.region IN ({', '.join(['%s'] * len(regions))})")
                    tupleList.extend(regions)

            if keyword:
                sqlList.append(f"""
                MATCH
                (title_ko, desc_ko, title_en, desc_en, title_zh, desc_zh, title_th, desc_th, title_vi, desc_vi, title_ru, desc_ru, title_my, desc_my)
                AGAINST(%s IN BOOLEAN MODE)
                """)
                tupleList.append(keyword)

            sqlList.append("job.onoff = 'yes'")

            if sqlList:
                sql += "WHERE " + " AND ".join(sqlList)

            sql += " ORDER BY job.id DESC Limit 1000"
            print(sql)

            cursor.execute(sql, tupleList)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()


@app.route('/favorite_put', methods=['POST'])   #즐겨찾기 등록---------------------------------------------------------------------
def favorite_put():
    connection = get_db_connection()
    user_id = request.form.get('user_id')
    job_id = request.form.get('job_id')

    try:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM favorite WHERE user_id = %s AND job_id = %s", (user_id, job_id))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({'message': 'User already exists', 'user': existing_user, 'succeess' : 0})

            sql = "Insert Into favorite (user_id, job_id) Value (%s, %s)"
            cursor.execute(sql, (user_id, job_id))
            connection.commit()

            return jsonify({"message": "Data posted successfully", 'succeess' : 1})
    finally:
        connection.close()


@app.route('/favorite_out', methods=['DELETE'])
def favorite_out():
    connection = get_db_connection()
    user_id = request.form.get('user_id')
    job_id = request.form.get('job_id')

    try:
        with connection.cursor() as cursor:
            sql = "Delete from favorite where user_id = %s and job_id = %s;"
            cursor.execute(sql, (user_id, job_id))
            connection.commit()

            return jsonify({"message": "Data removed successfully"})
    finally:
        connection.close()


@app.route('/favorite_list', methods=['GET'])
def favorite_list():
    connection = get_db_connection()
    user_id = request.args.get('user_id')
    try:
        with connection.cursor() as cursor:
            sql ="""
            SELECT favorite.*, job_content.title_ko, job_content.title_en, job_content.title_vi, job_content.title_th, job_content.title_zh  FROM favorite
            Inner JOIN job_content ON favorite.job_id = job_content.job_id
            WHERE favorite.user_id = %s
            """
            cursor.execute(sql, user_id)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()

@app.route('/all_jobs', methods=['GET']) // 관리자의 채용공고 관리
def all_jobs():
    connection = get_db_connection()
    user_id = request.args.get('user_id')
    source = request.args.get('source')
    onoff = request.args.get('onoff')
    is_applied = request.args.get('is_applied')  # 추가된 입력 파라미터

    try:
        with connection.cursor() as cursor:
            # 기본 쿼리
            sql = """
            SELECT
                job.id, job.source, job.onoff, job.duedate,
                job_content.title_ko,
                COUNT(applications.job_id) AS applicants_count
            FROM
                job
            LEFT JOIN
                applications ON job.id = applications.job_id
            INNER JOIN
                job_content ON job.id = job_content.job_id
            WHERE 1=1  -- 항상 참인 조건으로 시작
            """

            # is_applied에 따라 JOIN 방식 결정
            if is_applied == '아니오':
                # LEFT JOIN 사용
                pass  # LEFT JOIN 이미 사용 중이므로 추가 작업 없음
            else:
                # INNER JOIN 사용
                sql = sql.replace("LEFT JOIN", "INNER JOIN", 1)

            # user_id가 None이 아닐 경우 조건 추가
            if user_id:
                sql += " AND job.user_id = %s"
            else:
                sql += " AND job.user_id IS NOT NULL"  # user_id가 NULL인 경우 조건 제거

            # source가 None이 아닐 경우 조건 추가
            if source:
                sql += " AND job.source = %s"
            else:
                sql += " AND job.source IS NOT NULL"  # source가 NULL인 경우 조건 제거

            # onoff가 None이 아닐 경우 조건 추가
            if onoff:
                sql += " AND job.onoff = %s"
            else:
                sql += " AND job.onoff IS NOT NULL"  # onoff가 NULL인 경우 조건 제거

            sql += " GROUP BY job.id, job_content.title_ko"
            sql += " Limit 100;"

            # 쿼리 실행 시 파라미터를 리스트 형태로 전달
            params = []
            if user_id:
                params.append(user_id)
            if source:
                params.append(source)
            if onoff:
                params.append(onoff)

            cursor.execute(sql, params)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    