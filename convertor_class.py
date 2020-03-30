import xml.etree.ElementTree as ET
from copy import deepcopy
import os


class attribute(object):

    def __init__(self, _name, _type='varchar', _notnull=False, _default=None):
        self.name = _name
        self.type = _type
        self.bit = None
        self.notNull = _notnull
        self.default = _default
        # multivalue
        self.multi = False
        ###


class foreignkey(object):

    def __init__(self, _name, _table, _target):
        self.name = _name
        self.table = _table
        self.target = _target


class table(object):

    def __init__(self, _name):
        self.name = _name
        self.attlist = {}
        self.primary = []
        self.foreign = []
        # partial key
        self.partial = []
        ###
        self.weak = False

    def AddAtt(self, att):
        self.attlist[att.name] = att


class relation(object):

    def __init__(self, _name):
        self.name = _name
        self.member = []
        self.value = []
        self.cardinality = []
        self.ref = []
        self.build = False


class tree(object):

    def __init__(self, _file):
        self.fpath = _file
        self.name = None
        self.tables = {}
        # record er_tables
        self.ertables = {}
        ###
        self.rels = {}
        self.parse(self.fpath)

    def parse(self, _fname):
        _t = ET.parse(_fname)
        _r = _t.getroot()

        for child in _r.findall('Entity'):
            temp_table = table(child.get('name'))
            if (child.get('weak') == 'True'):
                temp_table.weak = True
            for grandchild in child:
                att_name = grandchild.get('name')
                temp_att = attribute(att_name)
                temp_att.type = grandchild.get('type')
                temp_att.default = grandchild.get('default')
                temp_att.bit = grandchild.get('bit')
                # parse multi
                if (grandchild.get('multi') == 'True'):
                    temp_att.multi = True
                ###
                if (grandchild.get('notNull') == 'True'):
                    temp_att.notNull = True
                if (grandchild.get('Part') == 'True' or grandchild.get('PK') == 'True'):
                    temp_table.primary.append(att_name)
                    # parse partial key
                    if grandchild.get('Part') == 'True':
                        temp_table.partial.append(att_name)
                    ###
                temp_table.AddAtt(temp_att)
            self.tables[temp_table.name] = temp_table
            ###
            self.ertables[temp_table.name] = deepcopy(temp_table)
            ###

        for child in _r.findall('Relation'):
            temp_rel = relation(child.get('name'))
            for grandchild in child:
                temp_rel.member.append(grandchild.get('name'))
                temp_rel.value.append(grandchild.get('value'))
                temp_rel.cardinality.append(grandchild.get('Cardinality'))
                temp_rel.ref.append(grandchild.get('ref'))
            if (temp_rel.cardinality[0] == 'many' and temp_rel.cardinality[1] == 'many'):
                temp_rel.build = True
            if not temp_rel.build:
                if (temp_rel.cardinality[0] == 'many' or temp_rel.cardinality[1] == 'many'):
                    for i in range(len(temp_rel.member)):
                        if temp_rel.cardinality[i] == 'many':
                            fk = foreignkey(temp_rel.ref[i], temp_rel.member[
                                            1 - i], temp_rel.ref[1 - i])
                            self.tables[temp_rel.member[i]].foreign.append(fk)
                            ###
                            self.ertables[temp_rel.member[
                                i]].foreign.append(fk)
                            ###
                elif (temp_rel.cardinality[0] == 'one' and temp_rel.cardinality[1] == 'one'):
                    att_one_to_one = temp_rel.name + \
                        temp_rel.member[1] + temp_rel.ref[1]
                    new_att = deepcopy(self.tables[temp_rel.member[
                                       1]].attlist[temp_rel.ref[1]])
                    new_att.name = att_one_to_one
                    self.tables[temp_rel.member[0]].attlist[
                        att_one_to_one] = new_att
                    self.ertables[temp_rel.member[0]].attlist[
                        att_one_to_one] = new_att
                    fk = foreignkey(att_one_to_one, temp_rel.member[
                                    1], temp_rel.ref[1])
                    self.tables[temp_rel.member[0]].foreign.append(fk)
                    self.ertables[temp_rel.member[0]].foreign.append(fk)

                else:
                    if (temp_rel.member[0] == temp_rel.member[1]):
                        fk = foreignkey(temp_rel.ref[0], temp_rel.member[
                                        0], temp_rel.ref[1])
                        self.tables[temp_rel.member[0]].foreign.append(fk)
                        ###
                        self.ertables[temp_rel.member[0]].foreign.append(fk)
                        ###
            else:
                new_table = table(child.get('name'))
                for i in range(2):
                    temp_att = deepcopy(
                        self.tables[temp_rel.member[i]].attlist[temp_rel.ref[i]])
                    temp_att.name = temp_rel.member[i] + temp_rel.ref[i]
                    new_table.AddAtt(temp_att)
                    new_table.primary.append(temp_att.name)
                    fk = foreignkey(temp_rel.member[
                                    i] + temp_rel.ref[i], temp_rel.member[1 - i], temp_rel.ref[1 - i])
                    new_table.foreign.append(fk)
                self.tables[new_table.name] = new_table
            self.rels[temp_rel.name] = temp_rel


