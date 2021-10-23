CREATE TABLE `region`
(
    `id`   int(11) NOT NULL ,
    `name` varchar(45) DEFAULT NULL,
    PRIMARY KEY (`id`)
);


CREATE TABLE `category`
(
    `id`   int(11) NOT NULL ,
    `name` varchar(45) DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `user`
(
    `id`         int(11) NOT NULL,
    `username`   varchar(45) DEFAULT NULL,
    `first_name` varchar(45) DEFAULT NULL,
    `last_name`  varchar(45) DEFAULT NULL,
    `email`      varchar(45) DEFAULT NULL,
    `password`   varchar(45) DEFAULT NULL,
    `region_id`  int(11)     DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
);

CREATE TABLE `Advertisement`
(
    `id`                 int(11) NOT NULL ,
    `text`               varchar(45)           DEFAULT NULL,
    `date_of_publishing` datetime              DEFAULT NULL,
    `status`             enum ('open','close') DEFAULT NULL,
    `region_id`          int(11)               DEFAULT NULL,
    `category_id`        int(11)               DEFAULT NULL,
    `user_id`            int(11)               DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ,
    FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
    FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
);
