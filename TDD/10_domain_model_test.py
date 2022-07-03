from datetime import date
from dataclasses import dataclass



@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self,ref:str,sku:str,qty:int,eta:date|None):
        self._reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()
    
    def __eq__(self,other):
        if not isinstance(other,Batch):
            return False
        return other.reference == self.reference
    def __hash__(self):
        return hash(self.reference)

    def allocate(self,line:OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    def deallocate(self,line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self,line:OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self,value):
        raise Exception("Read-Only Value!")

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

#Matching
def make_batch_and_line(sku,batch_qty,line_qty):
    return (
        Batch("batch-001",sku,batch_qty,eta=date.today()),
        OrderLine(orderid="order-123",sku=sku,qty=line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001","SMALL-TABLE",qty=20,eta=date.today())
    line = OrderLine(orderid="order-ref",sku="SMALL-TABLE",qty=2)
    batch.allocate(line)
    assert batch.available_quantity == 18

def test_can_allocate_when_batch_is_larger():
    large_batch,small_line = make_batch_and_line("SuperSKU",20,2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_when_batch_is_smaller():
    small_batch,large_line = make_batch_and_line("DuperSKU",10,20)
    assert small_batch.can_allocate(large_line) == False

def test_can_allocate_when_batchsize_equal():
    batch,line   =  make_batch_and_line("WhatSKU",2,2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001","UNCOMFY-CHAIR",100,eta=None)
    line = OrderLine(orderid="order-01",sku="COMFY-CHAIR",qty=30)
    assert batch.can_allocate(line) == False

def test_can_only_deallocate_allocated_lines():
    batch,unallocated_line = make_batch_and_line("DECORATIVE-TRINKET",20,2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch,line = make_batch_and_line("ANGULAR-DESK",20,2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18 

