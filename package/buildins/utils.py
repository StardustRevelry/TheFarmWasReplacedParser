def dict_merge(dicts):
    #"""合并多个字典，后面的字典会覆盖前面的键值"""
    result = {}
    for d in dicts:
        for k in d:
            result[k] = d[k]  # 相同键时，后出现的值会覆盖前面的值
    return result


def dict_update(d, u, merge=True):
    #"""更新字典d，使用字典u的内容
    #
    # Args:
    #     d: 要被更新的字典
    #     u: 提供更新内容的字典
    #     merge: 是否合并模式，为False时跳过已存在的键
    #"""
    for k in u:
        if not merge and k in d:
            continue  # 非合并模式且键已存在时跳过
        d[k] = u[k]  # 更新或添加键值对
    return d


def dict_copy(d):
    #"""创建字典的浅拷贝"""
    return dict_merge([d])  # 通过合并单个字典实现拷贝


def list_copy(lst):
    #"""创建列表的浅拷贝"""
    new_lst = []
    for i in lst:
        new_lst.append(i)
    return new_lst


def list_slice(lst, start, end):
    #"""实现列表切片功能，支持负数索引和边界处理"""
    length = len(lst)

    # 处理 start 的默认值和负数索引
    if start == None:
        start = 0
    elif start < 0:
        start = max(length + start, 0)  # 负数索引转换为正数
    else:
        start = min(start, length)  # 确保不超过列表长度

    # 处理 end 的默认值和负数索引
    if end == None:
        end = length
    elif end < 0:
        end = max(length + end, 0)  # 负数索引转换为正数
    else:
        end = min(end, length)  # 确保不超过列表长度

    # 确保 start 和 end 的合理性
    start = max(0, start)
    end = max(0, end)

    # 提取子列表
    result = []
    for i in range(start, end):
        if i < length:  # 防止索引越界
            result.append(lst[i])
    return result


def reversed(lst):
    #"""反转列表顺序"""
    _l = []
    for i in range(len(lst) - 1, -1, -1):  # 从后往前遍历
        _l.append(lst[i])
    return _l


def any(lst, condition):
    #"""判断列表中是否存在满足条件的元素
    #   Args:
    #       lst: 列表
    #       condition: 条件函数，接收元素作为参数，返回True或False
    #   Returns:
    #       True/False
    #"""
    def _condition(i):
        return i
    if condition == None:
        condition = _condition
    for i in lst:
        if condition(i):
            return True
    return False


def all(lst, condition):
    #"""判断列表中是否所有元素都满足条件
    #   Args:
    #       lst: 列表
    #       condition: 条件函数，接收元素作为参数，返回True或False
    #   Returns:
    #       True/False
    #"""
    def _condition(i):
        return i
    if condition == None:
        condition = _condition
    for i in lst:
        if not condition(i):
            return False
    return True


def item_in_lst(lst, item, key):
    #"""判断列表中是否存在指定元素
    #   Args:
    #       lst: 列表
    #       item: 指定元素
    #       keys: 用于比较的键，默认为空，表示直接比较元素
    #   Returns:
    #       True/False
    #"""
    for i in lst:
        if key:
            if i[key] == item[key]:
                return True
        else:
            if i == item:
                return True
    return False