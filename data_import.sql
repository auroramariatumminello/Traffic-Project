-- MySQL dump 10.13  Distrib 8.0.23, for macos10.15 (x86_64)
--
-- Host: localhost    Database: bluetoothstations
-- ------------------------------------------------------
-- Server version	8.0.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `measurement`
--

DROP TABLE IF EXISTS `measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measurement` (
  `timestamp` datetime(6) NOT NULL,
  `count` int NOT NULL,
  `station` varchar(45) NOT NULL,
  PRIMARY KEY (`timestamp`,`station`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement`
--

LOCK TABLES `measurement` WRITE;
/*!40000 ALTER TABLE `measurement` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `name` varchar(45) NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES ('A22_ML103',46.321,11.2669),('A22_ML107',46.2888,11.2375),('Agip_Einstein',46.4713,11.3166),('Arginale_Palermo',46.4866,11.3345),('Arginale_Resia',46.4826,11.3254),('Buozzi_Fiera',46.4737,11.3258),('caugusta',46.4825,11.3424),('cavour',46.6684,11.1673),('cfirmiano',46.4934,11.3101),('corse_cappuccini',46.6739,11.1594),('Druso mobile',46.4951,11.3389),('Druso_Palermo',46.4951,11.3327),('druso-poste',46.4951,11.3397),('galilei',46.6736,11.1613),('Galilei_Lancia',46.4861,11.3371),('Galilei_Palermo',46.485,11.3326),('Galilei_Roma',46.487,11.3435),('Galilei_Virgolo',46.487,11.3414),('Galleria_Virgolo',46.492,11.3592),('galvani',46.474,11.3317),('goethe_ospedale',46.6768,11.1488),('goethe-alpini',46.6748,11.1558),('hofer',46.6751,11.1524),('huber',46.6729,11.1566),('Laives North',46.4307,11.3454),('Laives South',46.4124,11.3299),('liberta-corse',46.6706,11.1594),('Maso_Pieve',46.4757,11.3375),('mazzini',46.6711,11.1526),('meinstein',46.4683,11.3282),('Milano_Palermo',46.4896,11.3317),('Milano_Resia',46.4897,11.317),('P_Campiglio',46.4925,11.3714),('petrarca',46.6667,11.1564),('piave_matteotti',46.6642,11.159),('piave-palade',46.6617,11.1602),('ponte resia',46.4813,11.3238),('ponte_rezia',46.6685,11.1531),('proma',46.4903,11.342),('raspberrypi',NULL,NULL),('resiadruso',46.494,11.3143),('Roma_Firenze',46.4923,11.3413),('roma_nord',46.6675,11.1627),('roma_sud',46.6569,11.1678),('rpi01',NULL,NULL),('rpi02',NULL,NULL),('scena-leichter',46.6696,11.1782),('schaffer-winkel',46.6658,11.1701),('siemens',46.4824,11.3305),('sinigo',46.642,11.1776),('stazione',46.6733,11.1501),('terme_est',46.6693,11.1643),('terme_ovest',46.6695,11.1596),('test @tis',NULL,NULL),('thales',NULL,NULL),('TN-Acquaviva',45.9735,11.1133),('TN-Cadino',46.2103,11.1519),('TN-Maccani',46.085,11.1093),('TN-Nord',46.1331,11.082),('TN-Sud',46.0391,11.1215),('Torricelli',46.4781,11.324),('Uscita galleria virgolo',46.4925,11.3566),('Via Rosmini',46.4991,11.3478),('Via_Galilei_Virgolo',NULL,NULL),('Viale Druso',46.4951,11.3389),('Vienna',NULL,NULL),('Vittorio veneto',46.5025,11.3306),('wolf',46.6744,11.1592),('wolf-franziskus',46.678,11.1559),('zuegg-palade',46.6589,11.1459);
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-06 11:43:53
