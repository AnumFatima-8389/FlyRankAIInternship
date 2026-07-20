

create type gender AS ENUM ('female','male');

create table Students(
    student_id serial primary key, 
    student_name text not null, 
    student_gender gender
) 
