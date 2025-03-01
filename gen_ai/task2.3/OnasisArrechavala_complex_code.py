class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        k = 0  # Pointer for the new valid array
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]  # Overwrite elements in-place
                k += 1
        return k  # k represents the new length of nums