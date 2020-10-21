#!/usr/bin/env python
# -*- coding: utf-8 -*-
# %% [markdown]
# # PEP 557 Data Classes & attr

# %%
import pprint
import random

import attr
import cattr


# %% [markdown]
# ## Define attrs based Dataclass
#
# - set type & default values
# - set converter
# - set validators
# %%
@attr.s(auto_attribs=True)
class Point:
    x: float = attr.ib(
        default=0.,
        validator=[
            attr.validators.instance_of(float),
            attr.validators.in_([0,1,2,3,4])
        ],
        converter=float
    )
    y: float = 0.


# %%[markdown]
# ### Validate it!
# %%
Point(["1"], "ahoj")  # Fails on converter
Point(32, "ahoj")  # Fails on accepted range

# %% [markdown]
# ### Timeit!
# %%
%timeit p1 = Point("1", "ahoj")
p1 = Point("1", "ahoj")


# %% [markdown]
# ### Timeit without validation
# %%
attr.set_run_validators(False)
%timeit p2 = Point(1, "ahoj")
p2 = Point(1, "ahoj")


# %% [markdown]
# ## Slots
#
# - static amount of memory per instance with all the attributes
# - lower memory consumption
# - faster data access (depends on data type)

# %%
@attr.s(slots=True, auto_attribs=True)
class PointSlots:
    x: float = 0.
    y: float = 0.

# p1s = [Point(i, i**2) for i in range(10000000)]
# ps = [PointSlots(i, i**2) for i in range(10000000)]

p = Point(2, 2**2)
p_slot = PointSlots(2, 2**2)

%timeit p.x
%timeit p_slot.x


# %% [markdown]
# ## Easy introspection
# %%
print(attr.has(Point))
print(attr.fields_dict(Point))

# %% [markdown]
# ## Convert attrs to and from structured data
# %%
point_dict = cattr.unstructure(p)
point_from_dict = cattr.structure_attrs_fromdict(point_dict, Point)

# %% [markdown]
# ### Nested structures
# %%
@attr.s(auto_attribs=True)
class Line:
    begin: PointSlots
    end: PointSlots

line = Line(PointSlots(1., 3.), PointSlots(2., 3.))

line_dict = cattr.unstructure(line)

line_from_unstructured = cattr.structure_attrs_fromdict(line_dict, Line)


# %%
