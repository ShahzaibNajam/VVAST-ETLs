CREATE TABLE brightpearl_yeti.errorLog
(
    logId SERIAL NOT NULL
        CONSTRAINT PK_LOG PRIMARY KEY
    ,loginName varchar(50) NOT NULL
    ,moduleName varchar(50) NOT NULL
    ,errorDescription varchar(255)
    ,createdOn timestamptz NOT NULL DEFAULT now()
    ,updatedOn timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE brightpearl_stance.errorLog
(
    logId SERIAL NOT NULL
        CONSTRAINT PK_LOG PRIMARY KEY
    ,loginName varchar(50) NOT NULL        
    ,moduleName varchar(50) NOT NULL
    ,errorDescription varchar(255)
    ,createdOn timestamptz NOT NULL DEFAULT now()
    ,updatedOn timestamptz NOT NULL DEFAULT now()
);