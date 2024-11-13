drop table if exists brightpearl_yeti.productavailability;
create table brightpearl_yeti.productavailability
(
    productAvailabilityId varchar(25) NOT NULL        
	CONSTRAINT PK_PRODAVA PRIMARY KEY
    ,productId int NOT NULL        
    ,inStock smallint DEFAULT 0
    ,onHand smallint DEFAULT 0
    ,allocated smallint DEFAULT 0
    ,inTransit smallint DEFAULT 0
    ,warehouse smallint DEFAULT 0        
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);


drop table if exists brightpearl_stance.productavailability;
create table brightpearl_stance.productavailability
(
    productAvailabilityId varchar(25) NOT NULL        
	CONSTRAINT PK_PRODAVA PRIMARY KEY
    ,productId int NOT NULL        
    ,inStock smallint DEFAULT 0
    ,onHand smallint DEFAULT 0
    ,allocated smallint DEFAULT 0
    ,inTransit smallint DEFAULT 0
    ,warehouse smallint DEFAULT 0        
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);