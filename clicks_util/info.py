import inspect


def getAllFuncs(cls) -> list:
    """Teturn all callable functions of a class"""
    return [func for func in dir(cls) if callable(getattr(cls, func)) if not str(func).startswith("__")]


def getAllVars(cls) -> list:
    """Return all variables of a class"""
    return [var for var in vars(cls) if not str(var).startswith("__")]


def getInfo(target) -> dict:
    if not inspect.isclass(target):
        if inspect.isfunction(target):
            return {
                "name": target.__name__,
                "type": type(target),
                "arg_count": target.__code__.co_argcount,
                "arg_names": target.__code__.co_varnames,
                "filename": target.__code__.co_filename,
                "defaults": target.__defaults__,
                "kwdefaults": target.__kwdefaults__,
                "doc": target.__doc__,
                "annotations": target.__annotations__
            }

        elif inspect.ismethod(target) or inspect.isbuiltin(target):
            return {
                "name": target.__name__,
                "qualname": target.__qualname__,
                "type": type(target),
                "self": target.__self__,
                "module": target.__module__,
                "doc": target.__doc__,
            }

    elif inspect.isclass(target):

        return_dict = {
            "name": target.__name__,
            "module": target.__module__,
            "qualname": target.__qualname__,
            "doc": target.__doc__,
            "functions": getAllFuncs(target),
        }

        if inspect.isbuiltin(target):
            return_dict["file"] = inspect.getfile(target)
            return return_dict
        return return_dict

    return {
            "value": target,
            "type": str(type(target)).replace("<", "").replace(">", "").replace("'", "").split(" ")[1],
        }

print(getInfo(int))