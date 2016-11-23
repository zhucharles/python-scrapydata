CREATE DATABASE macbookInfo DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;



CREATE TABLE `MacbookjdInfo` (  
`No` INT(11) NOT NULL AUTO_INCREMENT,  
`id` VARCHAR(50),  
`title` VARCHAR(200),  
`img_url` VARCHAR(200),  
`price` VARCHAR(100),  
`description` VARCHAR(200),  
`comments` VARCHAR(500),  
PRIMARY KEY (`No`)  
)
COLLATE='utf8_general_ci'  
ENGINE=MyISAM  
AUTO_INCREMENT=5;


CREATE DATABASE weiboInfo DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE `TweetsInfo` (  
`No` INT(11) NOT NULL AUTO_INCREMENT,  
`id` VARCHAR(50),  
`Content` VARCHAR(500),  
`Time_Location` VARCHAR(100),  
`Pic_Url` VARCHAR(100),  
`Num_Comment` VARCHAR(20),  
`Num_Like` VARCHAR(20),  
`NUm_Transfer` VARCHAR(20),
PRIMARY KEY (`No`)  
)
COLLATE='utf8_general_ci'  
ENGINE=MyISAM  
AUTO_INCREMENT=5;
