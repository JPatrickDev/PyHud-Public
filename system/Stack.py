class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def empty(self):
        return self.items == []

    def pop(self):
        return self.items.pop()

    def length(self):
        return len(self.items)

    def peek(self):
        return self.items[len(self.items) - 1]
