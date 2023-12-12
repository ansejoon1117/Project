from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Example : 파리
# Chrome WebDriver 인스턴스 초기화
driver = webdriver.Chrome()

# 웹 사이트로 이동
driver.get('https://kr.trip.com/travel-guide/europe-120002/')
time.sleep(3)

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 페이지의 특정 요소 클릭
paris_click = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[1]/div/i').click()
paris_best = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[4]/div[2]/div[3]/div/div[2]/div').click()

# 새 창으로 전환
driver.switch_to.window(driver.window_handles[1])

# 데이터를 저장할 리스트 초기화
paris_name = []
paris_address = []

# 페이지 및 요소 반복
for page in range(2, 5):
    # 페이지 내 요소 클릭
    elements = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/ul/li[%d]' % page).click()
    time.sleep(3)
    
    # 페이지 내 각 요소에 대해 반복
    for i in range(1, 6):
        try:
            # 요소 클릭
            driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[%d]' % i).click()
            time.sleep(2)
            
            # 새 창으로 전환
            driver.switch_to.window(driver.window_handles[2])
            
            try:
                # 다양한 XPath로 요소 찾기
                element1_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div[3]/div[1]/div[1]/div/div[1]/h1'
                element1 = driver.find_element_by_xpath(element1_xpath)
                
                element2_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/div[2]/div/div[1]/div[3]/div/div/div/div/div/span[1]'
                element2 = driver.find_element_by_xpath(element2_xpath)
                
            except:
                # 다양한 XPath로 요소 찾기
                try:
                    element1_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div/div[1]/div/div[1]/h1'
                    element1 = driver.find_element_by_xpath(element1_xpath)
                    
                    element2_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div/div/span[1]'
                    element2 = driver.find_element_by_xpath(element2_xpath)
                    
                except:
                    # 다양한 XPath로 요소 찾기
                    try:
                        element2_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div[3]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div/div/span[1]'
                        element2 = driver.find_element_by_xpath(element2_xpath)
                        
                    except:
                        # 다양한 XPath로 요소 찾기
                        try:
                            element2_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div/span[1]'
                            element2 = driver.find_element_by_xpath(element2_xpath)
                            
                        except:
                            element2_xpath = '/html/body/div[2]/div[1]/div[2]/div/div[4]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/span[1]'
                            element2 = driver.find_element_by_xpath(element2_xpath)
            
            # 텍스트 값을 추출하고 리스트에 추가
            value1 = element1.text
            value2 = element2.text
            paris_name.append(value1)
            paris_address.append(value2)
            
            # 시간 대기 후 창 닫기
            time.sleep(2)
            driver.close()
            
            # 기본 창으로 전환
            driver.switch_to.window(driver.window_handles[1])
            
        except:
            # 예외 발생 시 무시하고 계속 진행
            pass

# 최종 결과 출력
print(paris_address)
