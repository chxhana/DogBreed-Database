-- MariaDB dump 10.19  Distrib 10.6.4-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: kdl1113_course_schedule
-- ------------------------------------------------------
-- Server version	10.3.23-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Classroom`
--

DROP TABLE IF EXISTS `Classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Classroom` (
  `id` int(10) unsigned NOT NULL,
  `building` varchar(20) NOT NULL,
  `room` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Classroom`
--

LOCK TABLES `Classroom` WRITE;
/*!40000 ALTER TABLE `Classroom` DISABLE KEYS */;
INSERT INTO `Classroom` VALUES (136,'Meldrum','170'),(255,'Malouf','202'),(406,'Meldrum','220'),(457,'Meldrum','160'),(462,'Meldrum','120');
/*!40000 ALTER TABLE `Classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Course`
--

DROP TABLE IF EXISTS `Course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Course` (
  `prefix` varchar(6) NOT NULL,
  `number` varchar(6) NOT NULL,
  `section` varchar(6) NOT NULL,
  `credits` tinyint(3) unsigned NOT NULL,
  `title` varchar(50) NOT NULL,
  `instructor` varchar(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`prefix`,`number`,`section`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Course`
--

LOCK TABLES `Course` WRITE;
/*!40000 ALTER TABLE `Course` DISABLE KEYS */;
INSERT INTO `Course` VALUES ('CMPT','150','01LC',3,'Math & Tech of Ent. Arts','Gagne'),('CMPT','190','01',2,'Learning to Code','Gagne,Hu'),('CMPT','201','01',4,'Intro to Computer Science','Hu'),('CMPT','210','01',2,'Just Enough Java','Gagne'),('CMPT','215','01',1,'Emerging Scholars','Hu'),('CMPT','251','01',4,'Computer Systems & Programming','Lenth'),('CMPT','306','01',4,'Algorithms','Hu'),('CMPT','307','01',4,'Databases','Lenth'),('CMPT','352','01',4,'Computer Networks','Gagne'),('CMPT','375','01',4,'Web Applications','Lenth'),('CMPT','385','01',1,'Senior Project Proposal Wrtg','Hu,Lenth');
/*!40000 ALTER TABLE `Course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MeetsIn`
--

DROP TABLE IF EXISTS `MeetsIn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MeetsIn` (
  `coursePrefix` varchar(6) NOT NULL,
  `courseNumber` varchar(6) NOT NULL,
  `courseSection` varchar(6) NOT NULL,
  `classroomId` int(10) unsigned NOT NULL,
  `days` set('Sun','Mon','Tue','Wed','Thu','Fri','Sat') DEFAULT NULL,
  PRIMARY KEY (`coursePrefix`,`courseNumber`,`courseSection`,`classroomId`),
  KEY `classroomId` (`classroomId`),
  CONSTRAINT `MeetsIn_ibfk_1` FOREIGN KEY (`coursePrefix`, `courseNumber`, `courseSection`) REFERENCES `Course` (`prefix`, `number`, `section`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `MeetsIn_ibfk_2` FOREIGN KEY (`classroomId`) REFERENCES `Classroom` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MeetsIn`
--

LOCK TABLES `MeetsIn` WRITE;
/*!40000 ALTER TABLE `MeetsIn` DISABLE KEYS */;
INSERT INTO `MeetsIn` VALUES ('CMPT','150','01LC',457,'Mon,Wed'),('CMPT','190','01',462,'Mon,Wed'),('CMPT','201','01',406,'Tue,Thu'),('CMPT','210','01',462,'Mon,Wed'),('CMPT','215','01',255,'Mon,Wed'),('CMPT','251','01',457,'Mon,Wed'),('CMPT','306','01',406,'Mon,Wed'),('CMPT','307','01',136,'Tue,Thu'),('CMPT','352','01',457,'Tue,Thu'),('CMPT','375','01',136,'Tue,Thu');
/*!40000 ALTER TABLE `MeetsIn` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-10 19:18:21
