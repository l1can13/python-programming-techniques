from typing import Union, List, Dict
from collections import namedtuple
from datetime import date
import os.path
import json
from datetime import time


LAB_WORK_SESSION_KEYS = ("presence", "lab_work_n", "lab_work_mark", "date")
STUDENT_KEYS = ("unique_id", "name", "surname", "group", "subgroup", "lab_works_sessions")


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
    __slots__ = ('_unique_id', '_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int):
        self._unique_id: int = -1
        self._name:      str = "no name"
        self._surname:   str = "no surname"
        self._group:     int = 1
        self._subgroup:  int = 1
        if not self._build_student(unique_id, name, surname, group, subgroup):
            raise ValueError(f"Student::"
                             f"incorrect args:\nunique_id, \nname {name},\nsurname {surname},\ngroup {group},\nsubgroup {subgroup}")
        self._lab_work_sessions: List[LabWorkSession] = []

    def _build_student(self, unique_id: int, name: str, surname: str, group: int, subgroup: int) -> bool:
        if not isinstance(unique_id,  int) or unique_id < 0:
            return False
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
        self._unique_id = unique_id
        self._name = name
        self._surname = surname
        self._group = group
        self._subgroup = subgroup
        return True

    def __str__(self) -> str:
        sep = ',\n'
        return (f"{{\n"
                f"\t\"unique_id\":          {self.unique_id},\n"
                f"\t\"name\":               \"{self.name}\",\n"
                f"\t\"surname\":            \"{self.surname}\",\n"
                f"\t\"group\":              {self.group},\n"
                f"\t\"subgroup\":           {self.subgroup},\n"
                f"\t\"lab_works_sessions\": [\n {sep.join(str(v)for v in self.lab_work_sessions)}]\n"
                f"}}")
    
    @property
    def unique_id(self) -> int:
        return self._unique_id

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
    
    @unique_id.setter
    def unique_id(self, val) -> None:
        if not isinstance(val, int):
            raise ValueError(f"Student::unique_id::setter arg val error... Type {type(val)} is incorrect")
        if val < 0:
            raise ValueError(f"Student::unique_id::new state invalid... Unique id less then zero")
        self._unique_id = val

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
    """
        Создание из под-дерева json файла экземпляра класса LabWorkSession.
        hint: чтобы прочитать дату из формата строки, указанного в json используйте
        date(*tuple(map(int, json_node['date'].split(':'))))
    """
    for key in LAB_WORK_SESSION_KEYS:
        if key not in json_node:
            raise KeyError(f"load_lab_work_session:: key \"{key}\" not present in json_node")
    return LabWorkSession(True if int(json_node['presence']) == 1 else False,
                          int(json_node['lab_work_n']),
                          int(json_node['lab_work_mark']),
                          time.fromisoformat(json_node['date'])
    )


def _load_student(json_node) -> Student:
    """
        Создание из под-дерева json файла экземпляра класса Student.
        Если в процессе создания LabWorkSession у студента случается ошибка,
        создание самого студента ломаться не должно.
    """
    for key in STUDENT_KEYS:
        if key not in json_node:
            raise KeyError(f"load_student:: key \"{key}\" not present in json_node")
    student = Student(
        int(json_node['unique_id']),
        json_node['name'],
        json_node['surname'],
        int(json_node['group']),
        int(json_node['subgroup'])
        )
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


# csv header
#     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
# unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
UNIQUE_ID = 0
STUD_NAME = 1
STUD_SURNAME = 2
STUD_GROUP = 3
STUD_SUBGROUP = 4
LAB_WORK_DATE = 5
STUD_PRESENCE = 6
LAB_WORK_NUMBER = 7
LAB_WORK_MARK = 8


def load_students_csv(file_path: str) -> Union[List[Student], None]:
    # csv header
    #     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
    # unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'rt', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    headers = lines[0].strip().split(';')
    fields = []
    students = []
    for line in lines:
        try:
            line_lst = line.strip().split(';')
            first = dict(zip(headers[:5], line_lst[:5]))
            first['lab_works_sessions'] = dict(zip(headers[5:], line_lst[5:]))
        except Exception as ex:
            print(ex)
            continue



def load_students_json(file_path: str) -> Union[List[Student], None]:
    """
    Загрузка списка студентов из json файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
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

def get_variable_name(var, namespace=None):
    if namespace is None:
        namespace = globals()
    
    for name, value in namespace.items():
        if value is var:
            return name
    return None

def save_students_json(file_path: str, students: List[Student]):
    """
    Запись списка студентов в json файл
    """
    assert isinstance(file_path, str)
    
    with open(file_path, 'w', encoding='utf-8') as output_file:
        init = f'{{\n\"{get_variable_name(students)}\":[\n'
        output_file.write(init)

        for elem in students[:-1]:
            output_file.write(str(elem) + ',\n')

        output_file.write(str(elem) + '\n')

        output_file.write(']}')

def save_students_csv(file_path: str, students: List[Student]):
    """
    Запись списка студентов в csv файл
    """



if __name__ == '__main__':
    # Задание на проверку json читалки:
    # 1. прочитать файл "students.json"
    # 2. сохранить прочитанный файл в "saved_students.json"
    # 3. прочитать файл "saved_students.json"
    # Задание на проверку csv читалки:
    # 1.-3. аналогично

    # students = load_students_json('students.json')
    # save_students_json('students_saved.json', students)
    # students = load_students_json('students_saved.json')
    
    students = load_students_csv('students.csv')
    # students = save_students_csv('students_saved.csv')
    # load_students_csv('students_saved.csv', students)
    
    # for s in students:
        # print(s)
