from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
from konlpy.tag import Okt
import re
import numpy as np
import pandas as pd

grad_df = pd.read_csv(r'grad_board_crawling.csv')

# 데이터 전처리 함수
def preprocess_text(text):
    okt = Okt()
    text = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z\s]", "", text)
    words = okt.morphs(text, stem=True)  # 형태소 분석
    
    stop_words = ['불용어1', '불용어2']  # 필요에 따라 불용어 추가 또는 수정
    words = [word for word in words if word not in stop_words]
    
    return ' '.join(words)

# 명사 추출 및 전처리
okt = Okt()
nouns = []
for text in grad_df['text']:
    nouns.extend(okt.nouns(text))

words = [n for n in nouns if len(n) > 1]  # 단어의 길이가 1개인 것은 제외(불용어 제거 목적)
words = [preprocess_text(word) for word in words]

c = Counter(words)

# 워드클라우드 원모양 변경
img = Image.open(r'circle.png')
imgArray = np.array(img)

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path=r"malgun.ttf",
    width=500, height=500, max_font_size=200, background_color='white', mask=imgArray
).generate_from_frequencies(c)

# 출력
plt.figure()
plt.imshow(wordcloud)
plt.axis('off')
plt.show()