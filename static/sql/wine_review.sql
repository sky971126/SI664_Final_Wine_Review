SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS country, province, region, wine, winery,
                    taster, taster_wine, wine_variety, 
                    taster_temp, wine_temp, province_temp, region_temp, taster_wine_temp;
SET FOREIGN_KEY_CHECKS=1;


CREATE TABLE IF NOT EXISTS winery(
    winery_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    winery_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (winery_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/winery_trimmed_short.csv'
INTO TABLE winery
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (winery_name);


CREATE TABLE IF NOT EXISTS country(
    country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    country_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (country_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/country_trimmed_short.csv'
INTO TABLE country
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (country_name);


CREATE TEMPORARY TABLE IF NOT EXISTS province_temp(
    province_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    province_name VARCHAR(60) NOT NULL UNIQUE,
    country_name VARCHAR(60) NOT NULL,
    PRIMARY KEY (province_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/province_trimmed_short.csv'
INTO TABLE province_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (province_name,country_name);

CREATE TABLE IF NOT EXISTS province(
    province_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    province_name VARCHAR(60) NOT NULL UNIQUE,
    country_id INTEGER NOT NULL,
    PRIMARY KEY (province_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


INSERT IGNORE INTO province
(province_name,country_id)
SELECT pt.province_name as province_name, co.country_id as country_id
FROM province_temp pt
LEFT JOIN country co
ON pt.country_name = co.country_name
WHERE pt.province_name NOT LIKE '';



CREATE TEMPORARY TABLE IF NOT EXISTS region_temp(
    region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    region_name VARCHAR(60) NOT NULL UNIQUE,
    province_name VARCHAR(60) NOT NULL,
    PRIMARY KEY (region_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/region_trimmed_short.csv'
INTO TABLE region_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (region_name,province_name);

CREATE TABLE IF NOT EXISTS region(
    region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    region_name VARCHAR(60) NOT NULL UNIQUE,
    province_id INTEGER NOT NULL,
    PRIMARY KEY (region_id),
    FOREIGN KEY (province_id) REFERENCES province(province_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


INSERT IGNORE INTO region
(region_name,province_id)
SELECT rt.region_name as region_name, pr.province_id as province_id
FROM region_temp rt
LEFT JOIN province pr
ON rt.province_name = pr.province_name
WHERE rt.region_name NOT LIKE '';


CREATE TABLE IF NOT EXISTS wine_variety(
    wine_variety_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    wine_variety_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (wine_variety_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/wine_variety_trimmed_short.csv'
INTO TABLE wine_variety
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (wine_variety_name);

CREATE TEMPORARY TABLE IF NOT EXISTS taster_temp(
    taster_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    taster_name VARCHAR(60) NOT NULL UNIQUE,
    taster_twitter VARCHAR(60) NULL,
    PRIMARY KEY (taster_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/taster_trimmed_short.csv'
INTO TABLE taster_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (taster_name,taster_twitter)

  SET taster_name = IF(taster_name = '', NULL, TRIM(taster_name)),
  taster_twitter = IF(taster_twitter = '', NULL, TRIM(taster_twitter));

CREATE TABLE IF NOT EXISTS taster(
    taster_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    taster_name VARCHAR(60) NOT NULL UNIQUE,
    taster_twitter VARCHAR(60) NULL,
    PRIMARY KEY (taster_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO taster
(taster_name,taster_twitter)
SELECT tt.taster_name as taster_name, tt.taster_twitter as taster_twitter
FROM taster_temp tt
WHERE tt.taster_name NOT LIKE '';








CREATE TEMPORARY TABLE wine_temp (
  wine_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  wine_title VARCHAR(100) NOT NULL UNIQUE,
  wine_variety_name VARCHAR(60) NOT NULL,
  winery_name VARCHAR(60) NOT NULL,
  region_name VARCHAR(60) NULL,
  province_name VARCHAR(60) NOT NULL,
  country_name VARCHAR(60) NOT NULL,
  PRIMARY KEY (wine_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/wine_trimmed_short.csv'
INTO TABLE wine_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (wine_title,wine_variety_name,winery_name,region_name,province_name,country_name)

  SET region_name = IF(TRIM(region_name) = '', NULL, TRIM(region_name));



CREATE TABLE if NOT EXISTS wine(
  wine_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  wine_title VARCHAR(100) NOT NULL UNIQUE,
  wine_variety_id INTEGER NOT NULL,
  winery_id INTEGER NOT NULL,
  region_id INTEGER NULL,
  province_id INTEGER NULL,
  country_id INTEGER NULL,
  PRIMARY KEY (wine_id),
  FOREIGN KEY (wine_variety_id) REFERENCES wine_variety(wine_variety_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (winery_id) REFERENCES winery(winery_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (region_id) REFERENCES region(region_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (province_id) REFERENCES province(province_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (country_id) REFERENCES country(country_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO wine
(
  wine_title,
  wine_variety_id,
  winery_id,
  region_id,
  province_id,
  country_id
)
SELECT wt.wine_title, wv.wine_variety_id, wi.winery_id, re.region_id, pr.province_id, co.country_id
FROM wine_temp wt
      LEFT JOIN wine_variety wv
             ON TRIM(wt.wine_variety_name) = TRIM(wv.wine_variety_name)
      LEFT JOIN winery wi
             ON TRIM(wt.winery_name) = TRIM(wi.winery_name)
      LEFT JOIN region re
             ON TRIM(wt.region_name) = TRIM(re.region_name)
      LEFT JOIN province pr
             ON TRIM(wt.province_name) = TRIM(pr.province_name)
      LEFT JOIN country co
             ON TRIM(wt.country_name) = TRIM(co.country_name)
ORDER BY wt.wine_title;


CREATE TEMPORARY TABLE taster_wine_temp(
  taster_wine_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  taster_name VARCHAR(60) NULL,
  wine_title VARCHAR(100) NOT NULL,
  description VARCHAR(500) NOT NULL,
  rating INTEGER NOT NULL,
  PRIMARY KEY (taster_wine_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output_short/manytomany_trimmed_short.csv'
INTO TABLE taster_wine_temp
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (taster_name,wine_title,description,rating)

  SET taster_name = IF(TRIM(taster_name) = '', NULL, TRIM(taster_name));


CREATE TABLE if NOT EXISTS taster_wine(
  taster_wine_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  taster_id INTEGER NULL,
  wine_id INTEGER NOT NULL,
  description VARCHAR(500) NOT NULL,
  rating INTEGER NOT NULL,
  PRIMARY KEY (taster_wine_id),
  FOREIGN KEY (taster_id) REFERENCES taster(taster_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (wine_id) REFERENCES wine(wine_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO taster_wine
(
  taster_id,
  wine_id,
  description,
  rating
)
SELECT ta.taster_id, w.wine_id, twt.description, twt.rating
FROM taster_wine_temp twt
      LEFT JOIN wine w
             ON TRIM(twt.wine_title) = TRIM(w.wine_title)
      LEFT JOIN taster ta
             ON TRIM(twt.taster_name) = TRIM(ta.taster_name)
ORDER BY w.wine_title;
