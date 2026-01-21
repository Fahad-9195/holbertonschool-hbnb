-- HBnB Test Queries
-- Task 9: Test CRUD operations to verify schema and data integrity

-- ============================================
-- SELECT Operations (Read)
-- ============================================

-- 1. Verify admin user was created correctly
SELECT id, first_name, last_name, email, is_admin, created_at
FROM user
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- 2. Verify admin user has is_admin = TRUE
SELECT id, email, is_admin
FROM user
WHERE is_admin = TRUE;

-- 3. List all amenities
SELECT id, name, created_at
FROM amenity
ORDER BY name;

-- 4. Verify all three initial amenities exist
SELECT COUNT(*) as amenity_count
FROM amenity
WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning');

-- 5. Check password is stored (should be hashed, not plain text)
SELECT id, email, 
       CASE 
           WHEN password LIKE '$2b$%' THEN 'Hashed (bcrypt)'
           ELSE 'Plain text (ERROR!)'
       END as password_status
FROM user
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- ============================================
-- INSERT Operations (Create)
-- ============================================

-- 6. Insert a test user
INSERT INTO user (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'test-user-0000-0000-0000-000000000001',
    'Test',
    'User',
    'test@example.com',
    '$2b$12$G5WdxyNIoOUnxaEEv71JduPdvs.xW/hBwFDf9ywR7An86EhUKoldW',
    FALSE,
    datetime('now'),
    datetime('now')
);

-- 7. Insert a test place (owned by test user)
INSERT INTO place (id, name, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'test-place-0000-0000-0000-000000000001',
    'Test Place',
    'A test place for verification',
    100.00,
    40.7128,
    -74.0060,
    'test-user-0000-0000-0000-000000000001',
    datetime('now'),
    datetime('now')
);

-- 8. Insert a test review
INSERT INTO review (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    'test-review-0000-0000-0000-000000000001',
    'This is a test review',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',  -- Admin user
    'test-place-0000-0000-0000-000000000001',
    datetime('now'),
    datetime('now')
);

-- 9. Link amenity to place (Many-to-Many)
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'test-place-0000-0000-0000-000000000001',
    'a1b2c3d4-e5f6-4789-a012-345678901234'  -- WiFi
);

-- ============================================
-- UPDATE Operations
-- ============================================

-- 10. Update test user's first name
UPDATE user
SET first_name = 'Updated', updated_at = datetime('now')
WHERE id = 'test-user-0000-0000-0000-000000000001';

-- 11. Update test place price
UPDATE place
SET price = 150.00, updated_at = datetime('now')
WHERE id = 'test-place-0000-0000-0000-000000000001';

-- 12. Update test review rating
UPDATE review
SET rating = 4, updated_at = datetime('now')
WHERE id = 'test-review-0000-0000-0000-000000000001';

-- ============================================
-- DELETE Operations
-- ============================================

-- 13. Delete test review
DELETE FROM review
WHERE id = 'test-review-0000-0000-0000-000000000001';

-- 14. Delete test place (should cascade delete place_amenity entries)
DELETE FROM place
WHERE id = 'test-place-0000-0000-0000-000000000001';

-- 15. Delete test user
DELETE FROM user
WHERE id = 'test-user-0000-0000-0000-000000000001';

-- ============================================
-- Relationship Verification Queries
-- ============================================

-- 16. Verify foreign key constraints work (should show admin user's places)
SELECT u.email, p.name, p.price
FROM user u
LEFT JOIN place p ON u.id = p.owner_id
WHERE u.id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- 17. Verify unique constraint on (user_id, place_id) in review
-- This should fail if we try to insert duplicate:
-- INSERT INTO review (id, text, rating, user_id, place_id, created_at, updated_at)
-- VALUES ('duplicate-test', 'Duplicate', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'test-place-0000-0000-0000-000000000001', datetime('now'), datetime('now'));

-- 18. Verify many-to-many relationship structure
SELECT p.name as place_name, a.name as amenity_name
FROM place p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenity a ON pa.amenity_id = a.id;

-- ============================================
-- Final Verification
-- ============================================

-- 19. Count all records
SELECT 
    (SELECT COUNT(*) FROM user) as user_count,
    (SELECT COUNT(*) FROM amenity) as amenity_count,
    (SELECT COUNT(*) FROM place) as place_count,
    (SELECT COUNT(*) FROM review) as review_count,
    (SELECT COUNT(*) FROM place_amenity) as place_amenity_count;

-- 20. Verify admin user still exists and is correct
SELECT 
    id,
    first_name || ' ' || last_name as full_name,
    email,
    is_admin,
    created_at
FROM user
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
