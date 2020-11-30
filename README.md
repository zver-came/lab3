Назва: лабораторна робота №3 "Засоби оптимізації роботи СУБД PostgreSQL".
Структура: база даних описує предметну галузь "Університет" та складається із наступних таблиць:
teacher_student(збереження зв'язків між вчителями та студентами),
teachers (збереження інформації про вчителів), 
students (для збереження даних про студентів), 
student_phone (список телефонних номерів студентів), 
teacher_email (список електронних адрес вчителя), 
groups (список груп до яких належать студенти), 
subjects (список предметів які викладаються вчителями).
Зв'язки: 
"teachers" 1:N "teacher_student", 
"students" 1:N "teacher_student",
"groups" 1:N "students",
"student_phone" N:1 "students",
"subjects" 1:N "teachers"
"teacher_email" N:1 "teachers".
