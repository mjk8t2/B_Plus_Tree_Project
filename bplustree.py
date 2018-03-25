import bcv_utilities as bcv
import ast #just for reading and writing to files
import os
from graphviz import Digraph, nohtml # from https://pypi.python.org/pypi/graphviz

# only use this if you can't figure out how to add graphviz/bin to your
# system's environment variables
# import os
# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

empty_key = "_"
empty_child = "·"
pointer = " → "

class bplustree:
  #the constructor of the B+ tree must be passed an order (3 or greater, integer),
  #and you may or may not pass it a filename corresponding to a previously exported
  #tree (if you want to import a previously-generated one for testing purposes)
  def __init__(self, order, filename = ""):
    #p = the order of the B+ tree
    self.order = order
    #index of the pop-up value in the overflowed node
    self.pop_up_index = 2*((order - 1)//2) + 1
    #tree height
    self.height = 0
    #the tree's root is initialized to a list containing just an "empty_child" character
    self.root = [empty_child]
    self.iil = []
    self.nodenum = 0
    #just import the tree from an external file during intialization if filename was given
    if filename != "":
      self.root = ast.literal_eval(bcv.rfcas(filename))
      self.calculate_height(self.root)

  #calculate the height of an already-existing B+ tree
  def calculate_height(self, alist):
    for i in alist:
      if type(i) == list:
        self.height += 1
        self.calculate_height(i)
      elif not list in alist:
        break

  #internal nodes and the root (when the root isn't a leaf) all contain
  #sublists and not the "empty_child" characters (only the leaves contain
  #empty child characters) 
  def is_leaf(self, node):
    return empty_child in node

  #calculates if the node is full as a function of the tree's order
  def is_full(self, node):
    return len(node) >= 2*self.order - 1

  #returns a list containing the key values of all the keys in the passed node
  def keys_in_node(self, node):
    keys_in_node = []
    for j in range(1, len(node), 2):
      keys_in_node.append(node[j])
    return keys_in_node

  #takes a list and fills with all the keys in current tree in increasing order
  def keys_in_tree(self, keylist, alist):
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        self.keys_in_tree(keylist, alist[i])
      elif alist[i] != empty_child and alist[i - 1] == empty_child:
        keylist.append(alist[i])

  #inserts a key into a node
  #if the node is a leaf, then adjnodes is leaf at default (empty_child, empty_child)
  #if the node is not a leaf, then adjnodes contains the left half and the
  #right half the node that was split below it (since we only insert into
  #an internal node whenever a leaf node (or possibly an internal node
  #below this node) overflows.  Hence we need to know what the left and
  #right halves of the split node are in order to insert them properly into
  #the updated internal node
  def node_insert(self, key, node, adjnodes = (empty_child, empty_child)):
    push_index = len(node) - 1
    for i in range(1, len(node), 2):
      if key <= node[i]:
        push_index = i - 1
        break
    node.insert(push_index, key)
    node.insert(push_index, adjnodes[0])
    node[push_index + 2] = adjnodes[1]

  #returns a tuple containing the left and right halves of the node that was
  #split after overflowing; the left half will ONLY include the farthest right
  #value if it's a leaf node (that's when j = 2)
  def split_node(self, node):
    j = 2 if self.is_leaf(node) else 0
    leftnode = node[:self.pop_up_index + j]
    rightnode = node[self.pop_up_index + 1:]
    return (leftnode, rightnode)

  #an easy way to insert a key into the tree
  def insert(self, key):
    if key not in self.iil: self.iil.append(key)
    self.inserthelp(key, 0, self.root, [empty_child])
            
  #is called by "insert()" to insert keys into the tree
  def inserthelp(self, key, level, node, node_above):
    #base case of the recursive call; if we've reached a leaf node, then we
    #stop making recursive calls (the last level number of the tree is
    #equal to the height
    if level != self.height:
      #key_cache just takes the current keys in the node, adds in the new
      #key that we're looking to insert, sorts it, finds the position of the
      #key in the sorted key_cache, and then uses this number to calculate
      #the index of the node that corresponds to the child where this new
      #key should be inserted
      key_cache = self.keys_in_node(node) + [key]
      key_cache.sort()
      #this is the recursive call; leafdata is the variable that corresponds
      #to the information returned from whenever the node below split
      #leafdata typically contains the value of the key that popped up from
      #the previous overflowed node, as well as the left and right halves
      #of the node that split
      #if the node didn't split, then what it contains is insignificant
      leafdata = self.inserthelp(key, level + 1, node[2*key_cache.index(key)], node)
    else:
      #since we have reached the leaf nodes here, we initialize leafdata to
      #simply include the key and a tuple of "empty_children," which essentially
      #act as NULL pointers
      leafdata = (key, (empty_child, empty_child))
    #we only consider these lines if the node below us split 
    #(hence leafdata != False/None); if it didn't split, then we're good and 
    #we just recursively traverse back up withou doing anything since 
    #everything was taken care of earlier
    if leafdata != False and leafdata != None:
      #since we're inside this block, that means that we have to insert a key
      #somewhere; so if if the node isn't full, we just insert the key into
      #the node and call it a day
      if not self.is_full(node):
        #the reason it's "leafdata[0]" and not "key" is because leafdata[0]
        #contains the key initially (when we're at the leaf), but if we're
        #at a higher level node, it will contain the value of the internal
        #node below us that popped up when it overflowed; this may not 
        #necessarily be the key
        self.node_insert(leafdata[0], node)
        return False
      #since the node we're inserting into is full and node above (parent) exists
      #and the node above is not full, then we will split the current node,
      #then insert the split nodes into the proper sublists in the parent
      #since we know that there is room
      elif not self.is_full(node_above) and node_above != [empty_child]:
        #we still have to insert the key, or the value that popped up from
        #below (leafdata[0]) into the current node first
        self.node_insert(leafdata[0], node, leafdata[1])
        #we actually split the node inside this function call, and the return
        #value is then passed to the node_insert function so that we insert
        #the split nodes, as well as the value that popped_up, into the
        #node_above (which is the current node's parent)
        self.node_insert(node[self.pop_up_index], node_above, self.split_node(node))
        return False
      #since the node we're inserting into is full then, in this case, we
      #are at the root (node_above == [empty_child]) means we're at the root)
      elif node_above == [empty_child]:
        #insert the key or previous pop_up value into the current node
        self.node_insert(leafdata[0], node, leafdata[1])
        #temporarily set the root to [empty_chlid], which is essentially NULL
        self.root = [empty_child]
        #now put the pop_up value into the root and add in the left and right
        #nodes since we know this node (previously the root) split since it was full
        self.node_insert(node[self.pop_up_index], self.root, self.split_node(node))
        #increase the tree height because we know the original root split
        self.height += 1
        return False
      #so this means that the parent exists, the current node is full, and
      #the parent is full; so now we need to return all the information that
      #comes from this node splitting so that way, when we leave the recursive
      #call, we can use this information to try all the above techniques again,
      #just one node higher
      else:
        #we still have to insert the key or previous pop_up value into this
        #node (hence leafdata[0])
        self.node_insert(leafdata[0], node, leafdata[1])
        #we need to return the pop_up value as well as the nodes that split
        #so they can properly be inserted into the parent above
        return (node[self.pop_up_index], self.split_node(node))
  #and that's it! we're done! the insertion function is complete and always
  #works; every case accounted for

  #an easy way to delete a key from the tree
  def delete(self, key):
    if key in self.iil: self.iil.remove(key)
    self.deletehelp(key, 0, False, self.root, [empty_child])

  #is called by "delete()" to remove keys from the tree
  def deletehelp(self, key, level, saw_key, node, node_above):
    #base case of the recursive call; if we've reached a leaf node, then we
    #stop making recursive calls (the last level number of the tree is
    #equal to the height
    if level != self.height:
      #while traversing, set the "saw_key" flag to indicate that this key
      #was seen in an internal node while traversing down
      if key in self.keys_in_node(node):
        saw_key = True
      #just like in the insertion function, the key_cache is used to calculate
      #the index of the sublist that holds the internal nodes that eventually
      #lead down to the leaf node where this key should be inserted
      key_cache = self.keys_in_node(node) + [key]
      key_cache.sort()
      #make the recursive call right here
      leafdata = self.deletehelp(key, level + 1, saw_key, node[2*key_cache.index(key)], node)
      #in case we removed a key from a leaf that was also in an internal node,
      #when we traverse back up and reach the node where the internal key is,
      #then we replace it with the next largest key that was in that leaf node
      #to preserve the structure of the B+ tree
      if leafdata != False:
        if key in node:
          node[node.index(key)] = leafdata
      return leafdata
    else:
      #now that we've reached a leaf, we'll initialize leafdata to a default
      leafdata = (key, (empty_child, empty_child))
    if key in node and self.is_leaf(node):
      #if the key did not appear in an internal node and there won't be an underflow
      #when we remove this key, then simply remove it and we're done
      #since this is a leaf, the underflow condition is whenever there are
      #fewer than floor(order/2) keys in the node, hence we check the count
      if not saw_key and len(self.keys_in_node(node)) > (self.order)//2:
        j = node.index(key)
        #delete the extra "empty_child" list element in addition to the key
        del node[j + 1]
        del node[j]
        return False
      #since we saw the key in the internal node, and there won't be an underflow
      #when we delete from this node, we have to return the largest remaining 
      #key in the node in order to replace the deleted key in the internal
      #node with the next largest key; this preserves the structure
      #of the B+ tree without having to collapse nodes
      if saw_key and len(self.keys_in_node(node)) > (self.order)//2:
        j = node.index(key)
        del node[j + 1]
        del node[j]
        return self.keys_in_node(node)[-1]
      #if there will be an underflow in a leaf node after deletion:
      if len(self.keys_in_node(node)) <= (self.order)//2:
        #temporarily adjust tree root and height to prepare for collapsing nodes
        self.height = 0
        self.root = [empty_child]
        #insert values in efficient way to keep B+ tree unskewed
        for i in self.iil:
          self.insert(i)

  #just a recursive function to append each level of the tree (in text form)
  #into a passed-in list; used in prettyprint and export_tree_html
  def printhelp(self, depth, stringlist, alist):
    stringlist[depth] += "["
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
          stringlist[depth] += empty_child
          self.printhelp(depth + 1, stringlist, alist[i])
      else:
        stringlist[depth] += str(alist[i])
    stringlist[depth] += "]"
    if depth == self.height:
      stringlist[depth] += pointer

  #prints the tree in an interpretible way inside the console
  def prettyprint(self):
    stringlist = [""]*(self.height + 1)
    self.printhelp(0, stringlist, self.root)
    stringlist[-1] = str(stringlist[-1][:-len(pointer)])
    for i in stringlist:
      print(i)
    print()

  #export the tree as a simple list in plain-text, to be imported later
  #via the constructor's second parameter
  def export_tree(self, filename):
    file = open(filename, "w")
    file.write(str(self.root))
    file.close()

  #export the tree in HTML using some CSS formatting so it's possible
  #to view really wide trees that would be too much for limited console width
  def export_tree_html(self, filename):
    stringlist = [""]*(self.height + 1)
    self.printhelp(0, stringlist, self.root)
    stringlist[-1] = str(stringlist[-1][:-len(pointer)])
    newstring = ""
    for i in range(0, len(stringlist)):
      newstring += stringlist[i]
      if i < len(stringlist) - 1:
        newstring += "<br>\n    "
    baseplate = bcv.rfcas("baseplate.html")
    finaloutput = ""
    for i in range(0, len(baseplate)):
      if baseplate[i] == "@":
        finaloutput = baseplate[:i] + newstring + baseplate[i+1:]
        break
    finaloutput = finaloutput.replace(empty_child, "&middot")
    finaloutput = finaloutput.replace(pointer, " &#8594 ")
    file = open(filename, "w", encoding="utf-8")
    file.write(finaloutput)
    file.close()
    
  def graphviznodemaker(self, g, alist):
    contents = ""
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        contents += "<f" + str(i) + "> " + "●"
        self.graphviznodemaker(g, alist[i])
        self.nodenum += 1
      elif alist[i] == empty_child:
        contents += "<f" + str(i) + "> " + "○"
      else:
        contents += "|<f" + str(i) + ">" +str(alist[i])+ " |"
    g.node("node"+str(self.nodenum), nohtml(contents))
    for i in range(0, len(alist)):
      if type(alist[i]) != list and alist[i] != empty_child:
        alist[i] = self.nodenum
    
  def graphvizedgemaker(self, g, alist):
    for i in range(0, len(alist)):
      if type(alist[i]) == list:
        g.edge("node" + str(alist[1]) + ":f" + str(i), "node" + str(alist[i][1]) + ":f0")
        self.graphvizedgemaker(g, alist[i])
        
  def graphvizit(self, filename, operation):
    graph = Digraph('g', filename='bplustree.gv', node_attr={'shape': 'record', 'height': '.1'}, format='png', )
    graph.attr(label=operation)
    graph.attr(labelloc="t")
    newtree = deepcopy_nested_list(self.root)
    self.graphviznodemaker(graph, newtree)
    self.graphvizedgemaker(graph, newtree)
    self.nodenum = 0
    graph.render(filename, "output")
    os.remove("output\\" + filename) #just to remove the useless gv file after it compiles
      
def deepcopy_nested_list(data):
  out = []
  for el in data:
    if isinstance(el, list):
      out.append(deepcopy_nested_list(el))
    else:
      out.append(el)
  return out