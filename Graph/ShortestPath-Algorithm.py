import heapq
import sys

INF = sys.maxsize

from os import path
if(path.exists('input.txt')):
    sys.stdin = open("input.txt","r")
    sys.stdout = open("output.txt","w")


class Graph(object):

	def __init__(self, filename):
		graph_edges = []
		with open(filename) as fhandle:
			for line in fhandle:
				edgeFrom, edgeTo, cost, *_ = line.strip().split(',')
				graph_edges.append((edgeFrom, edgeTo, float(cost)))

		self.nodes = set()
		for edge in graph_edges:
			self.nodes.update([edge[0], edge[1]])

		self.AdjacencyList = {node: dict() for node in self.nodes}
		for edge in graph_edges:
			self.AdjacencyList[edge[0]][edge[1]] = edge[2]
			self.AdjacencyList[edge[1]][edge[0]] = edge[2]

	def getWeight(self, u, v):
		return self.AdjacencyList[u][v] 

	def shortestPath(self, start, end=None):
		"""
		Dijkstra algorithm
		"""	
		print("Dijkstra's shortest path: ")
		D = {node: INF for node in self.nodes}
		D[start] = 0
		visited = []
		prev = {}
		unvisitedQueue = [(D[v], v) for v in self.nodes]
		heapq.heapify(unvisitedQueue)
		while len(unvisitedQueue):
			uv = heapq.heappop(unvisitedQueue)
			current = uv[1]
			visited.append(current)
			print(visited)
			for nextPoint in self.AdjacencyList[current]:
				if nextPoint in visited:
					continue

				newDist = D[current] + self.getWeight(current, nextPoint)

				if newDist <  D[nextPoint]:
					D[nextPoint] = newDist
					prev[nextPoint] = current
			# Rebuild the heap
			while len(unvisitedQueue):
				heapq.heappop(unvisitedQueue)
			unvisitedQueue = [(D[v], v) for v in self.nodes if v not in visited]
			heapq.heapify(unvisitedQueue)

		if end:
			v = prev[end]	
			path =[end]
			while v != start:
				path.append(v)
				v = prev[v]
			path.append(start)			
			path = reversed(path)
			for v in path:
				print(v, '->', end='')
			print(' stop')

if __name__ == '__main__':

	filename = 'input.txt'
	A = Graph(filename)
	A.shortestPath('BWI')





