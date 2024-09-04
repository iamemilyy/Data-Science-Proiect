import csv
import os

# 욕설 단어 리스트 정의
bad_words = ['욕설1', '욕설2']  # 필요에 따라 추가

# 'bad_words.csv' 파일 생성
with open('bad_words.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['욕설', '***'])  # 파일의 첫번째 행에 헤더값 지정
    writer.writerow(['-' * 3, '-' * 3])  # 헤더와 데이터 구분
    for word in bad_words:
        writer.writerow([word, '*' * len(word)])


# 욕설 단어와 필터링된 단어가 저장된 CSV파일을 불러와 딕셔너리로 저장하는 함수
def load_bad_words(filename):
    bad_words = {}
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        try:
            bad_words = {row[0]: row[1] for row in reader}
        except IndexError:
            print("CSV 파일의 열 개수가 예상보다 적습니다.")
            return {}
    return bad_words

# 문장에 욕설이 포함되어 있는지 확인 후 필터링된 문장을 반환하는 함수
def filter_sentence(sentence, bad_words):
    words = sentence.split()
    filtered_words = []
    for word in words:
        if word in bad_words:
            filtered_word = '*' * len(word)
            filtered_words.append(filtered_word)
        else:
            filtered_words.append(word)
    filtered_sentence = ' '.join(filtered_words)
    return filtered_sentence

# load_bad_words 함수 사용
bad_words_dict = load_bad_words('bad_words.csv')

# 필터링할 CSV 파일들의 경로를 csv_file에 리스트로  저장
csv_files = [
    r'free_board_crawling.csv',
    r'secret_board_crawling.csv',
    r'grad_board_crawling.csv'
]

# csv_file 리스트의 각 파일을 순회하며 욕설 필터링 적용
for csv_file in csv_files:
    filtered_data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)

        # 첫 번째 행은 그대로 유지
        header_row = next(reader)
        filtered_data.append([header_row[0], header_row[2], header_row[3]])  # 두 번째 열을 제외하고 세 번째와 네 번째 열 데이터만 추가

        # 두 번째 행부터 필터링 수행
        for row in reader:
            filtered_row = [row[0]]  # 첫 번째 열 추가
    
            # 세 번째(title) 열 필터링
            filtered_sentence = filter_sentence(row[2], bad_words_dict)  # filter_sentence 함수 사용
            if '*' in filtered_sentence:
                filtered_row.append(filtered_sentence)
    
            # 네 번째(body) 열 필터링
            filtered_sentence = filter_sentence(row[3], bad_words_dict)  # filter_sentence 함수 사용
            if '*' in filtered_sentence:
                filtered_row.append(filtered_sentence)

            # 필터링된 행을 filtered_data 리스트에 추가
            if len(filtered_row) > 1:
                filtered_data.append(filtered_row)
             
    # 필터링된 데이터를 새로운 CSV 파일로 저장
    file_name = os.path.basename(csv_file)
    filtered_file = f'filtered_{file_name}'
    with open(filtered_file, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_data)
