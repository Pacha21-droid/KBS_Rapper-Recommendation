class Fact:
    def __init__(self,cat,val):
        self.cat=cat
        self.val=val
    def __repr__(self):
        return f"Fact:{self.cat}={self.val}"