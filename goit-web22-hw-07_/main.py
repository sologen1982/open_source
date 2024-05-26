from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    SELECT
        groups.name AS group_name,
        ROUND(AVG(grades.grade), 2) AS average_grade
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN groups ON students.group_id = groups.id
    GROUP BY groups.name;
    """
    result = session.query(Group.name.label('group_name'), func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).join(Group).group_by(Group.name).all()
    return result


def select_04():
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).all()
    return result


def select_05():
    """
    SELECT *
    FROM subjects
    WHERE teacher_id = 2;
    """
    result = session.query(Subject.name).filter(Subject.teacher_id == 2).all()
    return result


def select_06():
    """
    SELECT *
    FROM students
    WHERE group_id = 3;
    """
    result = session.query(Student.fullname).select_from(Group).join(Student).filter(Group.id == 3).all()
    return result


def select_07():
    """
    SELECT *
    FROM grades
    WHERE subject_id = 3
    AND student_id IN (
        SELECT id
        FROM students
        WHERE group_id = 1
    );
    """
    subquery = session.query(Student.id).filter(Student.group_id == 1).subquery()
    result = session.query(Grade.id, Grade.student_id, Grade.subjects_id, Grade.grade, Grade.grade_date) \
        .join(subquery, Grade.student_id == subquery.c.id) \
        .filter(Grade.subjects_id == 3).all()
    return result


def select_08():
    """
    SELECT ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN subjects s ON g.subject_id = s.id
    WHERE s.teacher_id = 2;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade) \
        .join(Subject).filter(Subject.teacher_id == 2).all()
    return result


def select_09():
    """
    SELECT DISTINCT s.name AS subject_name
    FROM subjects s
    JOIN grades g ON s.id = g.subject_id
    WHERE g.student_id = 20;
    """
    result = session.query(Subject.name).distinct() \
        .join(Grade).filter(Grade.student_id == 20).all()
    return result


def select_10():
    """
    SELECT DISTINCT s.name AS subject_name
    FROM subjects s
    JOIN grades g ON s.id = g.subject_id
    JOIN teachers t ON s.teacher_id = t.id
    WHERE g.student_id = 15 AND t.id = 2;
    """
    result = session.query(Subject.name).distinct() \
        .join(Grade).join(Teacher).filter(and_(Grade.student_id == 15, Teacher.id == 2)).all()
    return result




def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    # print(select_01())
    # print(select_02())
    # print(select_03())
    # print(select_04())
    # print(select_05())
    # print(select_06())
    # print(select_07())
    # print(select_08())
    # print(select_09())
    print(select_10())
    # print(select_12())

