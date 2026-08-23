def merge(left, right, key):
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
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    return merge(left, right, key)