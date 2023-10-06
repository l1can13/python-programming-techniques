import json
import os.path
from datetime import date
from typing import Union, List

LAB_WORK_SESSION_KEYS = ("presence", "lab_work_n", "lab_work_mark", "date")
STUDENT_KEYS = ("name", "surname", "group", "subgroup", "lab_works_sessions")


def _validate_node_keys(node, keys):
    for key in keys:
        if key not in node:
            return False
    return True


class LabWorkSession:
    __slots__ = ('_presence', '_l_w_number', '_l_w_mark', '_date')

    def __init__(self, p: bool, l_w_n: int, l_w_m: int, d: date):
        self._presence: bool = False
        self._l_w_number: int = -1
        self._l_w_mark: int = -1
        self._date: Union[None, date] = None
        if not self._build_session(p, l_w_n, l_w_m, d):
            raise ValueError(f"LabWorkSession::"
                             f"incorrect args:\npresence {p},\nl_w_number {l_w_n},\nl_w_mark {l_w_m},\ndate {d}")

    def _build_session(self, p: bool, l_w_n: int, l_w_m: int, d: date) -> bool:
        '''

        :param p:
        :param l_w_n:
        :param l_w_m:
        :param d:
        :return:
        '''
        if not p and l_w_n != -1:
            return False
        if l_w_n == -1 and l_w_m != -1:
            return False
        if d is None and l_w_n != -1:
            return False
        if d is None and l_w_m != -1:
            return False
        self._presence = p
        self._l_w_number = l_w_n
        self._l_w_mark = l_w_m
        self._date = d
        return True

    @property
    def presence(self) -> bool:
        return self._presence

    @property
    def lab_work_number(self) -> int:
        return self._l_w_number

    @property
    def lab_work_mark(self) -> int:
        return self._l_w_mark

    @property
    def lab_work_date(self) -> date:
        return self._date

    @lab_work_number.setter
    def lab_work_number(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError(f"LabWorkSession::lab_work_number::setter arg val error... Type {type(val)} is incorrect")
        if not self.presence:
            raise ValueError(f"LabWorkSession::lab_work_number::new state invalid... Presence is false")
        self._l_w_number = max(1, val)

    @lab_work_mark.setter
    def lab_work_mark(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError(f"LabWorkSession::lab_work_mark::setter arg val error... Type {type(val)} is incorrect")
        if not self.presence:
            raise ValueError(f"LabWorkSession::lab_work_mark::new state invalid... Presence is false")
        if self.lab_work_number == -1:
            raise ValueError(f"LabWorkSession::lab_work_mark::new state invalid... Lab work number is -1")
        self._l_w_mark = max(0, val)

    def __str__(self) -> str:
        return f"\t\t{{\n"\
               f"\t\t\t\"presence\":      {'1' if self.presence else '0'},\n"\
               f"\t\t\t\"lab_work_n\":    {self.lab_work_number},\n"\
               f"\t\t\t\"lab_work_mark\": {self.lab_work_mark},\n"\
               f"\t\t\t\"date\":          \"{str(self.lab_work_date)}\"\n"\
               f"\t\t}}"


class Student:
    __slots__ = ('_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, name: str, surname: str, group: int, subgroup: int):
        self._name:     str = "no name"
        self._surname:  str = "no surname"
        self._group:    int = 1
        self._subgroup: int = 1
        if not self._build_student(name, surname, group, subgroup):
            raise ValueError(f"Student::"
                             f"incorrect args:\nname {name},\nsurname {surname},\ngroup {group},\nsubgroup {subgroup}")
        self._lab_work_sessions: List[LabWorkSession] = []

    def _build_student(self, name: str, surname: str, group: int, subgroup: int) -> bool:
        # name
        if not isinstance(name,  str):
            return False
        if len(name) == 0:
            return False
        # surname
        if not isinstance(surname,  str):
            return False
        if len(surname) == 0:
            return False
        # group
        if not isinstance(group,  int):
            return False
        if group <= 0:
            return False
        # group
        if not isinstance(subgroup,  int):
            return False
        if subgroup <= 0:
            return False
        self._name = name
        self._surname = surname
        self._group = group
        self._subgroup = subgroup
        return True

    def __str__(self) -> str:
        sep = ',\n'
        return (f"{{\n"
                f"\t\"name\":               \"{self.name}\",\n"
                f"\t\"surname\":            \"{self.surname}\",\n"
                f"\t\"group\":              {self.group},\n"
                f"\t\"subgroup\":           {self.subgroup},\n"
                f"\t\"lab_works_sessions\": [\n {sep.join(str(v)for v in self.lab_work_sessions)}]\n"
                f"}}")

    @property
    def group(self) -> int:
        return self._group

    @property
    def subgroup(self) -> int:
        return self._subgroup

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @name.setter
    def name(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError(f"Student::name::setter arg val error... Type {type(val)} is incorrect")
        if len(val) == 0:
            raise ValueError(f"Student::name::new state invalid... Name is empty")
        self._name = val

    @surname.setter
    def surname(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError(f"Student::surname::setter arg val error... Type {type(val)} is incorrect")
        if len(val) == 0:
            raise ValueError(f"Student::surname::new state invalid... Name is empty")
        self._name = val

    @property
    def lab_work_sessions(self):
        for s in self._lab_work_sessions:
            yield s

    def append_lab_work_session(self, session: LabWorkSession):
        self._lab_work_sessions.append(session)


def _load_lab_work_session(json_node) -> LabWorkSession:
    for key in LAB_WORK_SESSION_KEYS:
        if key not in json_node:
            raise KeyError(f"load_lab_work_session:: key \"{key}\" not present in json_node")
    return LabWorkSession(True if int(json_node['presence']) == 1 else False,
                          int(json_node['lab_work_n']),
                          int(json_node['lab_work_mark']),
                          date(*tuple(map(int, json_node['date'].split(':')))))


def _load_student(json_node) -> Student:
    for key in STUDENT_KEYS:
        if key not in json_node:
            raise KeyError(f"load_student:: key \"{key}\" not present in json_node")
    student = Student(json_node['name'],
                      json_node['surname'],
                      int(json_node['group']),
                      int(json_node['subgroup']))
    for session in json_node['lab_works_sessions']:
        try:
            student.append_lab_work_session(_load_lab_work_session(session))
        except ValueError as er:
            print(er)
            continue
        except KeyError as er:
            print(er)
            continue
        except Exception as er:
            print(er)
            continue
    return student


def load_students(file_path: str) -> Union[List[Student], None]:
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rt', encoding='utf-8') as input_file:
        raw_json = json.load(input_file)
        if 'students' not in raw_json:
            return None
        students = []
        for node in raw_json['students']:
            try:
                students.append(_load_student(node))
            except Exception as ex:
                print(ex)
                continue
        return students

students = load_students('students.json')
for s in students:
    print(s)
