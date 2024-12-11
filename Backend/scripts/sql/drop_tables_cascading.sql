DO $$ DECLARE
    r RECORD;
BEGIN
    -- Loop through all tables in the current schema
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        -- Drop each table
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;