from convertor_class import *


def queryAttribute(_target, _db):
    _db.rels = {}
    del_table = set()
    for table in _db.tables.values():
        table.foreign = []
        flag = False
        for att_name in table.attlist.keys():
            if att_name == _target:
                flag = True
                break
        if not flag:
            del_table.add(table.name)
    if len(del_table) == len(_db.tables):
        return None
    for t_name in del_table:
        _db.tables.pop(t_name)
        ###
        if t_name in _db.ertables:
            _db.ertables.pop(t_name)
        ###
    return _db


def queryRelation(_target, _db):
    new_db = tree(_db.fpath)
    new_db.name = _db.name
    new_table = {}
    new_ertable = {}
    new_rel = {}
    mem = []
    for rel in _db.rels.keys():
        if rel == _target:
            new_rel[rel] = _db.rels[rel]
            mem = _db.rels[rel].member
    if len(new_rel) == 0:
        return None
    new_db.rels = new_rel
    for t_name in _db.tables.keys():
        if t_name in mem:
            new_fk = []
            new_table[t_name] = _db.tables[t_name]
            for fk in _db.tables[t_name].foreign:
                if fk.table in mem:
                    new_fk.append(fk)
            new_table[t_name].foreign = new_fk
    new_db.tables = new_table
    new_db.ertables = new_table
    return new_db


def queryEntity(_target, _db):
    flag = False
    entity_name = set()
    new_relation = {}
    for t_name in _db.tables.keys():
        if t_name != _target:
            entity_name.add(t_name)
    if len(entity_name) == len(_db.tables):
        return None

    for name, rel in _db.rels.items():
        if (rel.member[0] == _target or rel.member[1] == _target):
            new_relation[name] = rel
            if (not rel.member[0] == _target and rel.member[0] in entity_name):
                entity_name.remove(rel.member[0])
            if (not rel.member[1] == _target and rel.member[1] in entity_name):
                entity_name.remove(rel.member[1])
    _db.rels = new_relation

    for del_name in entity_name:
        _db.tables.pop(del_name)
        ###
        if del_name in _db.ertables:
            _db.ertables.pop(del_name)
        ###

    for table in _db.tables.values():
        new_foreign = []
        for fk in table.foreign:
            if (fk.table not in entity_name):
                new_foreign.append(fk)
        table.foreign = new_foreign
    return _db
