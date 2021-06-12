import heapq

class MyTuple:

    def __init__(self, a, b):
        self.a=a
        self.b=b


    def __lt__(self, other):
    	return self.a < other.a

    def __getitem__(self, i):
    	return self.a if i==0 else self.b

import sys

INF = sys.maxsize

class Vertex:
	__slots__ = '_element'

	def __init__(self, x):
		self._element = x

	def element(self):
		return self._element

	def __hash__(self):
		return hash(id(self)) # allow vertex to be a map/set key

class Edge:
	__slots__ = '_origin', '_destination', '_element'

	def __init__(self, u, v, x):
		self._origin = u
		self._destination = v
		self._element = x

	def endpoints(self):
		return (self._origin, self._destination)

	def opposite(self, v):
		return self._destination if v is self._origin else self._origin

	def element(self):
		return self._element

	def __hash__(self):
		return hash((self._origin, self._destination))


class Graph(object):
	
	def __init__(self, digraph=True):
		
		self._outgoing = {}
		self._incoming = {} if digraph else self._outgoing


	def make_graph(self, filename):
		graph_edges = []
		with open(filename) as fhandle:
			for line in fhandle:
				edgeFrom, edgeTo, cost, *_ = line.strip().split(',')
				graph_edges.append((edgeFrom, edgeTo, float(cost)))

		for edgeFrom, edgeTo, cost in graph_edges:
			u = self.insert_vertex(edgeFrom)
			v = self.insert_vertex(edgeTo)
			self.insert_edge(u, v, cost)


	def is_directed(self):
		return self._incoming is not self._outgoing

	def insert_vertex(self, x=None):
		v = Vertex(x)
		self._outgoing[v] = {}
		if self.is_directed():
			self._incoming[v] = {}
		return v

	def vertices(self):
		return self._outgoing.keys()

	def insert_edge(self, u, v, x=None):
		e = Edge(u,v, x)
		self._outgoing[u][v] = e
		self._incoming[v][u] = e

	def get_edge(self, u, v):
		return self._outgoing[u].get(v)

	def get_vertex(self, u):
		for node in self._outgoing:
			if u == node.element():
				return node
		return None
	
	def getWeight(self, u, v):
		e = self.get_edge(u, v)
		return e.element()

	def incident_edges(self, v, outgoing=True):
		adj = self._outgoing if outgoing else self._incoming
		for edge in adj[v].values():
			yield edge


#####################################################################

	def dfs(self, u, discovered=[]):
		# Starting at vertex u
		for e in self.incident_edges(u):
			v = e.opposite(u)
			if v not in discovered:
				discovered[v] = e
				self.dfs(v , discovered)
	
	def shortestPath(self, start, end=None):
		"""
		Dijkstra algorithm
		"""	
		start = self.get_vertex(start)
		if end:
			end = self.get_vertex(end)
		# print(start)
		D = {node: INF for node in self.vertices()}
		D[start] = 0
		visited = []
		discovered = {}
		prev = {}
		unvisitedQueue = [MyTuple(D[v], v) for v in self.vertices()] # priority queue contains unvisited node and its distance

		heapq.heapify(unvisitedQueue)
		while len(unvisitedQueue):

			# Pull vertex u into the cloud
			uv = heapq.heappop(unvisitedQueue)
			current = uv[1]
			visited.append(current)

			# Relaxation procedure on adjacent edge

			for e in self.incident_edges(current):
				nextPoint = e.opposite(current)
				if nextPoint in visited:
					continue
				newDist = D[current] + self.getWeight(current, nextPoint)

				if newDist <  D[nextPoint]:
					D[nextPoint] = newDist
					discovered[nextPoint] = e
					discovered[current] = e

			# Rebuild the heap
			while len(unvisitedQueue):
				heapq.heappop(unvisitedQueue)
			unvisitedQueue = [MyTuple(D[v], v) for v in self.vertices() if v not in visited]

			heapq.heapify(unvisitedQueue)
			for v in visited:
				print(v.element())
		return prev


	def construct_path(self, u, v):
		"""
		discovered = self.shortestPath(u, v)
		path = []
		u = self.get_vertex(u)
		v = self.get_vertex(v)
		if v in discovered:
			path.append(v)
			walk = v
			while walk is not u:
				e = discovered[walk]
				walk = e.opposite(walk)
				path.append(walk)
			path.reverse()
		else:
			print("Fuck up")		
		"""

	def print_path(self, path):
		for point in path:
			print(point.element(),end="->")

if __name__ == '__main__':

	StartPoint = 'BWI'
	EndPoint = 'LAX'
	filename = 'input.txt'
	A = Graph(digraph=False) # this is a undirected graph
	A.make_graph(filename)

	print(f"Dijkstra's shortest path between {StartPoint} and {EndPoint} is: ")
	path = A.construct_path(StartPoint, EndPoint)
	A.print_path(path)




