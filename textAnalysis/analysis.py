from emotion import Emotion
from textreader import TextReader
import time
from word import Word

keyword_detector = Word()
emotion_detector = Emotion()

max_unit = 150  # 문장 분석 수 / 150이 적당한 크기 같아서 임의로 설정함

start_pos = 0  # 소설 시작 위치
end_pos = start_pos + max_unit  # 소설 끝날 위치 = 시작 + 분석 수

default_min_count = 3  # 키워드 최소 빈도수

# 파일에서 읽기
novel_path = 'novel.txt'  # 5000줄로 늘림
novel = open(novel_path, 'r', encoding='utf-8').read()
print(type(novel))
result_array = []

text_reader = TextReader(novel)
while (True):
    texts = text_reader.read(200)
    if texts is None:
        break
    keywords, rank = keyword_detector.get_word_from_novel(texts, 2)  # 소설에서 단어 읽어들이기
    emotional_word = []
    emotion_sum = 0

    start = time.time()
    for wordname, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
        wordname = wordname.strip(" ")
        word, emotion = emotion_detector.data_list(wordname=wordname)  # 읽어들인 단어의 감정 분석
        if emotion != 'None':
            emotion_value = r * int(emotion)
            emotional_word.append((wordname, emotion_value))
            emotion_sum += emotion_value
            result_array.append((wordname, (text_reader.readsentence / text_reader.novel_len) * 100))
    end = time.time()

    if emotion_sum == 0:  # 만약 감정 단어를 추출하지 못했다면
        print('감정 추출 결과 없음, 빈도수 조정')
        keywords, rank = keyword_detector.get_word_from_novel(texts, 1)  # min_count값을 1로 다시 추출함
        start = time.time()
        for wordname, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:30]:
            wordname = wordname.strip(" ")
            word, emotion = emotion_detector.data_list(wordname=wordname)  # 읽어들인 단어의 감정 분석
            if emotion != 'None':
                emotion_value = r * int(emotion)
                emotional_word.append((wordname, emotion_value))
                emotion_sum += emotion_value
                result_array.append((wordname, (text_reader.readsentence / text_reader.novel_len) * 100))
        end = time.time()

print('result : ', result_array)


