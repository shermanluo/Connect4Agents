

mySet = set()
mySet.add(1)
mySet.add(2)
if mySet.contains(1):
    print("here!") #here!
mySet.remove(1)
if mySet.contains(1):
    print("here!")

>>> tel = {'jack': 4098, 'sape': 4139}
>>> tel['guido'] = 4127
>>> tel
{'sape': 4139, 'guido': 4127, 'jack': 4098}
>>> tel['jack']
4098
>>> del tel['sape']
>>> tel['irv'] = 4127
>>> tel
{'guido': 4127, 'irv': 4127, 'jack': 4098}
>>> list(tel.keys())
['irv', 'guido', 'jack']
>>> 'guido' in tel
True


def twoSum(lst):
    helper = Set()
    for elem in lst:
        if helper.contains(-elem):
            return True
        helper.add(elem)
    return False

def intersection(A, B):
    helper = set()
    seen = set()
    ret = []
    for elem in A:
        helper.add(elem)
    for elem in B:
        if elem in helper and not in seen:
            seen.add(elem)
            ret.append(elem)
    return ret
