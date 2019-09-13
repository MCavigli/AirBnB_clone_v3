def get(req, cls_str, cls, id_only=False):
    ''' '''
    _set = set()
    cls_array = req.get(cls_str)
    if cls_array:
        for _id in cls_array:
            found = storage.get(cls, _id)
            if id_only:
                _set.add(found.id)
            else:
                _set.add(found)
    return _set


def populate(parent_list, child_prop):
    ''' '''
    _set = set()
    for p in parent_list:
        for child in getattr(p, child_prop):
            _set.add(child)
    return _set
