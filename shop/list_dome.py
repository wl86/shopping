nums = [3, 17, 21, 15, 1, 8, 7, 200, 34, 56, 77, 12, 6, 9, 122]
'''
（1）将上述列表进行排序，正序排列产生新的列表 （列表推导）

（2）过滤出所有大于20的数据，放入新的列表    （列表推导）

(3)  编写分页函数，将上述数据列表进行分页显示

'''
nums1 = [i for i in nums if i > 20]
# def bubbleSort(nums):
#     for i in range(len(nums)-1):    # 这个循环负责设置冒泡排序进行的次数
#         for j in range(len(nums)-1):  # ｊ为列表下标
#             if nums[j] > nums[j+1]:
#                 nums[j], nums[j+1] = nums[j+1], nums[j]
#     return nums
# print(bubbleSort(nums))

nums2 = sorted(nums)

print(nums2)
def page(nums,num,size):
    '''
    分页函数
    nums[0:5]
    nums[5:10]
    nums[10:15]
    :param num: 第几页
    :param size: 一页几条数据
    :return:
    '''
    return nums[(num-1)*size:num*size]
print(page(nums,1,5))



