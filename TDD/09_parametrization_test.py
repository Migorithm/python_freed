import pytest
from dataclasses import dataclass,asdict

@dataclass
class User:
    id :str
    age:int
    name:str


def test_finish(): 
    for u in [
        User("saka1023",20,"Migo"),
        User("saka1024",25,"Mago"),
        User("saka1025",32,"Mego"),    
    ]:
        assert u.name.startswith("M")

#Parametrizing function
@pytest.mark.parametrize(
    "IDs,Ages,Names",
    [
        ("saka1023",20,"MIGO"),
        ("zaka1023",24,"Zigo"),
        ("eaka123",93,"Tigo"),
    ],
)
def test_fenish(IDs,Ages,Names):
    initial_user=User(id=IDs,age=Ages,name=Names)
    assert initial_user.age >= 20

def test_params(parameters):
    assert parameters>=5