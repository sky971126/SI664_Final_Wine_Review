SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS country, province, region, wine, winery,
                    taster, taster_wine, wine_variety;
SET FOREIGN_KEY_CHECKS=1;


CREATE TABLE IF NOT EXISTS winery(
    winery_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    winery_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (winery_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output/winery_trimmed.csv'
INTO TABLE winery
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (winery_name);


CREATE TABLE IF NOT EXISTS country(
    country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    country_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (country_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output/country_trimmed.csv'
INTO TABLE country
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (country_name);

CREATE TABLE IF NOT EXISTS region(
    region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    region_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (region_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output/region_trimmed.csv'
INTO TABLE region
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (region_name);

CREATE TABLE IF NOT EXISTS province(
    province_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    province_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (province_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output/province_trimmed.csv'
INTO TABLE province
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (province_name);

CREATE TABLE IF NOT EXISTS wine_variety(
    wine_variety_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    wine_variety_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (wine_variety_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'E:/2018FA/SI664/SI664_Final_Wine_Review/static/data/output/wine_variety_trimmed.csv'
INTO TABLE wine_variety
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  (wine_variety_name);

