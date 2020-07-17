tokens = ["딸기", "바나나", "사과", "딸기", "파인애플"]
nodes = ["바나나", "사과", "파인애플", "딸기"]
vocab = nodes

vocab2idx = {vocab[i]: i for i in range(0, len(vocab))}  # vocab을 인덱스로 변환
idx2vocab = {i: vocab[i] for i in range(0, len(vocab))}  # 인덱스를 vocab으로 변환
print(idx2vocab)


import numpy as np
import math

vocab_len = len(vocab)

# 토큰별로 그래프 edge를 Matrix 형태로 생성
weighted_edge = np.zeros((vocab_len, vocab_len), dtype=np.float32)

# 각 토큰 노드별로 스코어 1로 초기화
score = np.ones((vocab_len), dtype=np.float32)

# coocurrence를 판단하기 위한 window 사이즈 설정
window_size = 2
covered_coocurrences = []

for window_start in range(0, (len(tokens) - window_size + 1)):
    window = tokens[window_start : window_start + window_size]
    for i in range(window_size):
        for j in range(i + 1, window_size):
            if (window[i] in vocab2idx.keys()) & (
                window[j] in vocab2idx.keys()
            ):  # 윈도 내 단어가 노드에 속하는 경우만 엣지로 연결
                index_of_i = window_start + i
                index_of_j = window_start + j

                if [index_of_i, index_of_j] not in covered_coocurrences:
                    weighted_edge[vocab2idx[window[i]]][vocab2idx[window[j]]] = 1
                    weighted_edge[vocab2idx[window[j]]][vocab2idx[window[i]]] = 1
                    covered_coocurrences.append([index_of_i, index_of_j])

for i in range(0, vocab_len):
    sumi = weighted_edge[i].sum()  # 각 노드별 보유한 edge 수
    weighted_edge[i] = weighted_edge[i] / sumi if sumi > 0 else 0  # edge 가중치

print(weighted_edge)


MAX_ITERATIONS = 50
d = 0.85
threshold = 0.0001  # convergence threshold

for iter in range(0, MAX_ITERATIONS):
    prev_score = np.copy(score)

    for i in range(0, vocab_len):
        summation = 0
        for j in range(0, vocab_len):
            if weighted_edge[j][i] != 0:
                summation += weighted_edge[j][i] * score[j]

        score[i] = (1 - d) + d * (summation)

    if np.sum(np.fabs(prev_score - score)) <= threshold:  # convergence condition
        break

    sorted_index = np.flip(np.argsort(score), 0)

n = 4

print("\n=== 핵심키워드 ===")
for i in range(0, n):
    print(str(idx2vocab[sorted_index[i]]) + " : " + str(score[sorted_index[i]]))

