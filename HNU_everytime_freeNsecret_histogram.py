import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# CSV 파일 읽기
data = pd.read_csv(r'freeNsecret_board_crawling.csv')

# 시간대별 이용자 수 계산
hour_counts = data['time'].str.split(' ').str[1].str[:2].value_counts().sort_index()

#title, x축, y축 한글로 출력이 가능하게 하기
font_path = r"malgun.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 히스토그램 그리기
x_values = [str(i).zfill(2) + '시' for i in range(24)]
plt.bar(x_values, hour_counts)
plt.xlabel('시간대')
plt.ylabel('이용자 수')
plt.title('시간대별 이용자 수')
plt.xticks(rotation=40)
plt.show()