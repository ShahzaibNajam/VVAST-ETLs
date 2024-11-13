alter table brightpearl_yeti.orders 
add column channelId smallint;

alter table brightpearl_outofstep.orders 
add column channelId smallint;

alter table brightpearl_jansports.orders 
add column channelId smallint;

alter table brightpearl_stance.orders 
add column channelId smallint;

-- after adding columns force orders reprocess
update brightpearl_stance.orders 
set updatedon = '1970-01-01 00:00:00';

update brightpearl_jansports.orders 
set updatedon = '1970-01-01 00:00:00';

update brightpearl_yeti.orders 
set updatedon = '1970-01-01 00:00:00';

update brightpearl_outofstep.orders 
set updatedon = '1970-01-01 00:00:00';