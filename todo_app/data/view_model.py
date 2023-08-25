class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def done_items(self):
        result = []
        for i in self.items:
            if i.status == "Done":
                result.append(i)
        return result

    @property
    def todo_items(self):
        result = []
        for i in self.items:
            if i.status == "To Do":
                result.append(i)
        return result

    @property
    def doing_items(self):
        result = []
        for i in self.items:
            if i.status == "Doing":
                result.append(i)
        return result
