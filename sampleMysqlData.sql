SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


CREATE TABLE IF NOT EXISTS `people` (
  `id` int(11) NOT NULL,
  `name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `zip` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


INSERT INTO `people` (`id`, `name`, `address`, `city`, `state`, `zip`) VALUES

(51, 'Paula Barker', '6528 Prozac Ave', 'San Francisco', 'CA', 92953),
(52, 'John Jacobs', '2957 Ashway Ct', 'Pittsburgh', 'PA', 18320),
(53, 'Dana Brunswick', '4825 Polly Ln', 'Las Vegas', 'NV', 89223),
(54, 'David Turner', '743 Main St', 'Knoxville', 'TN', 37710),
(55, 'Michael Orlando', '1355 Joseph Way', 'Pensacola', 'FL', 31552),
(56, 'Terry Green', '6320 LaSalle St', 'Yazoo', 'MS', 30428),
(57, 'Greg Evans', '2294 South St', 'Indianapolis', 'IN', 46203),
(58, 'Sandy Johnson', '5319 Brentwood Dr', 'Louisville', 'KY', 41350),
(59, 'Charlie Jones', '5382 Miracle Ln', 'New Orleans', 'LA', 73210),
(91, 'Dick Moore', '3209 Simpson Rd', 'New York', 'NY', 10220),
(93, 'Tyrone Jackson', '7725 Georgia St', 'Salt Lake City', 'UT', 82004),


CREATE TABLE IF NOT EXISTS `items` (
  `id` int(11) NOT NULL,
  `name` varchar(65) COLLATE utf8_unicode_ci NOT NULL,
  `cost` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `items` (`id`, `name`, `cost`) VALUES
(1, 'bath towel', 25.1),
(2, 'coffee machine', 210.89),
(3, 'sun glasses', 80.7),
(4, 'candle', 7.5),
(5, 'scarf', 11.9),
(6, 'microwave', 150.29),
(7, 'plasma tv', 645),
(8, 'play station', 256.75),
(9, 'dvd', 26.84),
(10, 'magazine', 3.5);
