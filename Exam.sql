 DRop table if exists book;
 
 Create Table Series(
 id INT auto_increment,
 title varchar(64) not null,
 primary key(id)
 
 );
 
  Create Table Author(
 id INT auto_increment,
 name varchar(64) not null,
 birthYear int not null,
 deathYear int,
 primary key(id)
 
 );
 
 Create Table BookInSeries(
 Bookid INT unique,
 Seriesid INT, 
 number int,
 primary key(Bookid, Seriesid)
 
 );
 
 


  