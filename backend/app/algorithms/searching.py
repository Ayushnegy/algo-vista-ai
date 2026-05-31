from __future__ import annotations

from typing import List, Optional


def linear_search(arr: List[int], target: int) -> Optional[int]:
    for i, x in enumerate(arr):
        if x == target:
            return i
    return None


def binary_search(arr: List[int], target: int) -> Optional[int]:
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None

