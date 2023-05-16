import heapq

class PriorityQueue:
    def __init__(self, length):
        self.heap = []
        self.length = length
        heapq.heapify(self.heap)

    def push(self, touple):
        if len(self.heap) < self.length:
            heapq.heappush(self.heap, touple)
        else:
            heapq.heappushpop(self.heap, touple)

    def getAll(self):
        return sorted(self.heap, reverse=True)
