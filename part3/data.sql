-- HBnB Initial Data
-- Task 9: Insert initial administrator user and amenities
-- This script populates the database with required initial data

-- Insert Administrator User
-- ID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1 (fixed as per requirements)
-- Password: admin1234 (hashed using bcrypt)
INSERT INTO user (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$G5WdxyNIoOUnxaEEv71JduPdvs.xW/hBwFDf9ywR7An86EhUKoldW',
    TRUE,
    datetime('now'),
    datetime('now')
);

-- Insert Initial Amenities
-- Generate UUIDs for each amenity
-- WiFi
INSERT INTO amenity (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-4789-a012-345678901234',
    'WiFi',
    datetime('now'),
    datetime('now')
);

-- Swimming Pool
INSERT INTO amenity (id, name, created_at, updated_at)
VALUES (
    'b2c3d4e5-f6a7-4890-b123-456789012345',
    'Swimming Pool',
    datetime('now'),
    datetime('now')
);

-- Air Conditioning
INSERT INTO amenity (id, name, created_at, updated_at)
VALUES (
    'c3d4e5f6-a7b8-4901-c234-567890123456',
    'Air Conditioning',
    datetime('now'),
    datetime('now')
);
