import builtins
import inspect
import types

magic = set()
for name in dir(builtins):
    obj = getattr(builtins, name)
    if inspect.isclass(obj) or inspect.isroutine(obj) or isinstance(obj, types.ModuleType):
        for attr in dir(obj):
            if attr.startswith('__') and attr.endswith('__'):
                magic.add(attr)
magic_list = sorted(magic)
print(len(magic_list))
print(magic_list)