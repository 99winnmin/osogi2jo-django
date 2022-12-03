import json, os

from .emotion import Emotion
from .textreader import TextReader
import time
from .word import Word
from django.http import JsonResponse, HttpResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt


keyword_detector = Word()
emotion_detector = Emotion()

@csrf_exempt
def text_analysis(request):
    if request.method == 'POST':
        # Text 분석 로직 코드 임베드 장소
        print(request.body)
        data = json.loads(request.body)
        novel_url = data['novel']
        # novel_url = 'https://www.tocsoda.co.kr/product/view?brcd=76M1912142125&epsdBrcd=76S1912866136'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # headless모드 브라우저가 뜨지 않고 실행됩니다.
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')  # 브라우저에서 이미지 로딩을 하지 않습니다.
        options.add_argument('--disable-blink-features=AutomationControlled')  # API 요청 너무 많이 되는거 처리
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(novel_url)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
            )

        novel_text = driver.find_elements(By.TAG_NAME, 'p')
        novel = ''
        for i in novel_text:
            # if i.text is not '':
            novel += i.text + '\n\n'
        driver.quit()
        print(novel)

        result_array = list()
        text_reader = TextReader(novel)
        while (True):
            texts = text_reader.read()
            if texts is None:
                break

            unit_length = int(text_reader.novel_len / 5)
            emotional_word = []
            for i in range(0, 5):
                tmp = texts[unit_length * i: unit_length * (i + 1)]
                keywords, rank = keyword_detector.get_word_from_novel(tmp, 2)  # 소설에서 단어 읽어들이기
                if (keywords == None):
                    continue
                emotion_sum = 0

                for wordname, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
                    wordname = wordname.strip(" ")
                    word, emotion = emotion_detector.data_list(wordname=wordname)  # 읽어들인 단어의 감정 분석
                    if emotion != 'None':
                        emotion_value = abs(r * int(emotion))
                        emotional_word.append((wordname, emotion_value,(text_reader.readsentence/text_reader.novel_len)*100))
                        emotion_sum += emotion_value
                        # result_array.append(dict(keyword=wordname, ratio=round((text_reader.readsentence / text_reader.novel_len) * 100)))

                if emotion_sum == 0:  # 만약 감정 단어를 추출하지 못했다면
                    # print('감정 추출 결과 없음, 빈도수 조정')
                    keywords, rank = keyword_detector.get_word_from_novel(texts, 1)  # min_count값을 1로 다시 추출함
                    for wordname, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
                        wordname = wordname.strip(" ")
                        word, emotion = emotion_detector.data_list(wordname=wordname)  # 읽어들인 단어의 감정 분석
                        if emotion != 'None':
                            emotion_value = abs(r * int(emotion))
                            emotional_word.append((wordname, emotion_value,(text_reader.readsentence/text_reader.novel_len)*100))
                            emotion_sum += emotion_value
                            # result_array.append(dict(keyword=wordname, ratio=round((text_reader.readsentence / text_reader.novel_len) * 100)))
            if (len(emotional_word) != 0):
                max_word = max(emotional_word, key=lambda x: x[1])
                result_array.append(dict(keyword=max_word[0], ratio=max_word[2]))

        print('result : ', result_array)
        result = json.dumps(result_array,ensure_ascii=False)
        return HttpResponse(result, status=200)
    else:
        return JsonResponse({"message": "error"}, status=400)