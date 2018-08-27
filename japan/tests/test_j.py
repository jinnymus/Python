#!/usr/bin/python3

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

logger.debug("start")

def pits(A, p, q, r):
    m = min(A[p] - A[q], A[r] - A[q])
    return m

def solution(A):
    deepest = 0
    p = 0
    r = -1
    q = -1
    l = len(A)
    for i in range(0, l):
        if q<0 and A[i]>=A[i-1]:
            q = i -1
        if (q>=0 and r<0) and (A[i]<=A[i-1] or i+1==l):
            r = i-1
            deepest = max(deepest, pits(A, p, q, r))
            p = i-1
            q = -1
            r = -1
    if deepest:
        return deepest
    else:
        return -1

A = [0, 1, 3, -2, 0, 1, 0, -3, 2, 4]
print(solution(A))