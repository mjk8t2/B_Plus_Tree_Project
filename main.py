import bplustree as bp
import bcv_utilities as bcv

# START TEST 1 ---------------------------------------

buildlist = [12, 35, 3, 20, 85, 22, 5, 10, 1, 18, 11, 55, 99, 36, 47]
sequence = [("D", 85), ("D", 84), ("D", 18), ("I", 19), ("D", 5), ("D", 47), ("D", 99), ("I", 11)]

mytree = bp.bplustree(4)
for i in buildlist:
  mytree.insert(i)
print("Original tree:")
mytree.prettyprint()
mytree.graphvizit("mytree0", "Original tree")

for i in range(0, len(sequence)):
  if sequence[i][0] == "D":
    if mytree.search(sequence[i][1], mytree.root):
      print("Deleting key value", sequence[i][1])
      mytree.delete(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "After deleting key value " + str(sequence[i][1]))
    else:
      print("Cannot delete key value", sequence[i][1], "since it is not in the tree!")
      mytree.delete(sequence[i][1])
      mytree.prettyprint()
      #mytree.graphvizit("mytree" + str(i+1), "Cannot delete key value " + str(sequence[i][1]) + " since it is not in the tree!")
  elif sequence[i][0] == "I":
    if not mytree.search(sequence[i][1], mytree.root):
      print("Inserting key value", sequence[i][1])
      mytree.insert(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "After inserting key value " + str(sequence[i][1]))
    else:
      print("Cannot insert key value", sequence[i][1], "since it is already in the tree!")
      mytree.insert(sequence[i][1])
      mytree.prettyprint()
      mytree.graphvizit("mytree" + str(i+1), "Cannot insert key value " + str(sequence[i][1]) + " since it is already in the tree!")

# END TEST 1 ----------------------------------------