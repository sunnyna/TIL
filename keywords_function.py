import numpy as np
import math

import requests
from bs4 import BeautifulSoup

from konlpy.tag import Mecab


def get_news_by_url(url):
    res = requests.get(url)
    bs = BeautifulSoup(res.content, "html.parser")

    title = bs.select("h3#articleTitle")[0].text  # 제목
    content = bs.select("#articleBodyContents")[0].get_text().replace("\n", " ")  # 본문
    content = content.replace(
        "// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", ""
    )
    return content.strip()


def gen_indices(vocab):
    vocab2idx = {vocab[i]: i for i in range(0, len(vocab))}  # vocab을 인덱스로 변환
    idx2vocab = {i: vocab[i] for i in range(0, len(vocab))}  # 인덱스를 vocab으로 변환
    return vocab2idx, idx2vocab


def get_weighted_edge(tokens, vocab, window_size, vocab2idx, idx2vocab):

    vocab_len = len(vocab)

    # 토큰별로 그래프 edge를 Matrix 형태로 생성
    weighted_edge = np.zeros((vocab_len, vocab_len), dtype=np.float32)

    # 각 토큰 노드별로 스코어 1로 초기화
    score = np.ones((vocab_len), dtype=np.float32)

    # coocurrence를 판단하기 위한 window 사이즈 설정
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

    return score, weighted_edge


def calc_score(
    score, max_iteration, damping_factor, threshold, weighted_edge, vocab_len
):
    for iter in range(0, max_iteration):
        prev_score = np.copy(score)

        for i in range(0, vocab_len):
            summation = 0
            for j in range(0, vocab_len):
                if weighted_edge[j][i] != 0:
                    summation += weighted_edge[j][i] * score[j]

            score[i] = (1 - damping_factor) + damping_factor * (summation)

        if np.sum(np.fabs(prev_score - score)) <= threshold:  # convergence condition
            break

    sorted_index = np.flip(np.argsort(score), 0)
    return sorted_index


if __name__ == "__main__":
    mecab = Mecab()
    doc = get_news_by_url(
        "https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=018&aid=0004430108"
    )

    nodes = [
        token for token in mecab.pos(doc) if token[1] in ["NNG", "NNP"]
    ]  # NNG, NNP를 스코어 계산 대상(노드)로 제한
    tokens = [token for token in mecab.pos(doc)]  # 탐색할 토큰 전체

    vocab = nodes

    vocab2idx, idx2vocab = gen_indices(vocab)
    score, weighted_edge = get_weighted_edge(tokens, vocab, 2, vocab2idx, idx2vocab)
    sorted_index = calc_score(score, 50, 0.85, 0.0001, weighted_edge, len(vocab))

    n = 4

    print("\n=== 핵심키워드 ===")
    for i in range(0, n):
        print(str(idx2vocab[sorted_index[i]]) + " : " + str(score[sorted_index[i]]))

