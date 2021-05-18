import time

# This is the implementation of Pattern Searching Algorithms

class PatternSearching():
	def __init__(self, T, p):
		self.text = T # text
		self.pattern = p # pattern

	# Find pattern p in text t
	
	def BoyerMoore(self):
		T = self.text
		p = self.pattern

		n,m = len(T), len(p)
		if m==0:
			return 0
		k = m-1 # for scanning p. Can be seen as the first miss match
		i = m-1 # for scanning t
		
		last = {} # Table for last occurence:
		for k in range(m):
				last[p[k]] = k

		while i<n:	

			if T[i] == p[k]:
				if k==0:
					return i
				else:
					i -= 1
					k -= 1
			else:
				j = last.get(T[i], -1)
				i += m - min(k, j+1)
				k = m-1
		return -1


	def compute_kmp_fail(self): 
		"""
		Failure function for kmp algorithm:
		Return the length of the longest prefix of the string which is suffix also
		"""
		p = self.pattern
		fail = [0]*len(p)
		i, j = 1, 0
		while i < len(p):
			if p[i] == p[j]:
				fail[i] = j + 1
				i += 1
				j += 1
			elif j > 0:
				j = fail[j-1] 
			else:
				i += 1
		return fail

	def KMP(self):
		T = self.text
		p = self.pattern
		n, m = len(T), len(p)
		if m==0:
			return 0
		fail = self.compute_kmp_fail()
		i = 0 # index for text
		k = 0 # index for pattern
		while i<n:
			if T[i] == p[k]:
				if k==m-1:
					return i - m + 1
				else:
					i += 1
					k += 1
			else:
				if k>0 : k = fail[k-1] # reuse the suffix of p[0:k]
				else:
					i +=1
		return -1






##############################################
import sys
from os import path
if(path.exists('input.txt')):
    sys.stdin = open("input.txt","r")
    sys.stdout = open("output.txt","w")
##############################################

# TEST
t = input().strip()
p = input().strip()

PM = PatternSearching(t, p)
print("Failure function", PM.compute_kmp_fail())

start_time = time.time()
print(f"Result find with BoyerMoore: {PM.BoyerMoore()}")
print("Expected: 10")
print(f"Time execution: {round(time.time() - start_time, 6)} seconds ")

print("------------------------------------")

start_time = time.time()
print(f"Result find with KMP: {PM.KMP()}")
print("Expected: 10")
print(f"Time execution: {round(time.time() - start_time, 6)} seconds")

