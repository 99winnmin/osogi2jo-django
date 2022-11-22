from selenium import webdriver
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
options.add_argument('disable-dev-shm-usage')
options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
options.add_argument("disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.tocsoda.co.kr/product/view?brcd=76M2101153332&epsdBrcd=76S2101527508')

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "p"))
    )

novel_text = driver.find_elements(By.TAG_NAME,'p')
print(type(novel_text))
str = ''
for i in novel_text:
    # if i.text is not '':
    str += i.text+'\n'
# print(novel)
# print(type(novel))
print(str)
driver.quit()