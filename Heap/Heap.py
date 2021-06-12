import sys
from os import path
if(path.exists('input.txt')):
    sys.stdin = open("input.txt","r")
    sys.stdout = open("output.txt","w")

class PriorityQueueBase:
	"""
	Abstract base class for a priority queue
	"""
	class _Item:
	    __slots__ = '_key', '_value'

	    def __init__(self, k, v):
	      self._key = k
	      self._value = v

	    def __lt__(self, other):
	      return self._value < other._value    # compare items based on their values

	    def __repr__(self):
	      return '({0},{1})'.format(self._key, self._value)
	
  
class HeapPriorityQueue(PriorityQueueBase):

	"""A min oriented priority queue implemented with a binary heap"""
	#__________________________non public behaviour______________________
	def _parent(self, j):
		return (j-1)//2
	def _left(self, j):
		return 2*j + 1
	def _right(self, j):
		return 2*j + 2
	def _has_left(self, j):
		return self._left(j) < len(self._data)
	def _has_right(self, j):
		return self._right(j) < len(self._data)
	
	def _swap(self, i, j):
		"""swap the elements at indices i and j of array"""
		self._data[i], self._data[j] = self._data[j], self._data[i]
	
	def _upheap(self, j):
		parent = self._parent(j)
		if j>0 and self._data[j] <  self._data[parent]:
			self._swap(j, parent)
			self._upheap(parent)
	
	def _downheap(self, j):
		if self._has_left(j):
			left = self._left(j)
			small_child = left
			if self._has_right(j):
				right = self._right(j)
				if self._data[right] < self._data[left]:
					small_child = right
			if self._data[small_child] < self._data[j]:
				self._swap(small_child, j)
				self._downheap(small_child)
	
	def _heapify(self):
		start = self._parent(len(self._data) - 1)
		for j in range(start, -1, -1):
			self._downheap(j)

	#________________________public behaviour_____________________
	def __init__(self, contents):
		"""
		Create new PQ with data in contents = [ (key, value)]
		"""
		contents = [(k,v) for k,v in enumerate(contents)]
		self._data = [self._Item(k, v) for k, v in contents]
		if len(self._data) > 1:
			self._heapify()

	def __len__(self):
		return len(self._data)

	def add(self, key, value):
		"""Add a key-value pair to the PQ
		O(logn)
		"""
		self._data.append(self._Item(key, value))
		self._upheap(len(self._data) - 1)

	def min(self):
		if self._data == 0:
			raise Empty("Priority Queue is empty")
		else:
			item = self._data[0]
			return (item._key, item._value)

	def remove_min(self):
		"""
		O(logn)
		"""
		if self.is_empty():
			raise Empty("Priority Queue is empty")
		else:
			self._swap(0, len(self._data) - 1)
			item = self._data.pop()
			self._downheap(0)
			return (item._key, item._value)
	
	def show_heap(self):
		print("Our current heap:")
		for item in self._data:
			print(item._value, end=' ')

arr = [4,5,2,7,9,1,3]
H = HeapPriorityQueue(arr)
H.show_heap()



