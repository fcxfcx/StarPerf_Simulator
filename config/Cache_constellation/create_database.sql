-- 创建数据库
CREATE DATABASE IF NOT EXISTS constellation_sim;
USE constellation_sim;

-- 创建constellation表
CREATE TABLE IF NOT EXISTS constellation (
  constellation_id INT PRIMARY KEY AUTO_INCREMENT,
  constellation_name VARCHAR(255),
  number_of_shells INT,
  dT INT
);

-- 创建shell表
CREATE TABLE IF NOT EXISTS shell(
  shell_id INT PRIMARY KEY AUTO_INCREMENT,
  shell_name VARCHAR(255),
  altitude INT,
  number_of_satellites INT,
  number_of_orbits INT,
  inclination FLOAT,
  orbit_cycle INT,
  number_of_satellite_per_orbit INT,
  phase_shift INT,
  constellation_id INT,
  FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);

-- 创建orbit表
CREATE TABLE IF NOT EXISTS orbit(
  orbit_id INT PRIMARY KEY AUTO_INCREMENT,
  orbit_name VARCHAR(255),
  orbit_cycle FLOAT,
  shell_id INT,
  FOREIGN KEY (shell_id) REFERENCES shell(shell_id)
);

-- 创建satellite表
CREATE TABLE IF NOT EXISTS satellite(
  satellite_id INT PRIMARY KEY AUTO_INCREMENT,
  longitude_str  TEXT,
  latitude_str  TEXT,
  altitude_str  TEXT,
  nu FLOAT,
  ISL_str TEXT,
  cache_max INT,
  orbit_id INT,
  FOREIGN KEY (orbit_id) REFERENCES orbit(orbit_id)
);

-- 创建video表
CREATE TABLE IF NOT EXISTS video (
  video_id INT PRIMARY KEY AUTO_INCREMENT,
  video_name VARCHAR(255)
);

-- 创建segment表
CREATE TABLE IF NOT EXISTS segment (
  segment_id INT PRIMARY KEY AUTO_INCREMENT,
  size INT,
  index_in_video INT,
  video_id INT,
  FOREIGN KEY (video_id) REFERENCES video(video_id)
);

-- 创建city表
CREATE TABLE IF NOT EXISTS city (
  city_id INT PRIMARY KEY AUTO_INCREMENT,
  city_name VARCHAR(255),
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6)
);

-- 创建user表
CREATE TABLE IF NOT EXISTS user (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255),
  city_id INT,
  FOREIGN KEY (city_id) REFERENCES city(city_id)
);

-- 创建request表
CREATE TABLE IF NOT EXISTS request (
  request_id INT PRIMARY KEY AUTO_INCREMENT,
  city_id INT,
  satellite_id INT,
  segment_id INT,
  timeslot INT,
  FOREIGN KEY (city_id) REFERENCES city(city_id),
  FOREIGN KEY (satellite_id) REFERENCES satellite(satellite_id),
  FOREIGN KEY (segment_id) REFERENCES segment(segment_id)
);

-- 创建缓存表
CREATE TABLE IF NOT EXISTS cache_segment (
  cache_segment_id INT PRIMARY KEY AUTO_INCREMENT,
  satellite_id INT,
  timeslot INT,
  cache_content_str TEXT,
  cache_strategy VARCHAR(255)
  FOREIGN KEY (satellite_id) REFERENCES satellite(satellite_id)
);

CREATE TABLE IF NOT EXISTS city_service (
    city_service_id INT PRIMARY KEY AUTO_INCREMENT,
    city_id INT,
    satellite_id INT,
    timeslot INT,
    FOREIGN KEY (city_id) REFERENCES city(city_id),
    FOREIGN KEY (satellite_id) REFERENCES satellite(satellite_id)
);
