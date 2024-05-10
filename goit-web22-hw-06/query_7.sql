SELECT *
FROM grades
WHERE subject_id = 3
AND student_id IN (
    SELECT id
    FROM students
    WHERE group_id = 1
);
