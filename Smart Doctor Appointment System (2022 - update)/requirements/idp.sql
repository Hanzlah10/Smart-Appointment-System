-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 28, 2021 at 12:09 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `idp`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments_information`
--

CREATE TABLE `appointments_information` (
  `pid` int(11) NOT NULL,
  `appointed_datetime` date NOT NULL DEFAULT current_timestamp(),
  `doctor_email` varchar(200) NOT NULL,
  `patient_email` varchar(200) NOT NULL,
  `done` int(2) NOT NULL DEFAULT 0,
  `appointment_time` varchar(50) DEFAULT current_timestamp(),
  `someone_patient_name` varchar(50) DEFAULT NULL,
  `someone_patient_age` int(50) DEFAULT NULL,
  `someone_patient_contact_number` int(50) DEFAULT NULL,
  `someone_patient_gender` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `appointments_information`
--

INSERT INTO `appointments_information` (`pid`, `appointed_datetime`, `doctor_email`, `patient_email`, `done`, `appointment_time`, `someone_patient_name`, `someone_patient_age`, `someone_patient_contact_number`, `someone_patient_gender`) VALUES
(56, '2021-01-18', 'rohanprajapati7860@gmail.com', 'rohanprajapati7860@gmail.com', 1, '07:34 AM - 08:34 AM', ' rohan', 16, 1234567890, 'Male'),
(57, '2021-01-18', 'rohanprajapati7860@gmail.com', 'rohanprajapati7860@gmail.com', 1, '07:34 AM - 08:34 AM', 'irfan', 23, 1234567897, 'Male'),
(58, '2021-01-19', 'rohanprajapati7860@gmail.com', 'rohanprajapati7860@gmail.com', 1, '06:00 PM - 07:00 PM', ' rohan', 16, 1234567890, 'Male');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_information`
--

CREATE TABLE `doctor_information` (
  `doctor_registered` datetime NOT NULL DEFAULT current_timestamp(),
  `doctor_id` int(11) NOT NULL,
  `doctor_name` text NOT NULL,
  `doctor_username` varchar(100) NOT NULL,
  `doctor_password` varchar(250) NOT NULL,
  `doctor_phone_number` varchar(12) NOT NULL DEFAULT '0',
  `doctor_email` varchar(100) NOT NULL DEFAULT '0',
  `qualification` varchar(50) DEFAULT 'MBBS',
  `address` varchar(200) DEFAULT 'address here',
  `profile_image` varchar(200) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 1,
  `start_time` varchar(50) DEFAULT NULL,
  `start_time_1` varchar(50) DEFAULT NULL,
  `end_time_1` varchar(50) DEFAULT NULL,
  `end_time` varchar(50) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT 'Not Available',
  `diagnose` int(50) DEFAULT 0,
  `token` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `doctor_information`
--

INSERT INTO `doctor_information` (`doctor_registered`, `doctor_id`, `doctor_name`, `doctor_username`, `doctor_password`, `doctor_phone_number`, `doctor_email`, `qualification`, `address`, `profile_image`, `status`, `start_time`, `start_time_1`, `end_time_1`, `end_time`, `specialization`, `diagnose`, `token`) VALUES
('2021-01-18 16:31:12', 43, 'Rohan', '', 'rp', '1234567890', 'rohanprajapati7860@gmail.com', 'MBBS', 'mumbra', '/static/Images/1610967773960Accenture-Jim-Wilson-724x543.png', 1, '07:00 AM', '06:00 PM', '10:00 PM', '01:00 PM', 'DTE ', 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `patient_information`
--

CREATE TABLE `patient_information` (
  `p_id` int(11) NOT NULL,
  `patient_registered` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `patient_name` text DEFAULT NULL,
  `patient_password` varchar(100) NOT NULL,
  `phone` bigint(12) DEFAULT 0,
  `email` varchar(100) NOT NULL DEFAULT '0',
  `patient_profile_image` varchar(200) DEFAULT NULL,
  `patient_age` int(100) DEFAULT 15,
  `patient_gender` varchar(50) DEFAULT 'Male',
  `token` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patient_information`
--

INSERT INTO `patient_information` (`p_id`, `patient_registered`, `patient_name`, `patient_password`, `phone`, `email`, `patient_profile_image`, `patient_age`, `patient_gender`, `token`) VALUES
(13, '2021-01-18 16:33:22.793066', ' rohan', 'rp', 1234567890, 'rohanprajapati7860@gmail.com', NULL, 16, 'Male', 'empty');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments_information`
--
ALTER TABLE `appointments_information`
  ADD PRIMARY KEY (`pid`);

--
-- Indexes for table `doctor_information`
--
ALTER TABLE `doctor_information`
  ADD PRIMARY KEY (`doctor_id`);

--
-- Indexes for table `patient_information`
--
ALTER TABLE `patient_information`
  ADD PRIMARY KEY (`p_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments_information`
--
ALTER TABLE `appointments_information`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `doctor_information`
--
ALTER TABLE `doctor_information`
  MODIFY `doctor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `patient_information`
--
ALTER TABLE `patient_information`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
