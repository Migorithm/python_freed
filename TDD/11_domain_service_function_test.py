from datetime import date,timedelta
from dataclasses import dataclass
import pytest

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
    def __repr__(self):
        return f"<Batch {self.reference}>"
        
    def __eq__(self,other):
        if not isinstance(other,Batch):
            return False
        return other.reference == self.reference
    def __hash__(self):
        return hash(self.reference)

    #For sorting
    def __gt__(self,other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

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

#StandAlone Function for domain service
def allocate(line:OrderLine, batches:list[Batch]) -> str:
    try:
        batch = next( b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
  

def tomorrow(days=1):
    return date.today() + timedelta(days=days)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch","RETRO-CLOCK",100,eta=None)
    shipment_batch = Batch("shipment_batch","RETRO-CLOCK",100,eta=tomorrow())
    line = OrderLine("oref","RETRO-CLOCK",10)
    allocate(line,[in_stock_batch,shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch","MINIMALIST-SPOON",100,eta=date.today())
    medium = Batch("normal-batch","MINIMALIST-SPOON",100,eta=tomorrow())
    latest = Batch("slow-batch","MINIMALIST-SPOON",100,eta=tomorrow(5))
    line=OrderLine("order1","MINIMALIST-SPOON",10)
    allocate(line,[medium,earliest,latest])

    assert earliest.available_quantity == 90

def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref","HIGHBROW-POSTER",100,eta=None)
    shipment_batch = Batch("shipment-batch-ref","HIGHBROW-POSTER",100,eta=tomorrow())
    line= OrderLine("oref","HIGHBROW-POSTER",10)
    allocation = allocate(line, [in_stock_batch,shipment_batch])
    assert allocation == in_stock_batch.reference


#Exceptions can express Domain Concepts too.
#  If there is the possibility that an order cannot be allocated because it's out of stock,
#  we can capture that by using a 'DOMAIN EXCEPTION'

class OutOfStock(Exception):
    pass

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1","SMALL-FORK", 10, eta=date.today())
    allocate(OrderLine("order1","SMALL-FORK",10),[batch])
    with pytest.raises(OutOfStock,match="SMALL-FORK"):
        allocate(OrderLine("order2","SMALL-FORK",2),[batch])
