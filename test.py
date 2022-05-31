from typing import TypeAlias
from pydantic import BaseModel

Symbol: TypeAlias = str
Atom: TypeAlias = float|int|Symbol
Expression: TypeAlias = Atom| list

class TypeAliasTest(BaseModel):
    name: Symbol
    alphanu: Atom
    whatever:Expression

a= TypeAliasTest(name=32,alphanu=";;",whatever=6)
print(a)