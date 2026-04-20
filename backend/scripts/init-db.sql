-- SkyMechanics PostgreSQL Schema Initialization
-- This script creates all tables and initial data for the auth-service

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    password_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refresh tokens for session management
CREATE TABLE IF NOT EXISTS refresh_tokens (
    token_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    token VARCHAR(512) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Organizations table (for multi-tenancy)
CREATE TABLE IF NOT EXISTS organizations (
    org_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User-organization assignments (many-to-many)
CREATE TABLE IF NOT EXISTS user_organizations (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    org_id INTEGER REFERENCES organizations(org_id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, org_id)
);

-- Profiles table (role-specific user data)
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    profile_type VARCHAR(50) NOT NULL, -- 'mechanic', 'customer', 'admin'
    external_id VARCHAR(255), -- Foreign key to FalkorDB node_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log for user actions
CREATE TABLE IF NOT EXISTS audit_log (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    org_id INTEGER REFERENCES organizations(org_id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_organizations_user ON user_organizations(user_id);
CREATE INDEX IF NOT EXISTS idx_user_organizations_org ON user_organizations(org_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_org ON audit_log(org_id);

-- Seed data: Default organization
INSERT INTO organizations (name, domain, is_active)
VALUES ('SkyMechanics', 'skymechanics.dev', true)
ON CONFLICT (domain) DO NOTHING;

-- Seed data: Admin user (owner role)
INSERT INTO users (email, first_name, last_name, password_hash, role, is_active)
VALUES (
    'admin@skymechanics.dev',
    'Admin',
    'User',
    'admin123',  -- Simplified hash for testing
    'owner',
    true
)
ON CONFLICT (email) DO NOTHING;

-- Link admin to org
INSERT INTO user_organizations (user_id, org_id, role)
SELECT u.user_id, o.org_id, 'admin'
FROM users u, organizations o
WHERE u.email = 'admin@skymechanics.dev' AND o.domain = 'skymechanics.dev'
ON CONFLICT (user_id, org_id) DO NOTHING;

-- Seed data: Test mechanic user
INSERT INTO users (email, first_name, last_name, password_hash, role, phone, is_active)
VALUES (
    'mechanic@skymechanics.dev',
    'Test',
    'Mechanic',
    'mechanic123',
    'member',
    '+1-555-1001',
    true
)
ON CONFLICT (email) DO NOTHING;

-- Link mechanic to org
INSERT INTO user_organizations (user_id, org_id, role)
SELECT u.user_id, o.org_id, 'member'
FROM users u, organizations o
WHERE u.email = 'mechanic@skymechanics.dev' AND o.domain = 'skymechanics.dev'
ON CONFLICT (user_id, org_id) DO NOTHING;

-- Seed data: Test customer user
INSERT INTO users (email, first_name, last_name, password_hash, role, phone, is_active)
VALUES (
    'customer@skymechanics.dev',
    'Test',
    'Customer',
    'customer123',
    'member',
    '+1-555-2001',
    true
)
ON CONFLICT (email) DO NOTHING;

-- Link customer to org
INSERT INTO user_organizations (user_id, org_id, role)
SELECT u.user_id, o.org_id, 'member'
FROM users u, organizations o
WHERE u.email = 'customer@skymechanics.dev' AND o.domain = 'skymechanics.dev'
ON CONFLICT (user_id, org_id) DO NOTHING;

-- Create profiles for test users
INSERT INTO user_profiles (user_id, profile_type, external_id)
SELECT user_id, 'mechanic', NULL
FROM users WHERE email = 'mechanic@skymechanics.dev'
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO user_profiles (user_id, profile_type, external_id)
SELECT user_id, 'customer', NULL
FROM users WHERE email = 'customer@skymechanics.dev'
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO user_profiles (user_id, profile_type, external_id)
SELECT user_id, 'admin', NULL
FROM users WHERE email = 'admin@skymechanics.dev'
ON CONFLICT (user_id) DO NOTHING;

-- Add admin profile for admin user
UPDATE user_profiles
SET profile_type = 'admin'
WHERE user_id = (SELECT user_id FROM users WHERE email = 'admin@skymechanics.dev');
