from typing import List, Dict

import yaml
from yaml import YAMLObject


__all__ = [
    "OverrideArray",
    "ResetNull",
]


class OverrideArray(YAMLObject):
    """
    - https://pyyaml.org/wiki/PyYAMLDocumentation
    - https://stackoverflow.com/questions/26744956/formatting-custom-class-output-in-pyyaml
    """
    yaml_tag = u'!override'
    yaml_flow_style = False

    def __init__(
            self,
            array: List,
    ):
        self.array = array

    @classmethod
    def to_yaml(cls, dumper: yaml.Dumper, data):
        node = dumper.represent_sequence(cls.yaml_tag, data.array)
        return node

    @classmethod
    def from_yaml(cls, loader, node):
        array = loader.construct_sequence(node)
        return OverrideArray(array)

    def __repr__(self):
        return "%s(array=%r)" % (
            self.__class__.__name__, self.array)


class ResetNull(YAMLObject):
    """
    - https://pyyaml.org/wiki/PyYAMLDocumentation
    - https://stackoverflow.com/questions/26744956/formatting-custom-class-output-in-pyyaml
    """
    yaml_tag = '!reset'
    yaml_flow_style = False
    # yaml_loader = yaml.Loader
    # yaml_dumper = yaml.Dumper

    def __init__(self, obj: Dict):
        self.obj = obj

    @classmethod
    def to_yaml(
            cls,
            dumper: yaml.Dumper,
            data,
    ):
        # assert not bool(obj)
        # if isinstance(obj, NoneType):
        node = dumper.represent_mapping(cls.yaml_tag, data.obj)
        # if isinstance(data.obj, NoneType):
        # node = yaml.nodes.ScalarNode(cls.yaml_tag, None)
        return node
        node = dumper.represent_mapping(f"{cls.yaml_tag} null", None)
        # elif isinstance(data.obj, List):
        #     node = dumper.represent_sequence(u'!reset', data)
        # else:
        #     raise NotImplementedError(f"Cannot represent {type(data)}. "
        #                               f"{data = } "
        #                               f"{dir(data) = } ")
        # elif isinstance(obj, List):
        #     node = dumper.represent_sequence(u'!override', obj)
        # elif isinstance(obj, NoneType):
        #     node = dumper.represent_none(u'!override', obj)

        return node

    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node):
        obj = loader.construct_mapping(node)
        return ResetNull(obj)

    def __repr__(self):
        return "%s(obj=%r)" % (
            self.__class__.__name__, self.obj)
