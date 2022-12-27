SELECT * FROM Food;

SELECT * FROM Cuisine;

SELECT * FROM FoodCategory;

SELECT * FROM Category;

-- Add pizza to Food
-- INSERT INTO Food (name, cuisine) VALUES
   -- ("Momo", NULL);
   
   -- Add cusine
   INSERT INTO Cuisine(name) VALUES
   ('Nepalese');
   
   INSERT INTO Food(name, cuisine) VALUES
   ('Momo',2);
   
   INSERT INTO Food(name, cuisine) VALUES
   ('Chicken curry',2);
   
   INSERT INTO Food(name, cuisine) VALUES
   ('Thakali Thali',2);
   
   SELECT * FROM Food;
   INSERT INTO Food(name, cuisine) VALUES
   ('Chicken curry',2);
    SELECT * FROM Food;
    
    INSERT 
    INTO Category(name)VALUES
    ('Side Dish');
    
    INSERT
    INTO FoodCategory(food,category)VALUES
    (10,3);
    
    SELECT * FROM FoodCategory;
    
    -- see every food and its categories
      SELECT Food.name, Category.name 
      FROM Food
      inner join FoodCategory ON Food.id = FoodCategory.food
      inner join Category on FoodCategory.category = Category.id;
    
    -- I want to change the name of Pizza to Mexican Pizza
    Update Food
    SET name = "Gorakhali MOMO"
    WHERE name = "MOMO";
    
    SELECT * FROM Food;
    
    -- now change its cuisine 
    UPDATE Food
    SET cuisine = 2
    where id = 2;
    
    
    -- delete food
    DELETE
    FROM Food
    WHERE id = 3;
    
    
  
    
	INSERT INTO Food(name, cuisine) VALUES
   ('Momo',2);
   
     SELECT * FROM Food;
     
     -- <Moving to acitivity classes
     -- all classes and prof that teach the class; does not show if there is no prof
     SELECT *
     FROM Class 
     INNER JOIN Professor ON Class.prof_id = Professor.id 
     ORDER By Class.number;
     
     -- all class even the ones that do not have prof
     -- all rows of left table
     SELECT *
     FROM Class 
     LEFT JOIN Professor ON Class.prof_id = Professor.id 
     ORDER By Class.number;
     
     -- SELECT FROM .... Whichever table you mention first is left then you are inner joining another table that becomes right.
    
    -- all rows of right table
    SELECT *
     FROM Class 
     RIGHT JOIN Professor ON Class.prof_id = Professor.id 
     ORDER By Class.number;
     -- all class that do not have an assigned professor
     
     SELECT *
     FROM Class
     LEFT JOIN Professor 
     ON Class.prof_id = Professor.id
     WHERE Professor.id is NULL ;
    
    -- info all prof that are not assigned to any class
    SELECT *
     FROM Class
     RIGHT JOIN Professor 
     ON Class.prof_id = Professor.id
     WHERE Class.id is NULL ;
     
     -- see info all classes even w/o prof 
     -- classes w/o professor show "staff" for prof name
     SELECT Class.number, Class.section, Class.name,
     COALESCE(Professor.name , "STAFF" ), Professor.department
     FROM Class
     LEFT JOIN Professor 
     ON Class.prof_id = Professor.id
;

-- To keep all foods (even those without categories), we need "two" Left joins
-- because the nonmatching  rows of Food.FoodCategory would not matcg up with rows of category
SELECT Food.name, Category.name
FROM Food
Left Join FoodCategory ON Food.id = FoodCategory.Food
Left Join Category ON FoodCategory.category = Category.id;


-- A single right join, by bringing 
-- in the table that has nonmatching rows (food) "last"

SELECT Food.name, Category.name
FROM Category
Inner Join Category ON FoodCategory.category = Category.id
Right Join FoodCategory ON FoodCategory.Food =Food.id ;

-- if tables do not ,match up put them last and do the right join

SELECT *
FROM Food
INNER JOIN Cuisine
	ON Food.cuisine = Cuisine.id
ORDER BY Food.name
;
SELECT *
FROM Food
RIGHT JOIN Cuisine
	ON Food.cuisine = Cuisine.id
ORDER BY Food.name
;
 
SELECT COALESCE(Food.name, '(no foods yet)'), Cuisine.name
FROM Food
RIGHT JOIN Cuisine
	ON Food.cuisine = Cuisine.id
