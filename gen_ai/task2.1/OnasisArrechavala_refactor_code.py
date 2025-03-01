class Solution:
    def get_digit_square_sum(self, num: int) -> int:
        """Returns the sum of the squares of the digits of num."""
        return sum(int(digit) ** 2 for digit in str(num))

    def isHappy(self, n: int) -> bool:
        """Determines if a number is a happy number."""
        seen_numbers = set()

        while n not in seen_numbers:
            seen_numbers.add(n)
            n = self.get_digit_square_sum(n)
            if n == 1:
                return True
        
        return False
