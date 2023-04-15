from obfuscator.llist import LList, Node
import unittest

def assertLinkedList(lst, array):
        #Check list length
        assert lst.count == len(array), 'count is %s, %s expected. %s' %(lst.count, len(array), lst)
        if len(array) > 0:
            #Check tail and head
            assert lst.head.value == array[0], 'head is %s, %s expected. %s' %(lst.head.value, array[0], lst)
            assert lst.tail.value == array[-1], 'tail is %s, %s expected. %s' %(lst.tail.value, array[-1], lst)
            #Check elements pointers and elements
            new_array = array.copy()
            new_array.insert(0, None)
            new_array.append(None)
            for i, node in enumerate(lst.forwardn()):
                assert node.prevv() == new_array[i], 'node.prev.value is %s, %s expected. current node is %s. %s' % (node.prevv(), new_array[i], node.value, lst)
                assert node.value == new_array[i+1], 'node.value is %s, %s expected. %s' % (node.value, new_array[i+1], lst)
                assert node.nextv() == new_array[i+2], 'node.next.value is %s, %s expected. current node is %s. %s' % (node.nextv(), new_array[i+2], node.value, lst)
        #Check tail and head for empty list
        else:
            assert lst.head == None, 'head is not None. %s'%(lst)
            assert lst.tail == None, 'tail is not None. %s'%(lst)

