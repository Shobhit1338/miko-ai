CREATE DATABASE IF NOT EXISTS db123;

USE db123;

CREATE TABLE IF NOT EXISTS program_execution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program TEXT,
    status VARCHAR(10)
);
