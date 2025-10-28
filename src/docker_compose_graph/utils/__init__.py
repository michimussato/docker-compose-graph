__all__ = [
    "deep_merge",
    "deep_sorted",
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
                            dict1[key].append(item)
                else:
                    dict1[key] = dict2[key]
            elif isinstance(dict2[key], OverrideArray):
                # Override shall always REPLACE
                dict1[key] = dict2[key]
            else:
                dict1[key] = dict2[key]
    return copy.deepcopy(dict1)


def deep_sorted(d):
    # # https://www.geeksforgeeks.org/python/sort-a-nested-dictionary-by-value-in-python/
    # if isinstance(d, list):
    #     # sorting is case sensitive. capitals fist.
    #     return sorted(d, reverse=True)
    # for key, value in d.items():
    #     if isinstance(value, dict):
    #         d[key] = deep_sorted(value)
    #     elif isinstance(value, list):
    #         d[key] = deep_sorted(value)
    # return dict(sorted(d.items(), key=lambda item: str(item[1]) if not isinstance(item[1], dict) else str(
    #     deep_sorted(item[1]))))

    # https://stackoverflow.com/a/56305689/2207196
    def make_tuple(v): return (*v,) if isinstance(v, (list,dict)) else (v,)
    if isinstance(d, list):
        return sorted(map(deep_sorted, d), key=make_tuple)
    if isinstance(d, dict):
        return { k: deep_sorted(d[k]) for k in sorted(d)}
    return d