class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self.lst = LList()
        self.lst.add(1)
        self.lst.add(3)
        self.lst.add(5)
        self.lst.add(9)
        self.emp = LList()

    def testAdd(self):
        assertLinkedList(self.emp, [])
        assertLinkedList(self.lst, [1, 3, 5, 9])
        self.lst.adds(0)
        assertLinkedList(self.lst, [0, 1, 3, 5, 9])
        assert str(self.lst) == 'llist: [0, 1, 3, 5, 9]', 'llist is: %s'%(self.lst)

    def testCount(self):
        assert self.lst.len() == 4
        assert self.lst.len(self.lst.at(1)) == 3
        assert self.lst.len(self.lst.at(2)) == 2

    def testGetElement(self):
        node = self.lst.add(8)
        assert self.lst.v(0) == 1
        assert self.lst.v(1) == 3
        assert self.lst.at(4) == node
        assert self.lst.v(8) == None
        assert self.lst.v(-8) == None
        assert self.lst.v(-1) == 8
        assert self.lst.v(-5) == 1
        assert self.lst.mid() == 5
        assert self.lst.get(5) == self.lst.at(2)

    
    def testInsertIntoList(self):
        self.emp.put(2, 4)
        assertLinkedList(self.emp, [])
        self.lst.put(1, 8)
        assertLinkedList(self.lst, [1, 3, 8, 5, 9])
        self.lst.put(1, 6)
        assertLinkedList(self.lst, [1, 3, 6, 8, 5, 9])
        self.lst.put(0, 7)
        assertLinkedList(self.lst, [1, 7, 3, 6, 8, 5, 9])
        el = self.lst.put(4, 11)
        assertLinkedList(self.lst, [1, 7, 3, 6, 8, 11, 5, 9])
        self.lst.putn(el, 12)
        assertLinkedList(self.lst, [1, 7, 3, 6, 8, 11, 12, 5, 9])

    def testInsertIntoList2(self):
        self.lst.putl(1, [8, 3, 5])
        assertLinkedList(self.lst, [1, 3, 8, 3, 5, 5, 9])
        self.lst.u(0, -1).u(7, -2)
        assertLinkedList(self.lst, [1, -1, 3, 8, 3, 5, 5, 9, -2])

    def testAddBatch(self):
        self.emp.extend([1, 2, 3])
        assertLinkedList(self.emp, [1, 2, 3])
        self.emp = LList()
        self.emp.extends([1, 2, 3])
        assertLinkedList(self.emp, [3, 2, 1])
        self.lst.extends([-1, -2, -3])
        assertLinkedList(self.lst, [-3,-2,-1, 1, 3, 5, 9])

    def testListClr(self):
        self.lst.clr()
        assertLinkedList(self.lst, [])

    def testPop(self):
        el = self.lst.pops()
        assert el.value == 1
        el = self.lst.pop()
        assert el.value == 9
        el = self.lst.pops()
        assert el.value == 3
        el = self.lst.pop()
        assert el.value == 5
        el = self.lst.pop()
        assert el == None
        self.lst.add(4)
        el = self.lst.pops()
        assert el.value == 4
        el = self.lst.pops()
        assert el == None

    def testRemoveManyFromList(self):
        els = self.lst.at(0)
        ele = self.lst.at(3)
        nels, nele, count = self.lst.dl(els, ele)
        assertLinkedList(self.lst, [1, 9])
        assert nels.value == 3
        assert nele.value == 5
        assert count == 2

    def testRemoveManyFromList2(self):
        els = self.lst.at(0)
        ele = self.lst.at(2)
        nels, nele, count = self.lst.dl(els, ele)
        assertLinkedList(self.lst, [1, 5, 9])
        assert nels.value == 3
        assert nele.value == 3
        assert count == 1
        tuple_none = self.lst.dl(els, ele)
        assert tuple_none == (None, None, 0)
        tuple_none = self.lst.dl(els, els)
        assert tuple_none == (None, None, 0)

    def testRemoveFromList(self):
        els = self.lst.at(1)
        self.lst.d(els)
        assertLinkedList(self.lst, [1, 5, 9])
        value = self.lst.rem(1)
        assert value == 5
        assertLinkedList(self.lst, [1, 9])
        self.lst.r(1).r(0)
        assertLinkedList(self.lst, [])

    def testRemoveNodesFromList(self):
        el = self.lst.at(1)
        self.lst.remn(el,0)
        assertLinkedList(self.lst, [1, 3, 5, 9])
        els, ele, count = self.lst.remn(el,1)
        assertLinkedList(self.lst, [1, 5, 9])
        assert els == ele == el
        assert count == 1
        el = self.lst.at(1)
        els, ele, count = self.lst.remn(el,2)
        assertLinkedList(self.lst, [1])


    def testSeek(self):
        el = self.lst.at(1)
        assert self.lst.seek(el, 0) == el
        assert self.lst.seek(el, 1).value == 5
        el = self.lst.seek(el, 100)
        assert el.value == 9
        el = self.lst.at(1)
        assert self.lst.seek_n_of(el, 2) == (self.lst.at(3), 0)
        assert self.lst.seek_n_of(el, 9) == (self.lst.at(3), 7)

    def testFindInList(self):
        el, ind = self.lst.find(5)
        assert el.value == 5 
        assert ind == 2
        assert el == self.lst.at(2)
        assert 2 == self.lst.ind(el)
        assert self.lst.find(-1) == (None, -1)
        assert self.lst.ind(Node(-2)) == -1
    
    def testCut(self):
        el = self.lst.at(1)
        els, ele, count = self.lst.remn(el,2)
        lst2 = LList()
        lst2.extend([2,4,6,8,0])
        oels = lst2.at(1)
        oele = lst2.at(3)
        els, ele, count = lst2.cut(oels, oele, els, ele)
        assertLinkedList(lst2, [2, 4, 3, 5, 8, 0])
    
    def testShuffle(self):
        el = self.lst.at(1)
        el2 = self.lst.at(3)
        self.lst.xch(el, el2)
        assertLinkedList(self.lst, [1, 9, 5, 3])
        self.lst.shuffle()
        lst2 = LList()
        lst2.extend([1, 9, 5, 3])
        # lst2_str = str(lst2)
        # lst_str = str(self.lst)
        assert str(self.lst) != str(lst2)


if __name__ == "__main__":
    unittest.main() # run all tests