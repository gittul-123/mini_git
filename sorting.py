def merge(left, right, key):
    """이미 정렬된 두 리스트(left, right)를 맨 앞 원소끼리 비교하며
    하나의 정렬된 리스트로 합친다.

    <= 비교를 사용해, 값이 같을 때 항상 left(원래 앞쪽) 원소를 먼저
    꺼내므로 안정 정렬이 유지된다.
    """
    result = []
    while left and right:
        if key(left[0]) <= key(right[0]):
            result.append(left[0])
            left = left[1:]
        else:
            result.append(right[0])
            right = right[1:]
    return result + left + right


def merge_sort(items, key):
    """리스트를 절반으로 재귀적으로 분할하다가, 원소가 1개 이하가 되면
    이미 정렬된 것으로 보고 merge()로 다시 합쳐 정렬한다.

    시간복잡도: 평균/최악 모두 O(n log n) (입력 상태와 무관하게 일정)
    안정 정렬(Stable): 예 — merge()에서 <= 비교를 사용해 같은 값일 때
    원래 순서(왼쪽에 있던 것)를 유지한다.
    """
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    return merge(left, right, key)