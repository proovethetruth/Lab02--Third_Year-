
def bubble_sort(input_arr):
    arr = input_arr
    for i in range(len(arr)):
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr

def merge_sort(arr):
    if(len(arr) <= 1):
        return arr

    left, right = [], []
    for i in range(len(arr)):
        if i < len(arr) // 2: 
            left.append(arr[i])
        else:
            right.append(arr[i])
        
    left = merge_sort(left)
    right = merge_sort(right)

    return final_merge(left, right)

def final_merge(left, right):
    result = []

    while len(left) != 0 and len(right) != 0:
        if left[0] <= right[0]:
            result.append(left[0])
            left.pop(0)
        else:
            result.append(right[0])
            right.pop(0)

    while len(left) != 0:
        result.append(left[0])
        left.pop(0)

    while len(right) != 0:
        result.append(right[0])
        right.pop(0)
    return result

def quick_sort(arr):
    less = []
    equal = []
    greater = []

    if len(arr) > 1:
        pivot = arr[0]
        for x in arr:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        return quick_sort(less) + equal + quick_sort(greater)
    else:
        return arr