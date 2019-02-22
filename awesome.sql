-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2019-02-22 13:11:29
-- 服务器版本： 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `awesome`
--
CREATE DATABASE IF NOT EXISTS `awesome` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `awesome`;

-- --------------------------------------------------------

--
-- 表的结构 `blogs`
--

CREATE TABLE `blogs` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `name` varchar(50) NOT NULL,
  `summary` varchar(200) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `blogs`
--

INSERT INTO `blogs` (`id`, `user_id`, `user_name`, `user_image`, `name`, `summary`, `content`, `created_at`) VALUES
('001543322387114804c66a802474e839bddb7087a97b3b2000', '0015431338216087ac8f82379ea479083e903709d7b7d7a000', 'xunhan', 'http://www.gravatar.com/avatar/fbfb39203a727ad9e88a1ef224e0e8bc?d=mm&s=120', '?µ???־', '????һ????־ժҪ', '?մ?ˮ??\n##title\n<br/>\n#?????', 1543322387.11433),
('0015481729386590812bc8d5f3d4a3d852eaaa7f685527d000', '0015431338216087ac8f82379ea479083e903709d7b7d7a000', 'xunhan', 'http://www.gravatar.com/avatar/fbfb39203a727ad9e88a1ef224e0e8bc?d=mm&s=120', '新的日志', '摘要', '内容', 1548172938.65823);

-- --------------------------------------------------------

--
-- 表的结构 `comments`
--

CREATE TABLE `comments` (
  `id` varchar(50) NOT NULL,
  `blog_id` varchar(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_image` varchar(500) NOT NULL,
  `content` mediumtext NOT NULL,
  `created_at` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `comments`
--

INSERT INTO `comments` (`id`, `blog_id`, `user_id`, `user_name`, `user_image`, `content`, `created_at`) VALUES
('001543325987219c65b80d6ed5543bd8ff4e86e1a3e4e4c000', '001543322387114804c66a802474e839bddb7087a97b3b2000', '0015431338216087ac8f82379ea479083e903709d7b7d7a000', 'xunhan', 'http://www.gravatar.com/avatar/fbfb39203a727ad9e88a1ef224e0e8bc?d=mm&s=120', '˵??ʲô', 1543325987.21859),
('0015481728576371fc178a509494efdae88fcb33b43db56000', '001543322387114804c66a802474e839bddb7087a97b3b2000', '0015431338216087ac8f82379ea479083e903709d7b7d7a000', 'xunhan', 'http://www.gravatar.com/avatar/fbfb39203a727ad9e88a1ef224e0e8bc?d=mm&s=120', '哈哈', 1548172857.63797);

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `passwd` varchar(50) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(500) NOT NULL,
  `created_at` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`id`, `email`, `passwd`, `admin`, `name`, `image`, `created_at`) VALUES
('0015431338216087ac8f82379ea479083e903709d7b7d7a000', '1638081534@qq.com', 'f77f8015c9aea2acd8f817e3fc00b9901c549dcd', 1, 'xunhan', 'http://www.gravatar.com/avatar/fbfb39203a727ad9e88a1ef224e0e8bc?d=mm&s=120', 1543133821.60887);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blogs`
--
ALTER TABLE `blogs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idx_email` (`email`),
  ADD KEY `idx_created_at` (`created_at`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
