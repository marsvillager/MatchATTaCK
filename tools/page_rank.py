import numpy as np
import pandas as pd
import re

from tools.config import Config


def find_all(regex, text):
    """
    Solve the problem that function re.search() only returns one result, so here will return all results.

    :param regex: match rules
    :param text: origin text
    :return: match results
    """
    match_list: list = []
    while True:
        match = re.search(regex, text)
        if match:
            match_list.append(match.group(0))
            text = text[match.end():]
        else:
            return match_list


def build_matrix(format_list: pd.DataFrame) -> np.ndarray:
    """
    Transform mitre att&ck into matrix, matrix[i][j] = 1 if attack i mentions/refers attack j, in other words out links.

    :param format_list: processed data of mitre att&ck data
    :return: adjacent matrix of mitre att&ck
    """
    with open(Config.DEPRECATED_LIST) as f:
        deprecated_list: str = f.read().lower()

    n: int = format_list.shape[0]

    ids: dict = {}
    for i in range(n):
        ids[format_list.loc[i, "id"].lower()] = i

    matrix: np.ndarray = np.zeros((n, n))
    pattern: str = r'\b(t1|t0)\w*\b'
    for i in range(n):
        words: str = str(format_list.loc[i, "name"]) + " " + \
                     str(format_list.loc[i, "description"]) + " " + \
                     str(format_list.loc[i, 'detects'])
        out_links: list = find_all(pattern, words)
        for out_link in out_links:
            if out_link not in deprecated_list:  # deprecated item will not be considered
                matrix[i, ids[out_link]] = 1

    # Find the indices of non-zero elements
    # row_indices, col_indices = np.nonzero(matrix)

    # Print the non-zero elements and their indices
    # for i, j in zip(row_indices, col_indices):
    #     print(f"matrix[{i}, {j}] = {matrix[i, j]}")

    return matrix


def pagerank(adj_matrix: np.ndarray, d=0.85, max_iter=100, tol=1e-6) -> np.ndarray:
    """
    Consider the issue of hyperlink by ranking the importance of webpages in a directed graph.

    :param adj_matrix: directed, where adj_matrix[i][j] is 1 if there is a hyperlink from webpage i to webpage j,
                       and 0 otherwise.
    :param d: damping factor, usually set to 0.85
    :param max_iter: maximum number of iterations
    :param tol: tolerance level convergence of the PageRank algorithm, 1e-6 is a common default value for many
                iterative algorithms
    :return: score vector of pagerank
    """
    N: int = adj_matrix.shape[0]

    # 若要根据邻接矩阵计算某网页出链, 则需要对邻接矩阵的该行求, 注意无出链情况下为了防止分母为 0 也为了防止 Dead Ends 问题, 需要将分母加一平滑
    out_degree: np.ndarray = np.sum(adj_matrix, axis=1)
    out_degree[out_degree == 0] += 1

    score = np.ones(N) / N
    for i in range(max_iter):
        # Pr = M * V, M = adj_matrix.T, V = score / out_degree
        new_score = (1 - d) / N + d * adj_matrix.T.dot(score / out_degree)
        if np.linalg.norm(new_score - score) < tol:
            break
        score = new_score
    return score
