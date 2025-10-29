from random import random

from .utils import *

def super(cls, ins):
    #"""模拟super()函数，用于方法解析顺序(MRO)中的父类查找"""
    mro = ins["__mro__"]  # 获取类的MRO列表

    def bind(cls, ins):
        #"""将类的方法绑定到实例上"""
        new_cls = dict_copy(cls)
        for n in cls["__methods__"]:
            m = cls[n]

            def __t(args=(), kwargs={}, _m=m, _ins=ins):
                return _m(_ins, args, kwargs)  # 将实例作为第一个参数传递

            new_cls[n] = __t
        return new_cls

    _next = False
    for c in mro:
        if _next:
            return bind(c, ins)  # 返回下一个类的绑定版本
        if c["__id__"] == cls["__id__"]:
            _next = True  # 找到当前类，下一个就是父类
    return None


def __build_class__(cls, name, bases=()):
    #"""类构建函数，模拟Python的类创建过程"""

    def __new__(args=(), kwargs={}):
        #"""实例创建方法"""
        self = dict_copy(cls)  # 创建类副本作为实例
        cls["__init__"](self, args, kwargs)  # 调用初始化方法
        self["__id__"] = random()  # 设置实例ID

        # 将类方法绑定到实例
        for n in cls["__methods__"]:
            m = cls[n]

            def __t(args=(), kwargs={}, _m=m, _self=self):
                return _m(_self, args, kwargs)

            self[n] = __t
        return self

    def __str__(self):
        #"""对象字符串表示"""
        return "<" + cls["__name__"] + " object>"

    def __mro__():
        #"""计算方法解析顺序(MRO)，使用C3线性化算法"""
        current_mro = [cls]  # 当前MRO，以当前类开始
        base_mros = []
        for b in bases:
            base_mros.append(list_copy(b["__mro__"]))  # 收集所有基类的MRO

        while base_mros:
            heads = []
            for mro in base_mros:
                if not mro:
                    continue
                heads.append(mro[0])  # 收集所有MRO列表的第一个元素

            if not heads:
                break

            current_head = None
            for h in heads:
                if h in current_mro:
                    print("[ERROR] Circular inheritance detected.")  # 检测循环继承
                used = False
                for mro in base_mros:
                    if mro and mro[0]["__id__"] == h["__id__"]:
                        continue
                    if item_in_lst(mro, h, "__id__"):
                        used = True  # 检查h是否在其他MRO的非首位出现
                        break
                if not used:
                    current_head = h  # 找到合适的候选头
                    break

            if not current_head:
                print("[ERROR] Cannot resolve inheritance order.")  # 无法解析继承顺序
                break

            current_mro.append(current_head)  # 将候选头添加到MRO
            # 从所有MRO中移除已处理的头
            for mro in base_mros:
                if mro and mro[0]["__id__"] == current_head["__id__"]:
                    mro.pop(0)
        return current_mro

    cls = cls()  # 初始化类字典
    inner_methods = {
        "__str__": __str__,
        "__repr__": __str__,  # repr也用str表示
    }

    # 合并内部方法、类信息和原始类定义
    cls = dict_merge([
        inner_methods,
        {
            "__id__": random(),  # 设置唯一ID
            "__new__": __new__,
            "__name__": name,  # 设置类名
        },
        cls
    ])

    __class__ = dict_copy(cls)  # 创建类副本
    # 设置类的元信息
    dict_update(__class__, {
        "__class__": __class__,
        "__dict__": __class__
    })
    cls["__mro__"] = __mro__()  # 设置MRO

    # 处理继承：从MRO中继承除第一个（自身）外的所有类的方法
    if len(bases) > 0:
        for b in list_slice(cls["__mro__"], 1, None):
            dict_update(cls, b, False)  # 更新类字典，并保持子类优先级

    # 处理类方法：将类方法绑定到类
    if "__classmethod__" in cls:
        for n in cls["__classmethod__"]:
            m = cls[n]

            def __t(args=(), kwargs={}, _m=m, _cls=cls):
                return _m(_cls, args, kwargs)  # 将类作为第一个参数传递

            cls[n] = __t

    cls["__mro__"][0] = cls
    return cls  # 返回构建完成的类