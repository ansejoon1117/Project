# 필요한 라이브러리 임포트
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cx_Oracle

# Oracle 데이터베이스에 연결
conn = cx_Oracle.connect('system/0000@localhost:1521/orcl')  # 실제 오라클 DB 연결 정보로 수정해주세요.
cursor = conn.cursor()

# 출발지와 도착지 지역을 사용자로부터 입력받음
origin_region = input("출발지 지역을 입력하세요: ")
destination_region = input("도착지 지역을 입력하세요: ")

# 지정된 출발지 지역에 대한 공항 코드를 가져옴
query_origin = f"SELECT 공항코드 FROM BIGDATA.AIRPORTCODE WHERE 공항 = '{origin_region}'"
cursor.execute(query_origin)
origin_code = cursor.fetchone()

# 지정된 도착지 지역에 대한 공항 코드를 가져옴
query_destination = f"SELECT 공항코드 FROM BIGDATA.AIRPORTCODE WHERE 공항 = '{destination_region}'"
cursor.execute(query_destination)
destination_code = cursor.fetchone()

# Oracle 연결 종료
conn.close()

# 출발지와 도착지의 공항 코드를 이용해 동적으로 URL 생성
if origin_code is not None and destination_code is not None:
    url = f'https://flight.naver.com/flights/international/{origin_code[0]}-{destination_code[0]}-20240124/{destination_code[0]}-{origin_code[0]}-20240213?adult=1&fareType=Y'

    # Chrome WebDriver를 headless 모드로 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # WebDriver를 사용하여 브라우저를 열고 페이지를 로드
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 지정된 요소가 나타날 때까지 대기하기 위해 WebDriverWait 설정
    wait = WebDriverWait(driver, 50)
    element_xpath = '/html/body/div/div/div[1]/div[6]/div/div[3]/div[1]/div/button'

    # 지정된 요소가 나타날 때까지 대기
    element = wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    # 현재 페이지의 소스를 가져오기
    html = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # 페이지의 특정 버튼 클릭
    air_click = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[6]/div/div[3]/div[1]/div/button').click()

    # 페이지에서 다른 요소의 값을 찾아 출력
    element_xpath = '/html/body/div/div/div[1]/div[6]/div/div[1]/div[1]/div/div[2]/div[2]/div/i'
    element = driver.find_element_by_xpath(element_xpath)
    value = element.text
    print(value)
else:
    print("지정된 지역에 대한 공항 코드를 찾을 수 없습니다.")
