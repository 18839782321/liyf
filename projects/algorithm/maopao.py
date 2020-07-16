# coding: utf8
# _author: Liyf
# date: 2020/6/22

"""
原理：比较相邻的元素，如果第一个比第二个大，就交换它们两个的位置；
对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对，这样在最后的元素应该会是最大的数；
针对所有的元素重复以上的步骤，除了最后一个；
"""


def bubbleSort1(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp
    return arr


arr1 = [1, 2, 4, 3, 5, 3, 5, 6, 9, 7, 8]
res1 = bubbleSort1(arr1)
print(res1)


# 冒泡排序就是比较，交换位置，一般认为时间复杂度都是O(n2)，查了一下也可以优化代码，设置一个flag来减少比较次数，使最快时间复杂度可以到O(n)。

def bubbleSort2(arr):
    k = len(arr) - 1
    # 设置pos位置标记，j后面没有进行排序，pos=j，下一趟扫描就只循环到pos
    pos = 0
    for i in range(len(arr) - 1):
        # 设置flag标记,如果发生了交换flag=1
        flag = 0
        for j in range(k):
            if arr[j] > arr[j + 1]:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp
                flag = 1
                pos = j
        k = pos
        # 没有发生交换就推出循环
        if flag == 0:
            break
    return arr


arr2 = [1, 2, 4, 3, 5, 3, 5, 6, 9, 7, 8]
res2 = bubbleSort2(arr2)
print(res2)

