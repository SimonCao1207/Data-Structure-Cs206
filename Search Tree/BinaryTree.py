from abc import ABC, abstractmethod

class Tree(ABC):
    """Abstract base class representing a tree structure"""

    class Position(ABC):
        """Abstraction representing the location of a single element"""

        @abstractmethod
        def element(self):
            """Return the element stored at this position"""
            pass

        @abstractmethod
        def __eq__(self, other):
            """Return True if other Position represents the same location"""
            pass

        def __ne__(self, other):
            """Return True is other does not represent the same location"""
            return not (self == other)

    @abstractmethod
    def root(self):
        """Return the Position of the root (or None if it's empty) """
        pass

    @abstractmethod
    def parent(self, p):
        """return Position representing p's parent (or None if p is root)"""
        pass

    @abstractmethod
    def num_children(self, p):
        """Return the number of children that Position p has"""
        pass

    @abstractmethod
    def children(self, p):
        """Generate an iteration of Positions representing p's children (or None if p is a leave)"""
        pass

    @abstractmethod
    def __len__(self):
        """Return the total number of nodes in the tree"""
        pass

    def is_root(self, p):
        """Return True if Position of p represents the root of the tree"""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children"""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty"""
        return len(self) == 0

    def depth(self, p):
        if self.is_root(p):
            return 0
        return 1 + self.depth(self.parent(p))

    def _height1(self):
        pass

    def _height2(self, p):
        if self.is_leaf(p):
            return 0
        return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        pass



        
class BinaryTree(Tree):
    """Abstract base class representing a binary data structure"""

    @abstractmethod
    def left(self, p):
        """Return a Position representing p's left child (None if p does not have left child) """

        pass

    @abstractmethod
    def right(self, p):
        """Return a Position representing p's right child (None if p does not have right child) """

        pass

    def sibling(self, p):
        """Return a Position representing p's sibling (None if no sibling)"""

        parent = self.parent(p)
        if parent == None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of Positions representing p's children"""

        if self.left(p) is not None:
            yield self.left(p)

        if self.right(p) is not None:
            yield self.right(p)

"""---------------------------IMPLEMENTING TREEs-------------------------------------------"""

class LinkedBinaryTree(BinaryTree):
    """Linked representation of Binary Tree structure"""

    class _Node:
        __slots = '_element', '_parent', '_left', '_right'
        def __init__(self, _element, _parent=None, _left=None, _right=None):
            self._element = _element
            self._parent = _parent
            self._left = _left
            self._right = _right

    class Position(BinaryTree.Position):
        """An abstract representation of location of a single element"""

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

    def _validiate(self, p):
        """
        Return associated node, if position is valid
        """
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')

        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
            return p._node
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)"""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        """Create the empty binary tree"""
        self._root = None
        self._size = 0
        self._positions = []

    def __len__(self):
        """Return the total number of elements in the tree"""
        return self._size

    def root(self):
        """Return the root Position of the tree (None if tree is empty)"""
        return self._make_position(self._root )

    @property
    def positions(self):
        return self._positions

    def parent(self, p):
        node = self._validiate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validiate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validiate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the numbber of children of Position p"""
        node = self._validiate(p)
        count = 0
        if node._left is not None:
            count +=1
        if node._right is not None:
            count +=1
        return count

    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty
        """

        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e, None, None, None)
        pos = self._make_position(self._root)
        self._positions.append(pos)

    def _add_right(self, p, e):
        """Create a new right child for Position p storing element
        Return the Position of the new Node
        Raise ValueError if Position p is invalid or p already have a right child
        """
        node = self._validiate(p)
        if node._right is not None: raise ValueError('Right child exists')
        self._size += 1
        node._right = self._Node(e, node)
        pos = self._make_position(node._right)
        self._positions.append(pos)
        return pos

    def _add_left(self, p, e):
        """Create a new left child for Position p storing element
        Return the Position of the new Node
        Raise ValueError if Position p is invalid or p already have a left child
        """
        node = self._validiate(p)
        if node._left is not None: raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)
        pos = self._make_position(node._left)
        self._positions.append(pos)
        return pos

    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element"""
        node = self._validiate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any...
        Return the element that has been stored in at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validiate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._positions.remove(p)
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p"""
        node = self._validiate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Trees type must be match")
        self._size += t1._size + t2._size
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

    def create_tree_from_array(self, tree):
        if not tree:
            raise TypeError("Array is empty")
        else:
            self._add_root(tree[0])
            for i in range(0, len(tree) // 2):
                if not tree[i]:
                    continue
                p = self._positions[i]
                if 2 * i + 1 < len(tree) and tree[2*i + 1]:
                    self._add_left(p, tree[2 * i + 1])
                if 2 * i + 2 < len(tree) and tree[2*i + 2]:
                    self._add_right(p, tree[2 * i + 2])

    def show(self):
        for p in self._positions:
            print(p._node._element, end=' ')
        print('\n')

    def __iter__(self):
        """Generate an iteration of the tree's element"""
        for p in self._positions:
            yield p.element()

    def preorder(self):
        """Generate a preorder iteration of positions in the tree"""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        """Generate a postorder iteration of postiions in subtree rooted at p."""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def breadthfirst(self):
        """Generate a breadth-first iteration of the positions of the tree"""
        if not self.is_empty():
            visit = [self.root()]
            while not visited.empty():
                p = visited.pop(0)
                yield p
                for c in self.children(p):
                    visit.append(c)

    def _subtree_inorder(self,p):
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def inorder(self,p):
        if not self.is_empty():
            for c in self._subtree_inorder(p):
                yield c

    def inorder_next(self, v):
        """Return the position visited after v in an inorder traversal of T(or None
        if v is the last node visited)"""
        if self.num_children(v)==0:
            p = self.parent(v)
            if v is self.left(p):
                return p
            else:
                while v is not self.left(p):
                    if p is self.root():
                        return None
                    p = self.parent(p)
                    v = p
                return p
        else:
            curr = self.right(v)
            while not self.num_children(curr)==0:
                curr = self.left(v)
            return curr
    
    def print_preorder(self):
        ls = self.preorder()
        for p in ls:
            print(p.element(), end=' ')
        print('')
    
    def print_postorder(self):
        ls = self.postorder()
        for p in ls:
            print(p.element(), end=' ')
        print('')

    def print_inorder(self):
        ls = self.inorder(self.root())
        for p in ls:
            print(p.element(), end=' ')
        print('')

    def print2DUtil(self, p, space) :
        # Base case 
        if (p == None) :
            return
        # Increase distance between levels 
        space += 5
        # Process right child first 
        self.print2DUtil(self.right(p), space) 
        
        # Print current node after space 
        # count 
        print() 
        for i in range(5, space):
            print(end = " ") 
        print(p.element()) 

        # Process left child 
        self.print2DUtil(self.left(p), space) 
    
    def print2D(self):

        self.print2DUtil(self.root(), 0)


    def eulerTraversal(self, p, visited=[], Euler=[]):
        """Return Euler tour path of a binary tree at Position p"""
        if not self.is_empty():
            visited.append(p) # visit the current node
            Euler.append(p.element()) # add it to Euler path
            for c in self.children(p):
                if c not in visited:
                    self.eulerTraversal(c, visited, Euler) # Euler path for every children
                    Euler.append(p.element()) # Add current node to Euler path
        return Euler

    




