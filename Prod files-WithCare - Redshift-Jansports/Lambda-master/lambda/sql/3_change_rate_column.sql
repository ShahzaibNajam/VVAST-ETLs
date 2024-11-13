ALTER TABLE brightpearl_yeti.orders 
    ALTER COLUMN exchangerate TYPE decimal(8,6);

ALTER TABLE brightpearl_stance.orders 
    ALTER COLUMN exchangerate TYPE decimal(8,6);

UPDATE brightpearl_stance.orders
SET updatedon = '1970-01-01 00:00:00';

UPDATE brightpearl_yeti.orders
SET updatedon = '1970-01-01 00:00:00';