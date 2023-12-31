# HW4
# REMINDER: The work in this assignment must be your own original work and must be completed alone.


class Node:
    def __init__(self, content):
        self.value = content
        self.next = None
        self.previous = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1005, 18, "another header", "111110")
        >>> hash(content1)
        0
        >>> hash(content2)
        1
        >>> hash(content3)
        2
        >>> hash(content4)
        1
    '''
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        total=0
        for x in ascii(self.header): #sets everything to ascii then adds up all the numerical values
                total+=ord(x)
        return total%3 #finds the remainder in order to shove it in to its different boxes
        pass


class CacheList:
    ''' 
        # An extended version available on Canvas. Make sure you pass this doctest first before running the extended version

        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1006, 18, "another header", "111110")
        >>> content5 = ContentItem(1008, 2, "items", "11x1110")
        >>> lst=CacheList(200)
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst.put(content2, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> lst.put(content4, 'mru')
        'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
        >>> lst.put(content5, 'mru')
        'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
        >>> lst.put(content3, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> 1006 in lst
        True
        >>> contentExtra = ContentItem(1034, 2, "items", "other content")
        >>> lst.update(1008, contentExtra)
        'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        >>> lst.tail.value
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> lst.tail.previous.value
        CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110
        >>> lst.tail.previous.previous.value
        CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content
        >>> lst.tail.previous.previous is lst.head
        True
        >>> lst.tail.previous.previous.previous is None
        True
        >>> lst.clear()
        'Cleared cache!'
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
    '''
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        if content.cid in self: #checks if id is already in program
            return "Content {} already in cache, insertion not allowed".format(content.cid)
        if content.size>self.maxSize: #checks if file is too large
            return "Insertion not allowed"
        if content.size>self.remainingSpace: #checks if file isn't too large for the system but ofr current storage
            if evictionPolicy=='lru': #checks the eviction policy and delets content based on it
                while content.size>self.remainingSpace: #continues going until there is enough space
                    self.lruEvict()
            if evictionPolicy=='mru':
                while content.size>self.remainingSpace:
                    self.mruEvict()
        temp=self.head #adds new node infront of old nodes
        self.head=Node(content)
        self.head.next=temp
        if self.head.next is not None: #a check to make sure this is not the first Node
            self.head.next.previous=self.head
        else:
            self.tail=self.head
        self.remainingSpace-=content.size #subtracts from leftover storage
        self.numItems+=1 #adds to item count
        return "INSERTED: {}".format(content)
        pass

    

    def __contains__(self, cid):
        current = self.head
        while current is not None: #goes through each value and checks if it lines up
            if cid==current.value.cid:
                temp=Node(current.value) #creates a seperate node of the value of the object
                temp.next=self.head #tacks on the old list
                self.head=temp #sets the new list as the current list
                self.head.next.previous=self.head #resets all pathway
                if current.next is None: #if tail
                    self.tail=current.previous #removes tail
                    current.previous.next=None
                    current=None
                else:
                    current.previous.next=current.next #moves Node below up and reassigns all back and forth pathways
                    current.next.previous=current.previous
                    current=current.next
                return True
            current=current.next
        return False
        pass


    def update(self, cid, content):
        if cid in self: #checks if the id is in the list already
            if content.size-self.head.value.size<self.remainingSpace: #if it is it checks if there is enough extra space for the update
                self.remainingSpace+=self.head.value.size-content.size #changes size values and updates node
                self.head.value=content 
                return "UPDATED:{}".format(content)
        return "Cache miss!"
        pass



    def mruEvict(self):
        self.remainingSpace+=self.head.value.size #readds the taken storage
        if self.head.next is not None: #checks if only item in list
            self.head=self.head.next #moves the node below up to the head position and updates bathways while removing the head node
            self.head.next.previous=self.head
            self.head.previous=None
        else:
            self.head=None #could use clear here, but felt unnecessary since the extra processes is handles have to be handle anyhow
            self.tail=None
        self.numItems-=1
        pass

    
    def lruEvict(self):
        self.remainingSpace+=self.tail.value.size #opens storage
        if self.tail.previous is not None: #checks if only piece in list
            self.tail = self.tail.previous #removes node while assigning the one behind it as its successor
            if self.tail.previous is not None: #in case next Node is the head node
                self.tail.previous.next=self.tail#sets pathway for the next node behind
            else: 
                self.tail=self.head #if is head node just assigns the both to the same thing
                self.head.next=None
            self.tail.next = None #removes the next Node from the new tail
        else: #again could use clear did not feel anymore efficient
            self.head=None
            self.tail=None
        self.numItems-=1
        pass

    
    def clear(self): #resets everything to initial properties (Might be a way to reuse init but im not confident enough to try)
        self.head=None
        self.tail=None
        self.remainingSpace=self.maxSize
        self.numItems=0
        return "Cleared cache!"
        pass
class Cache:
    """
        # An extended version available on Canvas. Make sure you pass this doctest first before running the extended version

        >>> cache = Cache()
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")

        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")

        >>> content7 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 18 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:177
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:45
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:16
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache[content9].next.value
        CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>
    """

    def __init__(self):
        self.hierarchy = [CacheList(200), CacheList(200), CacheList(200)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__


    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    
    def insert(self, content, evictionPolicy): #checks the hash and inserts the content accordingly
        return self.hierarchy[hash(content)].put(content,evictionPolicy)
        pass


    def __getitem__(self, content): #checks if the item exists then returns it once its pulled ot the front
        if content.cid in self.hierarchy[hash(content)]:
            return self.hierarchy[hash(content)].head
        return "Cache miss!"
        pass



    def updateContent(self, content): #checks the hash then updates the object in the hash list if it exists
        return self.hierarchy[hash(content)].update(content.cid,content)
        pass
