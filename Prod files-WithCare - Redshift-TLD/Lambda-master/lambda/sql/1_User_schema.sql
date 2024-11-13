CREATE USER brightpearlapp WITH PASSWORD 'EE$pd3#7FY*XJrpG';

GRANT CONNECT ON DATABASE vvast TO brightpearlapp;

GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA brightpearl_yeti TO brightpearlapp;
GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA brightpearl_stance TO brightpearlapp;