--
-- Table structure for table `support`
--

CREATE TABLE IF NOT EXISTS `support` (
  `UID` int(3) NOT NULL auto_increment,
  `Name` varchar(128) NOT NULL COMMENT 'Name of support person',
  `Number` varchar(13) NOT NULL,
  `Oncall` int(1) NOT NULL default '0',
  `Switchover` int(1) NOT NULL default '0',
  PRIMARY KEY  (`UID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

