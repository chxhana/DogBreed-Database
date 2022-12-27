SELECT *
from Item
WHERE (unit_price > 15 OR description LIKE "%pan-galactic%" or
unit_price < 20 and code LIKE "%x")
ORDER BY unit_price desc;

SELECT *
FROM Item
Where description LIKE "%bulletproof%"
ORDER BY unit_price DESC
LIMIT 3;

SELECT date, num 
FROM Invoice
WHERE date like "%2003-08%"
ORDER BY date;

SELECT *
from EpisodeOf
where seriesid = 1442437;

SELECT primaryTitle
from Title
where id = 1536241;

SELECT averageRating
From Rating
Where titleid = 1442437 OR titleid = 1536241;



SELECT COUNT(*)
FROM Title
WHERE typeId = 11 and primaryTitle LIKE "%Star Wars%";

SELECT id
FROM Title
WHERE primaryTitle like "%Doctor Who%" and endYear =1989;

SELECT COUNT(*)
FROM EpisodeOf
WHERE seriesID = 56751;

SELECT id 
FROM Title 
WHERE primaryTitle LIKE "Mars Attacks!";

SELECT personId
FROM WorkedOn
WHERE Titleid = 116996;

SELECT name
FROM Person
WHERE id = 197;

SELECT *
FROM Genre;

SELECT COUNT(*)
FROM HasGenre
WHERE genreId = 9;

SELECT count(*)
FROM Rating
where averageRating = 10.0 and numvotes >999;

SELECT Class.name
FROM Class INNER JOIN Tutor
    ON Class.id = Tutor.class_id
WHERE Tutor.id = 184;

SELECT Class.name, Professor.name
FROM Class INNER JOIN Professor
    ON Class.prof_id = Professor.id
WHERE Class.id = 7;

SELECT *
FROM Class inner join Professor
	
	 ON Class.prof_id = Professor.id 
WHERE department like  "%History%";

SELECT Title.primaryTitle, Title.originalTitle, Title.startYear, Genre.text
FROM Title 
Inner Join HasGenre On Title.id = HasGenre.titleid
Inner Join Genre On HasGenre.genreid = Genre.id
WHERE Title.primaryTitle LIKE "%Star Trek%" 
AND Title.startYear is not null
ORDER By Title.startYear;

SELECT primaryTitle, originalTitle, averageRating, numVotes
From Title 
Inner Join Rating On Title.id = Rating.titleid
Inner Join HasGenre On Rating.titleid = HasGenre.titleid
Inner Join Genre On HasGenre.genreid = Genre.id
WHERE startYear = 2001
ORDER By averageRating desc, primaryTitle asc;

