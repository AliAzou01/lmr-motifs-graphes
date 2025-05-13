class Item:
    """Représente un item unique."""
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Item) and self.value == other.value

    def __lt__(self, other):
        return isinstance(other, Item) and self.value < other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return str(self.value)

class Itemset:
    """Représente un ensemble d'items."""
    def __init__(self, items):
        self.items = set(items)

    def __eq__(self, other):
        return isinstance(other, Itemset) and self.items == other.items

    def __hash__(self):
        return hash(tuple(sorted(self.items)))

    def __repr__(self):
        return ' '.join(map(str, sorted(self.items)))

class Sequence:
    def __init__(self, itemsets):
        self.itemsets = itemsets

    def __str__(self):
        return " -1 ".join(str(itemset) for itemset in self.itemsets) + " -2"