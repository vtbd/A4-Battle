import ast
import constants as c
from typing import Any, Callable, Optional
from functools import wraps

def dict_assigning(func) -> Callable[[dict], dict]:
    @wraps(func)
    def wrapper(source_dict:dict, **kw) -> dict:
        return_dict = {}

        def assigner(target_key, source_key, default=None, wrapper_func: Optional[Callable[[Any], Any]]=None):
            if default is NotImplemented and source_key not in source_dict:
                return
            value = source_dict.get(source_key, default)
            if wrapper_func is not None:
                value = wrapper_func(value, **kw)
            return_dict[target_key] = value

        func(source_dict, assign=assigner)
        return return_dict
    return wrapper

@dict_assigning
def char_dict_builder(r:dict, *, assign: Callable, **kw):
    assign('name', 'char_name', 'Unnamed')
    assign('description', 'char_description', 'No description')
    assign('attack', 'attack', 0)
    assign('health', 'health', 0)
    assign('group', 'group', 0)
    def skill_wrapper(raw_skills:list, **kw):
        return list(map(lambda x:kw['skill'](skill_dict_builder(x, **kw)), raw_skills))
    assign('skill', 'skill', [], skill_wrapper)
    def null_func(*a, **k):
        pass
    assign('inits', 'inits', {"func": null_func}, effect_builder)

@dict_assigning
def skill_dict_builder(s:dict, *, assign: Callable, **kw):
    assign('name', 'skill_name', 'Unnamed')
    assign('description', 'skill_description', 'No description')
    assign('type', 'skill_type', c.SkillType.PASSIVE)
    assign('infinite', 'infinite', False)
    assign('choose', 'choose', False)
    assign('cost', 'cost', NotImplemented)
    assign('usecondition', 'usecondition', NotImplemented)
    assign('choosearea', 'choosearea', NotImplemented)
    assign('choosecondition', 'choosecondition', NotImplemented)
    assign('choosecount', 'choosecount', NotImplemented)
    assign('choosecount_dynamic', 'choosecount_dynamic', NotImplemented)
    def null_func(*a, **k):
        pass
    assign('effect', 'effect', {"func": null_func}, effect_builder)

def effect_builder(e:dict, **kw):
    return [kw['effect']({"type": c.EffectType.EXTERNAL, "func": PyEffect(e), "condition": e.get("condition", True)})]

def safe_exec(code, api=None):
    tree = ast.parse(code, mode='exec')
    code_obj = compile(tree, '<string>', 'exec')

    if api is None:
        api = {}
    namespace = {}
    allowed_builtins = {"print": print, "list": list, "dict": dict, "range": range, "len": len}
    exec(code_obj, globals={'__builtins__': allowed_builtins}, locals=namespace)
    
    return namespace['main'](api)

def char_loader(code, api, **kw):
    return char_dict_builder(safe_exec(code, api), **kw)

class Api:
    def __init__(self, **kw):
        self.__dict__.update(kw)

class PyEffect:
    def __init__(self, data:dict):
        self.func = data["func"]

    def __call__(self, **kw):
        self.func(**kw)
