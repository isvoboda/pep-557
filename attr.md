---
theme: default
marp: true
---


# [PEP: 557 Data Classes](https://www.python.org/dev/peps/pep-0557) & [attr](https://www.attrs.org/)

<!-- headingDivider: 2 -->

## Data Class

~~~python
from dataclasses import dataclass

@dataclass
class Point:
    x: float  # PEP 526 - type annotation from Python 3.6
    y: float = 0.0
    
    @classmethod
    def from_tuple(cls, pt: Tuple[float, float]) -> "Point":
        return cls(x=pt[0], y=pt[1])
~~~

- Main design goal of Data Classes is to support static type checkers
- The same as ordinary python class
- No meta-classes or inheritance involved
- `__dunder__` methods for free

## Data Class, that is it?!

~~~python
from dataclasses import astuple, field, dataclass

@dataclass
class Polygon:
    vertices: List[Point] = field(default_factory=list, metadata={"max_len": 64})

poly_tuple = astuple(Polygon(vertices=[Point(0., 0.), Point(1., 1.)]))
# ([(0., 0.), (1., 1.,)])
~~~

Why not just NamedTuple?

~~~python
class PointNT(NamedTuple):  # Can not be further inherited
    x: float
    y: float

PointNT(x=1.0, y=2.0) == (1.0, 2.0)  # True
Point(x=1.0, y=2.0) == (1.0, 2.0)  # False
~~~

## [I want more!](https://www.youtube.com/embed/B4Bbge92Nlo)

## attr

~~~python
import attr

@attr.s(auto_attribs=True)
class Point:
    x: float = 0.0
    y: float = attr.ib(
        default=0.0,
        converter=float,  # hell expensive, imagine dispatch from functools
        validator=[       # not in standard library, could be generic callable
            attr.validators.instance_of(float),
            attr.validators.in_([0.,1.,2.,3.,4.])
        ]
    )

point = Point(y="2")  # Point(x=0.0, y=2.0)
~~~

- `attr.set_run_validators(False)` - toggle the validation
- serious business names `@attrs` and `@attr.attrib`

## attr tweaks

~~~python
import attr, cattr

@attr.s(slots=True, auto_attribs=True)  # lower memory footprint & faster data access
class Point:
    x: float = 0.0
    y: float = 0.0

point = Point()

point_dict = cattr.unstructure(point)  # unstructer to dict or tuple

# Structure from dict/tuple back to Point type (works for nested data)
# allows to filter out specific attributes
point_from_dict = cattr.structure_attrs_fromdict(point_dict, Point) 
~~~

- ecosystem of attr extensions in a form of other pip packages
- easy to serialize data to json & yaml and back

## Conclusion

- Pandas support in 1.1 (DataFrame based on dataclass from standard library) :poop:
- fast and easy to use for streamed data
- support dynamic definition `attr.make_class(name=name, attrs=attrs, ...)`
- support hashing (instance as key in `set`, `dict`, ..)
- friendly introspection (get the name & type of dataclass attribute)
  - `Dataclass <-> dtype <-> DataFrame`
- the precious (milášek) v `idf`

## Notes

- [`Pydantic`](https://pydantic-docs.helpmanual.io/) more high-level and `faster` compared to attr but not as `clean`
- [`cluegen`](https://github.com/dabeaz/cluegen#wait-hasnt-this-already-been-invented) by David Beazly
> `At this point, naysayers will be quick to point out that "well, actually you could just use @dataclass from the standard library." Othe.rs migh.t help.fully sugg.est usag.e of the attr.s libr.ary. And they might have a point.`

- [why not just attrs?](https://github.com/ericvsmith/dataclasses/issues/19)
