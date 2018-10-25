#!/usr/bin/python3

class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        i = len(nums) - 1
        while i > 0:
            if nums[i] == nums[i-1]:
                nums.pop(i)
            i -= 1
        print(nums)
        return len(nums)

    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        B=sorted(nums,key=lambda x:nums.count(x))
        return B[0]

    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if (str(x)[0] == "-"):
            x = x * (-1)
            m = -1
        else:
            m = 1

        print(-(2 ** 32))
        res = m * int(str(x)[::-1])
        if res > (2 ** 31) - 1 or res < -(2 ** 31):
            return 0
        else:
            return res

    def firstUniqChar(self, s):
        """
        :type s: str
        :rtype: int
        """
        #st = set(s)
        #l = list(s) - list(st)
        c = 2
        i = 0
        for l in s:
            c = s.count(l)
            if c == 1:
                return i
            i += 1
        return -1

        #print(s.count(s[2]))
        #return i

    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        l1 = len(set(nums))
        l2 = len(nums)
        if (l1 == l2):
            return False
        else:
            return True

    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        #print(nums[:1:])

    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        s = ''
        for i in digits:
            s += str(i)
        print(s)
        l = list()
        for n in str(int(s) + 1):
            l.append(int(n))
        return l

    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        result=list(nums1 & nums2)
        return result

s = Solution()
nums = [1,2,2,1]
nums2 = [2, 2]
my_dict = {"one":1,"two":2,"two":3}
#ln = s.removeDuplicates(nums)
#for i in range(ln):
#    print(nums[i])
#ln = s.singleNumber(nums)
#ln = s.reverse(-1563847412)
#ln = s.firstUniqChar('')
#ln = s.containsDuplicate(nums)
ln = s.intersect(nums, nums2)
#print("nums: " + str(nums))
print("ln: " + str(ln))
#print("my_dict: " + str(my_dict))