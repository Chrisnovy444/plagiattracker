-- ============================================
-- PLAGIATTRACKER - Database Initialization
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types (enums)
DO $$ BEGIN
    CREATE TYPE plan_type AS ENUM ('trial', 'student', 'teacher', 'researcher', 'institution');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE code_status AS ENUM ('active', 'used', 'expired', 'revoked');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE document_status AS ENUM ('uploaded', 'processing', 'completed', 'failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ============================================
-- Users Table
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),

    -- Subscription
    plan_type plan_type DEFAULT 'trial',
    analyses_remaining INTEGER DEFAULT 3,
    analyses_limit INTEGER DEFAULT 3,
    subscription_expires_at TIMESTAMP,

    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,

    -- Settings (JSON)
    settings JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_plan_type ON users(plan_type);

-- ============================================
-- Activation Codes Table
-- ============================================
CREATE TABLE IF NOT EXISTS activation_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) UNIQUE NOT NULL,

    -- Plan details
    plan_type plan_type NOT NULL,
    analyses_limit INTEGER NOT NULL,
    validity_days INTEGER NOT NULL,

    -- Status
    status code_status DEFAULT 'active',

    -- Usage
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    activated_at TIMESTAMP,
    expires_at TIMESTAMP,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    notes TEXT
);

CREATE INDEX idx_codes_code ON activation_codes(code);
CREATE INDEX idx_codes_status ON activation_codes(status);
CREATE INDEX idx_codes_plan_type ON activation_codes(plan_type);
CREATE INDEX idx_codes_status_plan ON activation_codes(status, plan_type);

-- ============================================
-- Documents Table
-- ============================================
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- File info
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(50),
    file_path VARCHAR(500),

    -- Processing
    status document_status DEFAULT 'uploaded',
    extracted_text TEXT,
    word_count INTEGER,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    error_message TEXT,

    -- GDPR - auto-delete
    delete_at TIMESTAMP
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_user_created ON documents(user_id, created_at DESC);
CREATE INDEX idx_documents_delete_at ON documents(delete_at) WHERE delete_at IS NOT NULL;

-- ============================================
-- Reports Table
-- ============================================
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID UNIQUE NOT NULL REFERENCES documents(id) ON DELETE CASCADE,

    -- Plagiarism
    plagiarism_score FLOAT DEFAULT 0.0,
    plagiarism_level VARCHAR(20),
    sources_found JSONB DEFAULT '[]'::jsonb,

    -- AI detection
    ai_score FLOAT DEFAULT 0.0,
    ai_level VARCHAR(20),
    ai_details JSONB DEFAULT '{}'::jsonb,

    -- Findings
    plagiarism_passages JSONB DEFAULT '[]'::jsonb,
    ai_passages JSONB DEFAULT '[]'::jsonb,

    -- Corrections
    corrections_applied BOOLEAN DEFAULT FALSE,
    corrections JSONB DEFAULT '{}'::jsonb,

    -- PDF
    pdf_path VARCHAR(500),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time FLOAT,
    cache_key VARCHAR(64)
);

CREATE INDEX idx_reports_document_id ON reports(document_id);
CREATE INDEX idx_reports_cache_key ON reports(cache_key);

-- ============================================
-- Audit Logs Table
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,

    -- Action
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,

    -- Request
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),

    -- Result
    status VARCHAR(20),
    error_message TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_user_action ON audit_logs(user_id, action);

-- ============================================
-- Triggers for updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Function to generate activation codes
-- ============================================
CREATE OR REPLACE FUNCTION generate_activation_code(
    p_plan_type plan_type,
    p_count INTEGER DEFAULT 1,
    p_created_by VARCHAR DEFAULT 'admin'
)
RETURNS TABLE(code VARCHAR) AS $$
DECLARE
    v_code VARCHAR;
    v_prefix VARCHAR;
    v_analyses_limit INTEGER;
    v_validity_days INTEGER;
BEGIN
    -- Determine prefix and limits based on plan
    CASE p_plan_type
        WHEN 'trial' THEN
            v_prefix := 'TRIAL';
            v_analyses_limit := 3;
            v_validity_days := 7;
        WHEN 'student' THEN
            v_prefix := 'STU';
            v_analyses_limit := 50;
            v_validity_days := 30;
        WHEN 'teacher' THEN
            v_prefix := 'TCH';
            v_analyses_limit := 200;
            v_validity_days := 30;
        WHEN 'researcher' THEN
            v_prefix := 'RES';
            v_analyses_limit := 500;
            v_validity_days := 30;
        WHEN 'institution' THEN
            v_prefix := 'INS';
            v_analyses_limit := -1;  -- Unlimited
            v_validity_days := 365;
    END CASE;

    -- Generate codes
    FOR i IN 1..p_count LOOP
        v_code := v_prefix || '-' || upper(substring(md5(random()::text) from 1 for 5)) || '-' || upper(substring(md5(random()::text) from 1 for 5));

        INSERT INTO activation_codes (
            code,
            plan_type,
            analyses_limit,
            validity_days,
            created_by
        ) VALUES (
            v_code,
            p_plan_type,
            v_analyses_limit,
            v_validity_days,
            p_created_by
        );

        RETURN QUERY SELECT v_code;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Insert sample activation codes for testing
-- ============================================
-- Generate 5 trial codes
SELECT generate_activation_code('trial', 5, 'system');

-- Generate 3 student codes
SELECT generate_activation_code('student', 3, 'system');

-- Generate 2 teacher codes
SELECT generate_activation_code('teacher', 2, 'system');

-- Generate 1 researcher code
SELECT generate_activation_code('researcher', 1, 'system');

-- ============================================
-- View: Active codes summary
-- ============================================
CREATE OR REPLACE VIEW active_codes_summary AS
SELECT
    plan_type,
    COUNT(*) as total_codes,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_codes,
    SUM(CASE WHEN status = 'used' THEN 1 ELSE 0 END) as used_codes,
    SUM(CASE WHEN status = 'expired' THEN 1 ELSE 0 END) as expired_codes
FROM activation_codes
GROUP BY plan_type;

-- ============================================
-- View: User statistics
-- ============================================
CREATE OR REPLACE VIEW user_statistics AS
SELECT
    u.id,
    u.email,
    u.full_name,
    u.plan_type,
    u.analyses_remaining,
    u.analyses_limit,
    u.subscription_expires_at,
    COUNT(DISTINCT d.id) as total_documents,
    COUNT(DISTINCT r.id) as total_reports,
    MAX(d.created_at) as last_document_uploaded
FROM users u
LEFT JOIN documents d ON u.id = d.user_id
LEFT JOIN reports r ON d.id = r.document_id
GROUP BY u.id;

-- ============================================
-- Cleanup function (GDPR compliance)
-- ============================================
CREATE OR REPLACE FUNCTION cleanup_old_documents()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Delete documents older than delete_at
    DELETE FROM documents
    WHERE delete_at IS NOT NULL AND delete_at < CURRENT_TIMESTAMP;

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-old-documents', '0 3 * * *', 'SELECT cleanup_old_documents()');

-- ============================================
-- Success message
-- ============================================
DO $$
BEGIN
    RAISE NOTICE '✅ PLAGIATTRACKER database initialized successfully!';
    RAISE NOTICE '📊 Sample activation codes generated';
    RAISE NOTICE '🔍 Run: SELECT * FROM activation_codes WHERE status = ''active'';';
END $$;
