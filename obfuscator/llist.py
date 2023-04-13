from random import shuffle

class Node:

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next
    
    def nextv(self):
        """Следующее значение, если оно есть"""
        return self.next.value if self.next else None
    def prevv(self):
        """Предыдущее значение, если оно есть"""
        return self.prev.value if self.prev else None

    def set_pn(self, prev, next):
        """Устанавливает prev и next"""
        self.prev = prev
        self.next = next
    
    def set_pno(self):
        """Устанавливает prev и next у соседей"""
        if self.prev:
            self.prev.next = self
        if self.next:
            self.next.prev = self
        return bool(self.prev), bool(self.next)
    
    def set_pnlinks(self, prev, next):
        """Устанавливает соседние ссылки"""
        self.set_pn(prev, next)
        return self.set_pno()
    
    def set_plink(self, prev):
        """устанавливат предыдущую Node"""
        self.prev = prev
        if prev:
            self.prev.next = self
        return bool(prev)
    
    def set_nlink(self, next):
        """устанавливат следующую Node"""
        self.next = next
        if next:
            self.next.prev = self
        return bool(next)

    def pnlinks(self):
        """Возвращает все ссылки как tuple"""
        p = None
        pn = None
        n = None
        np = None
        if self.prev:
            p = self.prev
            pn = self.prev.next
        if self.next:
            p = self.next
            pn = self.next.prev
        return (p, pn, n, np)

    def pnlinks_str(self, node=False):
        """Возвращает строковое представление ссылок"""
        prev = 'node.prev -> '
        if self.prev:
            prev += '%s.value: %s, prev -> %s.value: %s ' % (self.prev if node else 'n', self.prev.value, self if node else 'n', self.value)
        else:
            prev += 'None '
        next = 'node.next -> '
        if self.next:
            next += '%s.value: %s, next -> %s.value: %s' % (self.next if node else 'n', self.next.value, self if node else 'n', self.value)
        else:
            next += 'None'
        return prev + next

    def forward(self):
        """Итератор вперед"""
        yield self
        if self.next:
            for node in self.next:
                yield node

    def backward(self):
        """Итератор назад"""
        yield self
        if self.prev:
            for node in self.prev:
                yield node

    def __iter__(self):
        """Итератор по умолчанию"""
        return self.forward()
    
    def __str__(self) -> str:
        return str(self.value)

class LList:

    def __init__(self):
        self.clr()
    
    def __iter__(self):
        return self.forwardn()

    def empty(self):
        """Проверяет пустоту листа"""
        return self.count == 0

    def len(self, node=None):
        """Длина списка начиная с Node"""
        if not node: node = self.head
        return sum(1 for e in list(node.forward()))

#region iterators  
  
    def forward(self):
        """Итерация вперед"""
        current = self.head
        while current:
            yield current.value if current else None
            current = current.next

    def backward(self):
        """Итерация назад"""
        current = self.tail
        while current:
            yield current.value if current else None
            current = current.prev
    
    def forwardn(self):
        """Итерация вперед, возращая Node"""
        current = self.head
        while current:
            yield current
            current = current.next        

    def backwardn(self):
        """Итерация назад, возращая Node"""
        current = self.tail
        while current:
            yield current
            current = current.prev

#endregion

#region adding elements

    def addn(self, node):
        """Добавить Node в конец"""
        self.count+=1
        node.prev = self.tail
        node.next = None
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        return node

    def extendn(self, lst):
        """Добавить список Node в конец"""
        for el in lst:
            self.addn(el)

    def add(self, el):
        """Создать и добавить Node в конец"""
        self.count+=1
        new_node = Node(el, self.tail)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return new_node
    
    def extend(self, lst):
        """Создать и добавить список Node в конец"""
        for el in lst:
            self.add(el)

    def addns(self, node):
        """Добавить Node в начало"""
        self.count+=1
        node.next = self.head
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.head.prev = node
            self.head = node
        return node

    def extendns(self, lst):
        """Добавить список Node в начало"""
        for el in lst:
            self.addns(el)

    def adds(self, el):
        """Создать и добавить Node в начало"""
        self.count+=1
        new_node = Node(el, next = self.head)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node
        return new_node
    
    def extends(self, lst):
        """Создать и добавить список Node в начало"""
        for el in lst:
            self.adds(el)

