SELECT DISTINCT s.name AS subject_name
FROM subjects s
JOIN grades g ON s.id = g.subject_id
JOIN teachers t ON s.teacher_id = t.id
WHERE g.student_id = 15 AND t.id = 2;
