class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda x: x[1] - x[0], reverse=True)
        energy  = 0   
        current = 0   
      for actual, minimum in tasks:
            if current < minimum:
                energy  += minimum - current
                current  = minimum
            current -= actual
        return energy