#endregion

#region find elements

    def get(self, value):
        """Находит элемент по значению"""
        current = self.head
        while(current.next and current.value != value):
            current = current.next
        if current.value == value:
            return current
        return None

    def find(self, value, from_node = None, until_node = None):
        """Находит элемент в указанном списке"""
        current = from_node if from_node else self.head
        count = 0
        while(current.next and current.value != value):
            current = current.next
            count += 1
            if current.value == value:
                return current, count
            if current == until_node:
                break
        return None, -1

    def inl(self, value, from_node = None, until_node = None):
        """Проверяет наличие элемента в указанном списке"""
        return not (self.find(value, from_node, until_node)[0] is None)

    def ind(self, node, from_node = None, until_node = None):
        """Находит индекс элемента в указанном списке"""
        current = from_node if from_node else self.head
        count = 0
        while(current.next and current is not node):
            current = current.next
            count += 1
            if current is node:
                return count
            if current == until_node:
                break
        return -1

    def seek(self, node, count):
        """Пропускает count элементов"""
        current = node
        for i in range(count):
            if not (current := current.next):
                return self.tail
        return current

    def seek_n_of(self, node, count):
        """Пропускает count элементов и возвращает остаток count"""
        current = node
        for i in range(count):
            if not (current := current.next):
                return (self.tail, count - i)
        return (current, 0)

    def at(self, index):
        """Берет элемент по индексу"""
        if index >= self.count or index < -self.count:
            return None
        current = None
        if index >= 0:
            current = self.head
            for i in range(0, index):
                current = current.next
        else:
            current = self.tail
            for i in range(-1, index, -1):
                current = current.prev
        
        return current

    def v(self, index):
        """Берет значение элемента по индексу"""
        if current := self.at(index):
            return current.value

    def midn(self):
        """Возвращает элемент по середине списка"""
        return self.at(self.count//2)

    def mid(self):
        """Возвращает значение по середине списка"""
        return self.midn().value

#endregion

    def ins(self, node, new_node):
        """Вставляет элемент после текущего"""
        next_node = node.next
        has_pn = new_node.set_pnlinks(node, next_node)
        # если нет следующего элемента
        if not has_pn[1]:
            self.tail = new_node
        self.count+=1

    def putn(self, node, el):
        """Создает и вставляет элемент после текущего"""
        next_node = node.next
        new_node = Node(el, node, next_node)
        node.next = new_node
        if next_node:
            next_node.prev = new_node
        else:
            self.tail = new_node
        self.count+=1
        return new_node
    
    def braze(self, els, ele, node, count=None):
        """Вставляет список от els до ele после указанного элемента"""
        if not count:
            count = self.ind(ele, els) + 1
        next_node = node.next
        node.next = els
        els.prev = node
        if next_node:
            next_node.prev = ele
            ele.next = next_node
        else:
            self.tail = ele
        self.count += count

    def d(self, node):
        """Удаляет указанный элемент из списка"""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        else:
            self.head = next_node
        if next_node:
            next_node.prev = prev_node
        else:
            self.tail = prev_node
        node.prev = None
        node.next = None
        self.count-=1

    def rem(self, index):
        """Удаляет указанный элемент из списка по индексу""" 
        if current := self.at(index):
            self.d(current)
            return current.value
    
    def neib(self, el1, el2):
        """Определяет 2 элемента на соседство"""
        if el1 and el2:
            if el1.next == el2: return 1
            if el2.next == el1: return 2
        return 0

    def dl(self, els = None, ele = None, count = None):
        """Удаляет элементы от els до ele"""
        if els == None and ele == None:
            all_nodes = self.get_all()
            self.clr()
            return all_nodes
        if els is ele or self.neib(els, ele):
            return (None, None, 0)
        nels = els.next if els else self.head
        nele = ele.prev if ele else self.tail
        nels.prev = None
        nele.next = None
        if els: els.next = ele 
        else: self.head = ele
        if ele: ele.prev = els 
        else: self.tail = els
        count = count if count else self.len(nels)
        self.count -= count
        return (nels, nele, count)

    def remn(self, node, count):
        """Удаляет N элементов из списка, начиная с текущего"""
        if count < 1:
            return (None, None, 0)
        next_node, overflow = self.seek_n_of(node, count-1)
        return self.dl(node.prev, next_node.next, count - overflow)

    def reml(self, index, count):
        """Удаляет N элементов из списка, начиная с текущего индекса"""
        return self.remn(self.at(index), count)     

    def r(self, index):
        """Удаление элемента по индексу, возвращает ссылку на себя"""
        self.rem(index)
        return self

    def put(self, index, el):
        """Вставляет элемент по индексу"""
        if current := self.at(index):
            return self.putn(current, el)
    
    def putl(self, index, lst): 
        """Вставляет список по индексу"""
        current = self.at(index)
        for el in lst:
            new_node = self.putn(current, el)
            current = new_node

    def u(self, index, el):
        """Вставка элемента по индексу, возвращает ссылку на себя"""
        self.put(index, el)
        return self
    
    def pop(self):
        """Достает элемент с конца"""
        if tail_node := self.tail:
            self.tail = tail_node.prev 
            if self.tail: self.tail.next = None
            else: self.head = None
            self.count-=1
        return tail_node
    
    def pops(self):
        """Достает первый элемент"""
        if head_node := self.head:
            self.head = head_node.next
            if self.head: self.head.prev = None
            else: self.tail = None
            self.count-=1
        return head_node

    def cut(self, els, ele, new_els, new_ele, count=None, count_new=None):
        """Заменяет часть списка на другую"""
        old_nodes = self.dl(els, ele, count)
        self.braze(new_els, new_ele,els, count_new)
        return old_nodes

    # def t(self, node):
    #     """"""
    #     if node.next == None:
    #         self.tail = node
    #         return False
    #     if node.prev == None:
    #         self.head = node
    #         return False
    #     return True

    def o(self, *nodes):
        """Чинит ссылки"""
        for node in nodes:
            if node.next == None:
                self.tail = node
            else:
                node.next.prev = node
            if node.prev == None:
                self.head = node
            else:
                node.prev.next = node


    def xch(self, n1, n2):
        """Обмен двух элементов"""
        n1.prev, n2.prev = n2.prev, n1.prev
        n1.next, n2.next = n2.next, n1.next
        self.o(n1, n2)

    def tol(self):
        """Возвращает список как массив"""
        lst = []
        for node in self.forwardn():
            lst.append(node)
        return lst

    def shuffle(self):
        """Перемешивает список"""
        lst = self.tol()
        shuffle(lst)
        self.clr()
        self.extendn(lst)
        
        



        # if not count:
        #     count = self.ind(els, ele)[1]
        # if not count_new:
        #     count_new = self.ind(new_els, new_ele)[1]
        # self.count += count_new - count

        # els.next, new_els.prev = new_els, els.next
        # ele.prev, new_ele.next = new_ele, ele.prev
        # return (els.next, ele.prev)

    def get_all(self):
        """Дает все данные списка"""
        return (self.head, self.tail, self.count)

    def clr(self):
        """Очищает список"""
        self.head = None
        self.tail = None
        self.count = 0

    def __str__(self):
        """Строковое представление списка"""
        nodes_concat = 'llist: ['
        nodes_concat += ', '.join(str(el) for el in self)
        nodes_concat += ']'
        return nodes_concat


        # curr=self.head
        # curr_index=0
        # while(curr and curr_index!=index):
        #     curr_index+=1
        #     curr=curr.next
        # return curr.value if curr else None                



    

