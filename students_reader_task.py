import datetime
from typing import Union, List, Dict
from collections import namedtuple
from datetime import date, datetime
import os.path
import json

LAB_WORK_SESSION_KEYS = ("date", "presence", "lab_work_n", "lab_work_mark")
STUDENT_KEYS = ("unique_id", "name", "surname", "group", "subgroup", "lab_works_sessions")


class LabWorkSession:
    """
    Информация о лабораторном занятии, которое могло или не могло быть посещено студентом
    """

    def __init__(self, presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: date):
        self._presence = presence
        self._lab_work_number = lab_work_number
        self._lab_work_mark = lab_work_mark
        self._lab_work_date = lab_work_date

    def __new__(cls, presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: date):
        if not cls._validate_args(presence, lab_work_number, lab_work_mark, lab_work_date):
            raise ValueError(f"LabWorkSession ::"
                             f"incorrect args :\n"
                             f"presence       : {presence},\n"
                             f"lab_work_number: {lab_work_number},\n"
                             f"lab_work_mark  : {lab_work_mark},\n"
                             f"lab_work_date  : {lab_work_date}")
        
        return super().__new__(cls)

    @staticmethod
    def _validate_args(presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: date) -> bool:
        """
            param: presence: присутствие студента на л.р.(bool)
            param: lab_work_number: номер л.р.(int)
            param: lab_work_mark: оценка за л.р.(int)
            param: lab_work_date: дата л.р.(date)
        """
        if not presence and lab_work_number != -1:
            return False
        if lab_work_number == -1 and lab_work_mark != -1:
            return False
        if lab_work_date is None and lab_work_number != -1:
            return False
        if lab_work_date is None and lab_work_mark != -1:
            return False
        return True

    def __str__(self) -> str:
        """
            Строковое представление LabWorkSession
            Пример:
            {
                    "presence":      1,
                    "lab_work_n":    4,
                    "lab_work_mark": 3,
                    "date":          "15:12:23"
            }
        """
        return f"\t\t{{\n" \
               f"\t\t\t\"presence\":      {int(self.presence)},\n" \
               f"\t\t\t\"lab_work_n\":    {self.lab_work_number},\n" \
               f"\t\t\t\"lab_work_mark\": {self.lab_work_mark},\n" \
               f"\t\t\t\"date\":          \"{self.lab_work_date.strftime('%d:%m:%y')}\"\n" \
               f"\t\t}}"

    @property
    def presence(self) -> bool:
        return self._presence

    @property
    def lab_work_number(self) -> int:
        return self._lab_work_number

    @property
    def lab_work_mark(self) -> int:
        return self._lab_work_mark

    @property
    def lab_work_date(self) -> date:
        return self._lab_work_date

    @lab_work_number.setter
    def lab_work_number(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError(f"LabWorkSession::lab_work_number::setter arg val error... Type {type(val)} is incorrect")
        if not self._presence:
            raise ValueError(f"LabWorkSession::lab_work_number::new state invalid... Presence is false")
        self._lab_work_number = max(1, val)

    @lab_work_mark.setter
    def lab_work_mark(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError(f"LabWorkSession::lab_work_mark::setter arg val error... Type {type(val)} is incorrect")
        if not self._presence:
            raise ValueError(f"LabWorkSession::lab_work_mark::new state invalid... Presence is false")
        if self._lab_work_number == -1:
            raise ValueError(f"LabWorkSession::lab_work_mark::new state invalid... Lab work number is -1")
        self._lab_work_mark = max(0, val)

    @presence.setter
    def presence(self, value):
        self._presence = value

    @lab_work_date.setter
    def lab_work_date(self, value):
        self._lab_work_date = value


class Student:
    __slots__ = ('_unique_id', '_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int):
        """
            param: unique_id: уникальный идентификатор студента (int)
            param: name: имя студента (str)
            param: surname: фамилия студента (str)
            param: group: номер группы в которой студент обучается (int)
            param: subgroup: номер подгруппы (int)
        """
        if not self._validate_args(unique_id, name, surname, group, subgroup):
            raise ValueError(f"Student::"
                             f"incorrect args:\nname {name},\nsurname {surname},\ngroup {group},\nsubgroup {subgroup}")
        self._unique_id = unique_id
        self._name = name
        self._surname = surname
        self._group = group
        self._subgroup = subgroup
        self._lab_work_sessions: List[LabWorkSession] = []

    @staticmethod
    def _validate_args(unique_id: int, name: str, surname: str, group: int, subgroup: int) -> bool:
        """
            param: unique_id: уникальный идентификатор студента (int)
            param: name: имя студента (str)
            param: surname: фамилия студента (str)
            param: group: номер группы в которой студент обучается (int)
            param: subgroup: номер подгруппы (int)
        """
        # name
        if not isinstance(name, str):
            return False
        if len(name) == 0:
            return False
        # surname
        if not isinstance(surname, str):
            return False
        if len(surname) == 0:
            return False
        # group
        if not isinstance(group, int):
            return False
        if group <= 0:
            return False
        # group
        if not isinstance(subgroup, int):
            return False
        if subgroup <= 0:
            return False
        return True

    def __str__(self) -> str:
        """
        Строковое представление Student
        Пример:
        {
                "unique_id":          26,
                "name":               "Щукарев",
                "surname":            "Даниил",
                "group":              6408,
                "subgroup":           2,
                "lab_works_sessions": [
                    {
                        "presence":      1,
                        "lab_work_n":    1,
                        "lab_work_mark": 4,
                        "date":          "15:9:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    2,
                        "lab_work_mark": 4,
                        "date":          "15:10:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    3,
                        "lab_work_mark": 4,
                        "date":          "15:11:23"
                    },
                    {
                        "presence":      1,
                        "lab_work_n":    4,
                        "lab_work_mark": 3,
                        "date":          "15:12:23"
                    }]
        }
        """
        sep = ',\n'
        return (f"{{\n"
                f"\t\"unique_id\":          {self.unique_id},\n"
                f"\t\"name\":               \"{self.name}\",\n"
                f"\t\"surname\":            \"{self.surname}\",\n"
                f"\t\"group\":              {self.group},\n"
                f"\t\"subgroup\":           {self.subgroup},\n"
                f"\t\"lab_works_sessions\": [\n {sep.join(str(v) for v in self.lab_work_sessions)}]\n"
                f"}}")

    @property
    def unique_id(self) -> int:
        """
        Метод доступа для unique_id
        """
        return self._unique_id

    @property
    def group(self) -> int:
        """
        Метод доступа для номера группы
        """
        return self._group

    @property
    def subgroup(self) -> int:
        """
        Метод доступа для номера подгруппы
        """
        return self._subgroup

    @property
    def name(self) -> str:
        """
        Метод доступа для имени студента
        """
        return self._name

    @property
    def surname(self) -> str:
        """
        Метод доступа для фамилии студента
        """
        return self._surname

    @name.setter
    def name(self, val: str) -> None:
        """
        Метод для изменения значения имени студента
        """
        assert isinstance(val, str)
        assert len(val) != 0
        self._name = val

    @surname.setter
    def surname(self, val: str) -> None:
        """
        Метод для изменения значения фамилии студента
        """
        assert isinstance(val, str)
        assert len(val) != 0
        self._name = val

    @property
    def lab_work_sessions(self):
        """
        Метод доступа для списка лабораторных работ, которые студент посетил или не посетил.
        Использовать yield.
        """
        for s in self._lab_work_sessions:
            yield s

    def append_lab_work_session(self, session: LabWorkSession):
        """
        Метод для регистрации нового лабораторного занятия
        """
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

    result = LabWorkSession(
        bool(json_node['presence']),
        int(json_node['lab_work_n']),
        int(json_node['lab_work_mark']),
        datetime.strptime(json_node['date'].strip('"'), "%d:%m:%y").date()
    )

    return result


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
    lab_session = []
    students = []

    for line in lines[1:]:
        line_lst = line.strip().split(';')
        lab_session.append(dict(zip(headers[5:], line_lst[5:])))

    for line in lines[1::4]:
        line_lst = line.replace('"', "").split(';')[:-1]
        student_dict = dict(zip(headers[:5], line_lst[:5]))
        student_dict['lab_works_sessions'] = []
        for i in range(4):
            student_dict['lab_works_sessions'].append(lab_session[0])
            del lab_session[0]
        students.append(_load_student(student_dict))

    return students


def load_students_json(file_path: str) -> Union[List[Student], None]:
    """
    Загрузка списка студентов из json файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None

    students_raw: Dict[int, Student] = {}

    with open(file_path, 'rt', encoding='utf-8') as input_file:
        try:
            json_data = json.load(input_file)
            students_list = json_data.get("students", [])

            for student_data in students_list:
                unique_id = student_data.get("unique_id")
                if unique_id is not None:
                    students_raw[unique_id] = _load_student(student_data)
        except json.JSONDecodeError as ex:
            print(ex)

    return list(students_raw.values())


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

    assert isinstance(file_path, str)

    headers = list(STUDENT_KEYS[:-1])
    headers.extend(list(LAB_WORK_SESSION_KEYS))

    with open(file_path, 'w', encoding='utf-8') as output_file:
        header_line = ';'.join(headers)
        output_file.write(f'{header_line}\n')

        for student in students:
            for lab_work in student.lab_work_sessions:
                data = [
                        student.unique_id,
                        student.name,
                        student.surname,
                        student.group,
                        student.subgroup,
                        lab_work.lab_work_date.strftime('%d:%m:%y'),
                        int(lab_work.presence),
                        lab_work.lab_work_number,
                        lab_work.lab_work_mark
                ]
                line = ';'.join(str(x) for x in data)

                output_file.write(f'{line}\n')


if __name__ == '__main__':
    # Задание на проверку json читалки:
    # 1. прочитать файл "students.json"
    # 2. сохранить прочитанный файл в "saved_students.json"
    # 3. прочитать файл "saved_students.json"
    # Задание на проверку csv читалки:
    # 1.-3. аналогично

    # students = load_students_json('students.json')
    # save_students_json('students_saved.json', students)

    students = load_students_csv('students.csv')
    save_students_csv('students_saved.csv', students)
    students = load_students_csv('students_saved.csv')

    for s in students:
        print(s)
