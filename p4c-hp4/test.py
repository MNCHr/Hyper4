#!/usr/bin/python

class myFirstClass():
  def __init__(self):
    self.items = set()
    self.inventory = []

class mySecondClass():
  def __init__(self, items, inventory):
    self.items = items
    self.inventory = inventory

a = myFirstClass()
b = myFirstClass()
a.inventory.append(1)
print("Added 1 to a's inventory.  Here is a's inventory:")
print(a.inventory)
print("And here is b's inventory:")
print(b.inventory)

newset = set()
newlist = []
c = mySecondClass(newset, newlist)
newset2 = set()
newlist2 = []
d = mySecondClass(newset2, newlist2)
c.items.add(1)
print("After adding 1 to c's items, here are d's items:")
print(d.items)
