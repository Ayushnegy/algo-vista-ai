from __future__ import annotations

import heapq
from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr: List[int]) -> List[int]:
    a = list(arr)
    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    merged: List[int] = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def heap_sort(arr: List[int]) -> List[int]:
    a = list(arr)
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]


def quick_sort(arr: List[int]) -> List[int]:
    # Recursion-based quicksort (used only for small benchmark sizes).
    a = list(arr)
    if len(a) <= 1:
        return a

    pivot = a[len(a) // 2]
    left = [x for x in a if x < pivot]
    middle = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

