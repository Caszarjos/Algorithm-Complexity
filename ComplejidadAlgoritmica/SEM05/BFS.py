# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.

from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

	# Constructor
	def __init__(self):

		# Default dictionary to store graph
		self.graph = defaultdict(list)

	# Function to add an edge to graph
	def addEdge(self, u, v):
		self.graph[u].append(v)

	# Function to print a BFS of graph
	def BFS(self, s):

		# Mark all the vertices as not visited
		visited = [False] * (max(self.graph) + 1)

		# Create a queue for BFS
		queue = []

		# Mark the source node as
		# visited and enqueue it
		queue.append(s)
		visited[s] = True

		while queue:

			# Dequeue a vertex from
			# queue and print it
			s = queue.pop(0)
			print(s, end=" ")

			# Get all adjacent vertices of the
			# dequeued vertex s. If a adjacent
			# has not been visited, then mark it
			# visited and enqueue it
			for i in self.graph[s]:
				if visited[i] == False:
					queue.append(i)
					visited[i] = True


# Driver code
'''
Generic Function for BFS traversal of a Graph
(valid for directed as well as undirected graphs
which can have multiple disconnected components)
-- Inputs --
-> V - represents number of vertices in the Graph
-> adj[] - represents adjacency list for the Graph
-- Output --
-> bfs_traversal - a vector containing bfs traversal
for entire graph
'''


def bfsOfGraph(V, adj):

	bfs_traversal = []
	vis = [False]*V
	for i in range(V):

		# To check if already visited
		if (vis[i] == False):
			q = []
			vis[i] = True
			q.append(i)

			# BFS starting from ith node
			while (len(q) > 0):
				g_node = q.pop(0)

				bfs_traversal.append(g_node)
				for it in adj[g_node]:
					if (vis[it] == False):
						vis[it] = True
						q.append(it)

	return bfs_traversal

# This code is contributed by Abhijeet Kumar(abhijeet19403)

if __name__ == '__main__':

	# Create a graph given in
	# the above diagram
	g = Graph()
	g.addEdge(0, 1)
	g.addEdge(0, 2)
	g.addEdge(1, 2)
	g.addEdge(2, 0)
	g.addEdge(2, 3)
	g.addEdge(3, 3)
	g.addEdge(4, 1)
	g.addEdge(3, 4)

	print("Following is Breadth First Traversal"
		" (starting from vertex 2)")
	g.BFS(0)

# This code is contributed by Neelam Yadav
