-- Initialize Nour database
CREATE DATABASE IF NOT EXISTS nour;
\c nour;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
