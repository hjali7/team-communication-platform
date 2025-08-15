-- Database initialization script for Team Communication Platform
-- This script runs when the PostgreSQL container starts for the first time

-- Create messages table for Flask-SQLAlchemy
CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    text VARCHAR(500) NOT NULL
);

-- Insert sample data
INSERT INTO message (username, text) VALUES 
    ('admin', 'Welcome to the team!'),
    ('user1', 'Hello everyone!')
ON CONFLICT (id) DO NOTHING;

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_message_username ON message(username);
