__all__ = [
    "deep_merge",
]

import copy

from docker_compose_graph.yaml_tags.overrides import OverrideArray


def deep_merge(dict1, dict2):
    """https://sqlpey.com/python/solved-top-5-methods-to-deep-merge-dictionaries-in-python/"""
    for key in dict2:
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            deep_merge(dict1[key], dict2[key])
        else:
            if isinstance(dict2[key], list):
                if key in dict1:
                    # Existing list shall
                    # be extended
                    for item in dict2[key]:
                        # Avoid duplicates and keep order
                        if item not in dict1[key]:
                            dict1[key].append(dict2[key])
                else:
                    dict1[key] = dict2[key]
            elif isinstance(dict2[key], OverrideArray):
                # Override shall always REPLACE
                dict1[key] = dict2[key]
            else:
                dict1[key] = dict2[key]
    return copy.deepcopy(dict1)
