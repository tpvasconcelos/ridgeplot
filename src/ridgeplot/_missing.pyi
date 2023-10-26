import sys
from enum import Enum

if sys.version_info >= (3, 8):
    from typing import Final, Literal
else:
    from typing_extensions import Final, Literal

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

class _Missing(Enum):
    MISSING = ...

MISSING: Final = _Missing.MISSING
MissingType: TypeAlias = Literal[_Missing.MISSING]
