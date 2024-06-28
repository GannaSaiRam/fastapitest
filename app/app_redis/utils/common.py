from typing import Union, get_args, Any, _UnionGenericAlias


def extract_type(optional_type: Any) -> Any:
    # Check if the type is an instance of Optional
    if isinstance(optional_type, _UnionGenericAlias) and optional_type.__origin__ is Union:
        # Extract the type argument from Optional
        args = get_args(optional_type)
        # Filter out NoneType and return the remaining type
        for arg in args:
            if arg is not type(None):
                return arg.__name__
    return optional_type.__name__
