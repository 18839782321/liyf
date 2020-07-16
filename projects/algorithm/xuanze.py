# coding: utf8
# _author: Liyf
# date: 2020/6/22

"""
原理：选择排序就是选择最小的元素和第一个交换。将n个元素的数组第一个元素默认为最小值min，从后面的元素中选择最小值与min比较大小，交换。然后将第二个元素设置为min，继续比较交换。
"""


def selectionSort(arr):
    for i in range(len(arr)):
        min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min]:
                min = j
        # 交换顺序
        temp = arr[i]
        arr[i] = arr[min]
        arr[min] = temp
    return arr


arr = [9, 7, 8, 3, 5, 6, 4, 1, 2, 0]
res = selectionSort(arr)
print(res)
