
import sys
from os import path
if(path.exists('input.txt')):
    sys.stdin = open("input.txt","r")
    sys.stdout = open("output.txt","w")

#--------------------------------------------------------------------------------
# AVL Tree implementation

class TreeNode(object):
	def __init__(self, key, value):
		self.height = 0
		self.left = None
		self.right = None
		self.key = key
		self.value = value

class AVLTree(object):
	def insert(self, root, key, value):
		if root is None:
			return TreeNode(key, value)

		if key < root.key:
			root.left = self.insert(root.left, key, value)
		else:
			root.right = self.insert(root.right, key, value)

		# update the height and balance factor of the whole tree
		root.height = max(self.getHeight(root.left), self.getHeight(root.right)) + 1	

		balancedFactor = self.getBalance(root)

		#BALANCE THE TREE
		if balancedFactor < -1: # right heavy: do left rotate or right-left rotate
			if key  > root.right.key:
				return self.leftRotate(root)
			elif key < root.right.key:
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		elif balancedFactor > 1: # left heavy: do right rotate or left-right rotate
			if key < root.left.key:
				return self.rightRotate(root)
			elif key > root.left.key:
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		return root
 
	def remove(self, root, key):
		if not root:
			return root
		elif key < root.key:
			root.left = self.remove(root.left, key)
		elif key > root.key:
			root.right = self.remove(root.right, key)
		else:
			# current root has at most one child
			if root.left is None:
				tmp = root.right
				root = None # delete node
				return tmp
			elif root.right is None:
				tmp = root.left
				root = None # delete node
				return tmp
				
			# current root has 2 child
			tmp = self.subtree_first_node(root.right)
			root.key = tmp.key
			root.right = self.delete_node(root.right, tmp.key)

		if root is None:
			return root
		
		# update the height and balance factor of the whole tree
		root.height = max(self.getHeight(root.left), self.getHeight(root.right)) + 1	

		balancedFactor = self.getBalance(root)
		
		#BALANCE THE TREE
		if balancedFactor < -1: # right heavy: do left rotate or right-left rotate
			if self.getBalance(root.right) <= 0:
				return self.leftRotate(root)
			else:
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		if balancedFactor > 1: # left heavy: do right rotate or left-right rotate
			if self.getBalance(root.left) >= 0:
				return self.rightRotate(root)
			else:
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		return root

	def leftRotate(self, z):
		y = z.right
		T2 = y.left
		y.left = z
		z.right = T2

		# update the height
		z.height = max(self.getHeight(z.left), self.getHeight(z.right)) + 1
		y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
		return y

	def rightRotate(self, z):
		y = z.left
		T3 = y.right
		y.right = z
		z.left = T3

		# update the height
		z.height = max(self.getHeight(z.left), self.getHeight(z.right)) + 1
		y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
		return y

	def getHeight(self, root):
		# if root is None:
		# 	return -1
		# return max(self.getHeight(root.left), self.getHeight(root.right)) + 1	
		if root is None:
			return -1
		return root.height

	def getBalance(self, root):
		if root is None:
			return 0
		return self.getHeight(root.left) - self.getHeight(root.right)

	def subtree_first_node(self, curr):
		if curr is None or curr.left is None:
			return curr
		return self.subtree_first_node(curr.left)

	def _inorder(self, root, lst=[]):
		if root.left:
			self._inorder(root.left, lst)
		lst.append(root.value)
		if root.right:
			self._inorder(root.right, lst)
		return lst

	def _preorder(self, root, lst=[]):
		lst.append(root.value)
		if root.left:
			self._preorder(root.left, lst)
		if root.right:
			self._preorder(root.right, lst)
		return lst
          
    #print the tree in inorder fashion: L -> Root -> R
	def print_inorder(self, root):
		global result1
		inord = self._inorder(root)
		result1 = " ".join(inord).strip()

	#print the tree in inorder fashion: Root -> L -> R
	def print_preorder(self, root):
		global result2
		preord = self._preorder(root)
		result2 = " ".join(preord).strip()

T = AVLTree()
root = None

result1 = str()
result2 = str()
while True:
    try:
        line = input().split(' ')
        if line[0] == 'quit': 
            break
        if(line[0] == 'insert'): 
            root = T.insert(root, int(line[1]), line[2])
        else: 
            root = T.remove(root, int(line[1]))    
        # print(AVLtree.root, AVLtree.size)
    except EOFError:
        break

T.print_inorder(root)
T.print_preorder(root)
print(result1.strip() + '\n')
print(result2.strip())