class output(object):

    def __init__(self, _file, _tree):
        self.fname = _file
        self.tree = _tree
        ###
        # self.export_ERD()
        ###
        # self.export()

    def export(self):
        text = open(self.fname, "w")
        for _table in self.tree.tables.values():
            text.write('CREATE TABLE ' + _table.name + '(\n')
            for _att in _table.attlist.values():
                temp = '    ' + _att.name + ' '
                if(_att.type == 'composite'):
                    temp += 'varchar(50)'
                else:
                    temp += _att.type
                    if _att.bit:
                        temp += '(' + _att.bit + ')'
                if _att.notNull:
                    temp += ' ' + 'NOT NULL'
                if _att.default:
                    temp += ' DEFAULT ' + _att.default
                temp += ',\n'
                text.write(temp)

            # primary key
            if _table.primary:
                temp = '    PRIMARY KEY ('
                for pk in _table.primary:
                    temp += pk + ', '
                temp = temp[:-2]
                temp += ')'
                if _table.foreign:
                    temp += '\n'
                text.write(temp)
            text.write('\n);\n\n')
            # foreign key
            # if _table.foreign:
            #     _num = 0
            #     for fk in _table.foreign:
            #         _num += 1
            #         temp = '    FOREIGN KEY (' + fk.name + ') REFERENCES ' + fk.table + '(' + fk.target + ')'
            #         if not (_num == len(_table.foreign)):
            #             temp += ',\n'
            #         text.write(temp)

        # foreign key
        for _table in self.tree.tables.values():
            for fk in _table.foreign:
                temp = 'ALTER TABLE ' + _table.name + ' '
                text.write(temp)
                temp = 'ADD FOREIGN KEY (' + fk.name + ') REFERENCES ' + \
                    fk.table + '(' + fk.target + ');\n\n'
                text.write(temp)
        text.close()

        #     text.write('\n);\n\n')
        # text.close()
    # export .er file
    def export_ERD(self):
        # TODO
        text = open(self.fname, "w")
        for _table in self.tree.ertables.values():
            if _table.weak:
                text.write('[' + _table.name + ']' +
                           '{label: "weak", bgcolor: "#ececfc"}' + '\n')
            else:
                text.write('[' + _table.name + ']' +
                           '{bgcolor: "#d0e0d0"}' + '\n')
            for _att in _table.attlist.values():
                tag = ''
                if _att.name in _table.primary:
                    tag += '*'
                if _att.name in [_table.foreign[i].name for i in range(len(_table.foreign))]:
                    tag += '+'
                if _att.type == 'composite':
                    tag += '&'
                if _att.multi:
                    tag += '@'
                text.write('\"' + tag + ' ' + _att.name + '\"')
                if _att.name in _table.partial:
                    text.write('{label: "partial"}')
                text.write('\n')
            text.write('\n')

        for _rel in self.tree.rels.values():
            _participate = {"partial": "pp", "total": "tp"}
            _cardinality = {"one": "1", "many": "*"}
            text.write(_rel.member[0] + ' ' + _cardinality[_rel.cardinality[0]] +
                       '--' + _cardinality[_rel.cardinality[1]] + ' ' + _rel.member[1] + ' ')
            _label = _rel.name + \
                ' (' + _participate[_rel.value[0]] + \
                ', ' + _participate[_rel.value[1]] + ')'
            text.write('{label:' + '"' + _label + '"' + '}' + '\n')
        text.close()
    ###
