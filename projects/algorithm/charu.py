# coding: utf8
# _author: Liyf
# date: 2020/6/22

"""
从未排序的元素中依次向已排序数组插入。
1.从第一个元素开始，该元素可以认为已经被排序；
2.取出下一个元素，在已经排序的元素序列中从后向前扫描；
3.如果该元素（已排序）大于新元素，将该元素移到下一位置；
4.重复步骤3，直到找到已排序的元素小于或者等于新元素的位置；
5.将新元素插入到该位置后；
6.重复步骤2~5
"""


def insertionSort(arr):
    for i in range(1, len(arr)):
        preIndex = i - 1
        current = arr[i]
        # 从已排序的数组最后一个元素开始比较，依次向前，找到位置后插入
        while preIndex >= 0 and arr[preIndex] > current:
            arr[preIndex + 1] = arr[preIndex]
            preIndex -= 1
        arr[preIndex + 1] = current
    return arr


arr = [9, 7, 8, 3, 5, 6, 4, 1, 2, 0]
res = insertionSort(arr)
print(res)
