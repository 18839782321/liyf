# coding: utf8
# _author: Liyf
# date: 2020/6/22

"""
快速排序的基本思想：通过一趟排序将待排记录分隔成独立的两部分，其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序；
1. 设置i，j作为指针，指向要排序数组的头尾，找一个基准，一般是数组开头。
2. 在i<j的情况下，大于基准key的交换到后面，小于key的交换到前面，直到i=j。
3. 将前后数组继续递归调用排序，直到排序完成。
"""


def quickSort(arr, start, end):
    """
    快速排序
    :param arr: 需要进行排序的列表
    :param start: 需要从列表的哪一个位置开始进行排序
    :param end: 排序截止位置
    :return:
    """
    if start < end:
        # i,j指针指向数组起始位置
        i, j = start, end
        key = arr[i]
        while i < j:
            # 小于key时，交换到前面
            while i < j and arr[j] >= key:
                j -= 1
            arr[i] = arr[j]
            while i < j and arr[i] <= key:
                i += 1
            arr[j] = arr[i]
        # 将中间的数替换为key
        arr[i] = key
        # 递归调用
        quickSort(arr, start, i - 1)
        quickSort(arr, j + 1, end)
    return arr


arr = [9, 7, 8, 3, 5, 6, 4, 1, 2, 0]

res = quickSort(arr, 0, len(arr)-1)
print(res)
