def rfcas(filename): # return file contents as string
  with open(filename, 'r') as myfile:
    data = myfile.read()
  return data

def elacsv(mylist, filename): # export list as csv
  file = open(filename, "w")
  for i in range(0, len(mylist)):
    if(i < len(mylist) - 1):
      file.write(str(mylist[i]) + ", ")
    else:
      file.write(str(mylist[i]))
  file.close()
ok = 4
def rcsvasl(filename): # return csv as string list
  data = rfcas(filename)
  mylist = []
  temp = ""
  for i in range(0, len(data)):
    if data[i] == ",":
      mylist.append(temp)
      temp = ""
    else:
      temp += data[i]
      if i == len(data) - 1:
        mylist.append(temp)
  return mylist

def rcsvail(filename): # return csv as int list
  return list(map(int, rcsvasl(filename)))