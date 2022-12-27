SELECT * FROM course_catalog.Course;

SELECT "hello, world!";
SELECT 2 + 2;

-- Select everything ( all the coloumns) from the Course table. 
SELECT * FROM Course;

-- Select the title coloumn from the Course table.
SELECT title  FROM Course;

-- SELECT title, prefix, number coloumns
SELECT title, prefix, number  FROM Course;

-- SELECT  prefix, number and title of cmpt courses.
SELECT title, prefix, number   -- which coloumns
FROM Course					-- which table
WHERE prefix =" CMPT"     -- which rows 
ORDER BY title  ;     -- which order

select """";
-- to limit rows there is limit to ... rows on top dropdown buttton.

-- All courses in order of max credits
SELECT *
FROM Course
ORDER By maxCredits DESC;

-- Number of rows
SELECT COUNT(*)
FROM Course;

-- Gives you classes that has computers in the description 
SELECT *
FROM Course
WHERE description LIKE "%computers%";

-- if there is "%the" then it gives you all that starts with the and if there is "the%" it gives you all that ends with the
-- when used with like
-- % stands in for any string (0 or more characters) 

SELECT 5 +7;
SELECT POW(2,3);

-- logic 
SELECT 5> 2; -- 1 TRUE
SELECT 3<= 3;
SELECT 5<>0 ; -- 0 (FALSE)

SELECT NULL > 0 ; -- GIVES YOU NULL
SELECT NULL < 0 ;
SELECT NULL <> 0 
SELECT NULL = 0;  

-- USE IS FOR NULL 
SELECT *
FROM Course
WHERE minCredits IS NULL;

SELECT COUNT(*)
FROM Course
WHERE minCredits IS NOT NULL;

SELECT * FROM TitleType;

-- SELECT * FROM Title;
-- WHERE id = 34203;

-- SELECT * FROM EpisodeOf;
-- LIMIT 100;

SELECT COUNT(*)
FROM Title;



SELECT COUNT(*)
FROM Title
WHERE typeId = 11
;

SELECT *
FROM Title
ORDER BY runtime DESC;

SELECT COUNT(*)
FROM EpisodeOf
WHERE seriesId ='58796';

describe title;
describe TitleType;

select * 
from Title 
where id = 1000 ;


DESCRIBE Course; 

SELECT primaryTitle, originalTitle, averageRating, numVotes
From Title 
Inner Join Rating On Title.id = Rating.titleid
Inner Join HasGenre On Rating.titleid = HasGenre.titleid
Inner Join Genre On HasGenre.genreid = Genre.id
WHERE startYear = 2001
ORDER By averageRating desc, primaryTitle asc;















