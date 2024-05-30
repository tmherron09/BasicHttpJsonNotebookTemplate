from dataclasses import dataclass
import dataclasses
import json


@dataclass
class BaseQolModel:
    def to_json(self):
        return json.dumps(dataclasses.asdict(self), indent=4)

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        d = self.__dict__.copy()
        for key, value in d.items():
            if isinstance(value, BaseQolModel):
                d[key] = value.__dict__
        return d.__str__()


@dataclass
class Address(BaseQolModel):
    street: str
    city: str
    country: str


@dataclass
class User(BaseQolModel):
    name: str
    age: int
    address: Address


def object_hook(d):
    if 'street' in d:
        return Address(**d)
    else:
        return User(**d)
