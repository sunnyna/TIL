from nltk.tokenize import sent_tokenize
from konlpy.tag import Mecab



# 문장의 가중치 계산
def get_sentence_weight (sentence , keywords):
    token_list = sentence.split(' ')
    window_start = 0;
    window_end = -1

    for i in range(len(token_list)):
      if token_list[i] in keywords:
        window_start =i
        break
    for i in range(len(token_list)-1,0,-1): # 끝에서부터시작
      if token_list[i] in keywords:
        window_end = i
        break

    if window_start > window_end:
      return 0

    window_size = window_end - window_start + 1
    keywords_cnt = 0
    for w in token_list :
      if w in keywords:
        keywords_cnt += 1

    return keywords_cnt*keywords_cnt / window_size