ORDER BY Food.name
;

 SELECT * FROM Cuisine;    
 
SELECT COUNT(*)
FROM Food
	RIGHT JOIN Cuisine ON Food.cuisine = Cuisine.id
WHERE Food.name is NULL;


SELECT *
FROM Category
	INNER JOIN FoodCategory ON Category.id = FoodCategory.category
   	 RIGHT JOIN Food ON FoodCategory.food = Food.id
     
     UNION


SELECT *
FROM Food
INNER JOIN FoodCategory
	ON Food.id = FoodCategory.food
RIGHT JOIN Category
	ON FoodCategory.category = Category.id;


INSERT into Developer ( id, name ,team_name)Values
(30040,"JengoSurendra", "Bob" );

SELECT * From Developer;
 
 DELETE FROM Project
 WHERE code = "Ganymede";
 
 SELECT * From Project;
  DELETE FROM Team
 WHERE name = "Hopper";    
SELECT * From Team;  
 SELECT * From Team;    
  SELECT * From Developer; 
  
   DELETE FROM Developer
 WHERE team_name = "Hopper";
 
 SELECT * from Team;
 
DELETE FROM Developer
 WHERE team_name = "Hopper";
 
 SELECT * from Team;
  SELECT * from Team;
delete FROM Project where code = 'Saturn';
  SELECT * from Project;
  
    select avg (averageRating)
  from EpisodeOf
  Inner Join Rating on Rating.titleId = EpisodeOf.episodeId
  Where seriesId = 944947;

select  TitleType.text , Count(Title.id)
from Title 
inner join TitleType
on Title.id = TitleType.id
group by  typeId ;

select  TitleType.text , Count(Title.id)
from Title 
inner join TitleType
on Title.typeId = TitleType.id
group by typeId ;


select  TitleType.text , Count(Title.id) AS titles
from Title 
inner join TitleType
on Title.typeId = TitleType.id
group by typeId 
ORDER BY COUNT(Title.id);

  INSERT INTO Book(id, title, authorId, year) VALUES
   (33, "The Alchemist",145, 1988); 
  
  -- Select * from Book;
  
  
select avg (averageRating)
from EpisodeOf
Inner Join Rating on Rating.titleId = EpisodeOf.episodeId
Where seriesId = 944947;


Select * from TitleType; 
  
select AVG(averageRating) as Average_Rating, Genre.text
FROM  Rating
INNER JOIN HasGenre on Rating.titleId = HasGenre.titleId
INNER JOIN Genre ON Genre.id = HasGenre.genreId
INNER JOIN Title ON Title.id = Rating.titleId
WHERE Title.typeId = 2
group by Genre.id
HAVING Average_Rating >= 7.0;

SELECT Count(personId) as credits, Person.name 
From Person
Inner Join WorkedOn
On WorkedOn.personId = Person.id
group by Person.id
Having credits >= 2000;

INSERT INTO Author (id, name, birthYear, deathYear) VALUES
   (1, "Suzanne Collins" ,1962, Null); 
   
    INSERT INTO Series (id, title) VALUES
   (01, "The Hunger Games" );
   
   INSERT INTO Book(id, title, authorId, year) VALUES
   (100, "The Hunger Games",1, 2008); 
   
    INSERT INTO BookInSeries(bookId, seriesId,  number) VALUES
   (100, 01, 1); 
   
    Select * from Author;
    
  -- imdb how many many titles are before the average startyear
  Select count(*)
    from Title
    Where startYear < (
    select avg(startYear)
    from Title);
    
    
    
    --  sales all the items having highest unit price
    
	Select *
    from Item
    where unit_price = (
		select MAX(unit_price)
		from Item
	);
    
    -- who are the customers who have purchased a bulletproof desk
    select * 
    from Customer
    inner join Invoice on Customer.num = Invoice.num
    inner join InvoiceLine on Invoice.num = InvoiceLine.invoice_num
    where InvoiceLine.item_code =(
    select code
    from Item
    where description = "bulletproof desk");
    
    select * 
    from Customer
    inner join Invoice on Customer.num = Invoice.num
    inner join InvoiceLine on Invoice.num = InvoiceLine.invoice_num
    where InvoiceLine.item_code in (
    select code
    from Item
    where description like "%bulletproof%");
