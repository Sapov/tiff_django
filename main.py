class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    class __Node:
        def __init__(self, value):
            self.value = value
            self.next = None

        def __repr__(self):
            return f'VALUE={self.value}'

    def add_first_node(self, value):
        new_node = self.__Node(value)
        if self.__head == None:
            self.__head = self.__tail = new_node
        else:
            new_node.next = self.__head
            self.__head = new_node

    def add_last_node(self, value):
        new_node = self.__Node(value)
        if self.__head == None:
            self.__head = self.__tail = new_node
        else:
            self.__tail.next = new_node
            self.__tail = new_node

    def remove_first_node(self):
        if self.__head == self.__tail:
            self.__head = self.__tail = None
        else:
            temp = self.__head.next
            self.__head = None
            self.__head = temp

    def remove_last_node(self):
        if self.__head == self.__tail:
            self.__head = self.__tail = None
        else:
            cur = self.__head
            while cur.next != self.__tail:
                cur = cur.next
            cur.next = None
            self.__tail = cur

    def remove(self, value):
        if self.__head == None:
            raise ValueError('!!')
        cur = self.__head
        prev = self.__head

        while cur.next:
            if cur.value == value:
                prev.next = cur.next
                cur.next = None
                return

            prev.next = cur
            cur = cur.next

        raise ValueError('Нет значения')


ll = LinkedList()

ll.add_last_node(10)
ll.add_last_node(20)
ll.add_last_node(30)

ll.remove(20)

print('')
