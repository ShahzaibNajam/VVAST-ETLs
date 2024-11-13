drop table if exists brightpearl_outofstep.priceList;
create table brightpearl_outofstep.priceList
(
    priceListId smallint NOT NULL
        CONSTRAINT PK_PRICE PRIMARY KEY
    ,priceListName varchar(100) NULL
    ,code varchar(50) NOT NULL
    ,currencyCode varchar(3)
    ,priceListTypeCode varchar(4) NOT NULL
    ,gross bool NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.productavailability;
create table brightpearl_outofstep.productavailability
(
    productAvailabilityId SERIAL NOT NULL
    ,productId int NOT NULL
        CONSTRAINT PK_PRODAVA PRIMARY KEY
    ,inStock smallint DEFAULT 0
    ,onHand smallint DEFAULT 0
    ,allocated smallint DEFAULT 0
    ,inTransit smallint DEFAULT 0    
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.productPrice;
create table brightpearl_outofstep.productPrice
(
    dbProductPriceValue varchar(10) NOT NULL
    ,fkproductId int NOT NULL
    ,fkpriceListId smallint REFERENCES brightpearl_outofstep.priceList (priceListId)
    ,quantityPriceNumber varchar(10) NOT NULL
    ,quantityPriceValue decimal (10,2) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.brand;
create table brightpearl_outofstep.brand
(
    brandId smallint NOT NULL
        CONSTRAINT PK_BRAND PRIMARY KEY
    ,brandName varchar(100) NULL
    ,brandDescription varchar(255) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.productsOptionValue;
create table brightpearl_outofstep.productsOptionValue
(
    optionValueId smallint NOT NULL
        CONSTRAINT PK_PRODOP PRIMARY KEY
    ,optionValueName varchar(255) NULL
    ,optionId smallint
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    );


drop table if exists brightpearl_outofstep.brightpearlCategory;
create table brightpearl_outofstep.brightpearlCategory
(
    brightpearlCategoryId smallint NOT NULL
        CONSTRAINT PK_BPCAT PRIMARY KEY
    ,brightpearlCategoryName varchar(100) NULL
    ,parentId smallint NULL
    ,active bool NOT NULL
    ,description varchar(255) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.productType;
create table brightpearl_outofstep.productType
(
    productTypeId smallint NOT NULL
        CONSTRAINT PK_PRODTYP PRIMARY KEY
    ,productTypeName varchar(100) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.season;
create table brightpearl_outofstep.season
(
    seasonId smallint NOT NULL
        CONSTRAINT PK_SEASON PRIMARY KEY
    ,seasonName varchar(100) NOT NULL
    ,seasonDescription varchar(255) NULL
    ,dateFrom date NOT NULL
    ,dateTo date NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_outofstep.products;
create table brightpearl_outofstep.products
(
    dbproductIdOptionValue varchar(20) NOT NULL         
    ,productId int NOT NULL
    ,fkBrandId int NOT NULL REFERENCES brightpearl_outofstep.brand (brandId)
    ,fkOptionValueId smallint REFERENCES brightpearl_outofstep.productsOptionValue (optionValueId)
    ,optionname varchar(50) NOT NULL
    ,fkProductTypeId smallint
    ,fkBrightpearlCategoryId smallint REFERENCES brightpearl_outofstep.brightpearlCategory (brightpearlCategoryId)
    ,fkSeasonId smallint
    ,sku varchar(100)
    ,barcode varchar(255)
    ,productGroupId smallint
    ,featured bool
    ,dimensionsLength varchar(20)
    ,dimensionsHeight varchar(20)
    ,dimensionsWidth varchar(20)
    ,dimensionsVolume varchar(20)
    ,salesChannelName varchar(255)
    ,productName varchar(255)
    ,productCondition varchar(20)
    ,status varchar(50)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    ,PRIMARY KEY(productId, fkOptionValueId)
    ,CONSTRAINT U_PROD_T UNIQUE (dbproductIdOptionValue)
);

drop table if exists brightpearl_outofstep.orders;
create table brightpearl_outofstep.orders
(
    orderId int NOT NULL
        CONSTRAINT PK_ORD PRIMARY KEY
    ,parentOrderdId int NULL
    ,orderTypeCode varchar(20)
    ,orderStatus varchar(100)
    ,reference varchar(255)
    ,fkcontactId int
    ,country varchar(100)
    ,tax varchar(100)
    ,acknowledged bool
    ,orderPaymentStatus varchar(20) NOT NULL
    ,stockStatusCode varchar(3) NOT NULL
    ,allocationStatusCode varchar(3) NOT NULL
    ,shippingStatusCode varchar(3) NOT NULL
    ,shippingMethodId smallint
    ,accountingCurrencyCode varchar(3)
    ,exchangeRate decimal (6,2)
    ,placedOn timestamptz NOT NULL
    ,closedOn timestamptz NOT NULL
    ,deliveryDate timestamptz
    ,taxdate timestamptz
    ,createdById smallint
    ,totalValueNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,taxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,baseTaxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseTotal decimal (10,2) NOT NULL DEFAULT 0.00
    ,total decimal (10,2) NOT NULL DEFAULT 0.00
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false

);
drop table if exists brightpearl_outofstep.orderItems;
create table brightpearl_outofstep.orderItems
(
    dbOrderItemOptionId varchar(50) NOT NULL
        CONSTRAINT PK_ORDITEM PRIMARY KEY
    ,orderItemId int NOT NULL
    ,fkOrderId int REFERENCES brightpearl_outofstep.orders (orderId)
    ,fkproductId int NOT NULL
    ,quantity decimal(5,1)
    ,itemCost decimal(10,2)
    ,taxCode varchar(10)
    ,taxRate decimal(8,2)
    ,itemNet decimal(10,2)
    ,itemTax decimal(8,2)
    ,productOptionName varchar(50)
    ,productOptionValue varchar(50)
    ,currencyCode varchar(3)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false    
);

drop table if exists brightpearl_stance.priceList;
create table brightpearl_stance.priceList
(
    priceListId smallint NOT NULL
        CONSTRAINT PK_PRICE PRIMARY KEY
    ,priceListName varchar(100) NULL
    ,code varchar(50) NOT NULL
    ,currencyCode varchar(3)
    ,priceListTypeCode varchar(4) NOT NULL
    ,gross bool NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.productPrice;
create table brightpearl_stance.productPrice
(
    dbProductPriceValue varchar(10) NOT NULL
    ,fkproductId int NOT NULL
    ,fkpriceListId smallint REFERENCES brightpearl_stance.priceList (priceListId)
    ,quantityPriceNumber varchar(10) NOT NULL
    ,quantityPriceValue decimal (10,2) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.brand;
create table brightpearl_stance.brand
(
    brandId smallint NOT NULL
        CONSTRAINT PK_BRAND PRIMARY KEY
    ,brandName varchar(100) NULL
    ,brandDescription varchar(255) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.productsOptionValue;
create table brightpearl_stance.productsOptionValue
(
    optionValueId smallint NOT NULL
        CONSTRAINT PK_PRODOP PRIMARY KEY
    ,optionValueName varchar(255) NULL
    ,optionId smallint
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    );


drop table if exists brightpearl_stance.brightpearlCategory;
create table brightpearl_stance.brightpearlCategory
(
    brightpearlCategoryId smallint NOT NULL
        CONSTRAINT PK_BPCAT PRIMARY KEY
    ,brightpearlCategoryName varchar(100) NULL
    ,parentId smallint NULL
    ,active bool NOT NULL
    ,description varchar(255) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.productType;
create table brightpearl_stance.productType
(
    productTypeId smallint NOT NULL
        CONSTRAINT PK_PRODTYP PRIMARY KEY
    ,productTypeName varchar(100) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.season;
create table brightpearl_stance.season
(
    seasonId smallint NOT NULL
        CONSTRAINT PK_SEASON PRIMARY KEY
    ,seasonName varchar(100) NOT NULL
    ,seasonDescription varchar(255) NULL
    ,dateFrom date NOT NULL
    ,dateTo date NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.products;
create table brightpearl_stance.products
(
    dbproductIdOptionValue varchar(20) NOT NULL         
    ,productId int NOT NULL
    ,fkBrandId int NOT NULL REFERENCES brightpearl_stance.brand (brandId)
    ,fkOptionValueId smallint REFERENCES brightpearl_stance.productsOptionValue (optionValueId)
    ,optionname varchar(50) NOT NULL
    ,fkProductTypeId smallint
    ,fkBrightpearlCategoryId smallint REFERENCES brightpearl_stance.brightpearlCategory (brightpearlCategoryId)
    ,fkSeasonId smallint
    ,sku varchar(100)
    ,barcode varchar(255)
    ,productGroupId smallint
    ,featured bool
    ,dimensionsLength varchar(20)
    ,dimensionsHeight varchar(20)
    ,dimensionsWidth varchar(20)
    ,dimensionsVolume varchar(20)
    ,salesChannelName varchar(255)
    ,productName varchar(255)
    ,productCondition varchar(20)
    ,status varchar(50)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    ,PRIMARY KEY(productId, fkOptionValueId)
    ,CONSTRAINT U_PROD_T UNIQUE (dbproductIdOptionValue)
);

drop table if exists brightpearl_stance.productavailability;
create table brightpearl_stance.productavailability
(
    productAvailabilityId SERIAL NOT NULL        
    ,productId int NOT NULL
        CONSTRAINT PK_PRODAVA PRIMARY KEY    
    ,inStock smallint DEFAULT 0
    ,onHand smallint DEFAULT 0
    ,allocated smallint DEFAULT 0
    ,inTransit smallint DEFAULT 0    
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_stance.orders;
create table brightpearl_stance.orders
(
    orderId int NOT NULL
        CONSTRAINT PK_ORD PRIMARY KEY
    ,parentOrderdId int NULL
    ,orderTypeCode varchar(20)
    ,orderStatus varchar(100)
    ,reference varchar(255)
    ,fkcontactId int REFERENCES brightpearl_stance.contacts (contactId)
    ,country varchar(100)
    ,tax varchar(100)
    ,acknowledged bool
    ,orderPaymentStatus varchar(20) NOT NULL
    ,stockStatusCode varchar(3) NOT NULL
    ,allocationStatusCode varchar(3) NOT NULL
    ,shippingStatusCode varchar(3) NOT NULL
    ,shippingMethodId smallint
    ,accountingCurrencyCode varchar(3)
    ,exchangeRate decimal (6,2)
    ,placedOn timestamptz NOT NULL
    ,closedOn timestamptz NOT NULL
    ,deliveryDate timestamptz
    ,taxdate timestamptz
    ,createdById int
    ,totalValueNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,taxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,baseTaxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseTotal decimal (10,2) NOT NULL DEFAULT 0.00
    ,total decimal (10,2) NOT NULL DEFAULT 0.00
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false

);

drop table if exists brightpearl_stance.orderItems;
create table brightpearl_stance.orderItems
(
    dbOrderItemOptionId varchar(50) NOT NULL
        CONSTRAINT PK_ORDITEM PRIMARY KEY
    ,orderItemId int NOT NULL
    ,fkOrderId int REFERENCES brightpearl_stance.orders (orderId)
    ,fkproductId int NOT NULL
    ,quantity smallint
    ,itemCost decimal(10,2)
    ,taxCode varchar(10)
    ,taxRate decimal(8,2)
    ,itemNet decimal(10,2)
    ,itemTax decimal(8,2)
    ,productOptionName varchar(50)
    ,productOptionValue varchar(50)
    ,currencyCode varchar(3)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false    
);

drop table if exists brightpearl_stance.contacts;
create table brightpearl_stance.contacts
(
    contactId int 
    CONSTRAINT PK_CONT PRIMARY KEY
    ,firstName varchar(255)
    ,lastName varchar(255)
    ,email varchar(200)
    ,countryIso varchar(3)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false 

);

drop table if exists brightpearl_yeti.priceList;
create table brightpearl_yeti.priceList
(
    priceListId smallint NOT NULL
        CONSTRAINT PK_PRICE PRIMARY KEY
    ,priceListName varchar(100) NULL
    ,code varchar(50) NOT NULL
    ,currencyCode varchar(3)
    ,priceListTypeCode varchar(4) NOT NULL
    ,gross bool NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.productavailability;
create table brightpearl_yeti.productavailability
(
    productAvailabilityId SERIAL NOT NULL        
    ,productId int NOT NULL
        CONSTRAINT PK_PRODAVA PRIMARY KEY    
    ,inStock smallint DEFAULT 0
    ,onHand smallint DEFAULT 0
    ,allocated smallint DEFAULT 0
    ,inTransit smallint DEFAULT 0    
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);


drop table if exists brightpearl_yeti.productPrice;
create table brightpearl_yeti.productPrice
(
    dbProductPriceValue varchar(10) NOT NULL
    ,fkproductId int NOT NULL
    ,fkpriceListId smallint REFERENCES brightpearl_yeti.priceList (priceListId)
    ,quantityPriceNumber varchar(10) NOT NULL
    ,quantityPriceValue decimal (10,2) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.brand;
create table brightpearl_yeti.brand
(
    brandId smallint NOT NULL
        CONSTRAINT PK_BRAND PRIMARY KEY
    ,brandName varchar(100) NULL
    ,brandDescription varchar(255) NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.productsOptionValue;
create table brightpearl_yeti.productsOptionValue
(
    optionValueId smallint NOT NULL
        CONSTRAINT PK_PRODOP PRIMARY KEY
    ,optionValueName varchar(255) NULL
    ,optionId smallint
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    );


drop table if exists brightpearl_yeti.brightpearlCategory;
create table brightpearl_yeti.brightpearlCategory
(
    brightpearlCategoryId smallint NOT NULL
        CONSTRAINT PK_BPCAT PRIMARY KEY
    ,brightpearlCategoryName varchar(100) NULL
    ,parentId smallint NULL
    ,active bool NOT NULL
    ,description varchar(255) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.productType;
create table brightpearl_yeti.productType
(
    productTypeId smallint NOT NULL
        CONSTRAINT PK_PRODTYP PRIMARY KEY
    ,productTypeName varchar(100) NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.season;
create table brightpearl_yeti.season
(
    seasonId smallint NOT NULL
        CONSTRAINT PK_SEASON PRIMARY KEY
    ,seasonName varchar(100) NOT NULL
    ,seasonDescription varchar(255) NULL
    ,dateFrom date NOT NULL
    ,dateTo date NOT NULL
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
);

drop table if exists brightpearl_yeti.products;
create table brightpearl_yeti.products
(
    dbproductIdOptionValue varchar(20) NOT NULL         
    ,productId int NOT NULL
    ,fkBrandId int NOT NULL REFERENCES brightpearl_yeti.brand (brandId)
    ,fkOptionValueId smallint REFERENCES brightpearl_yeti.productsOptionValue (optionValueId)
    ,optionname varchar(50) NOT NULL
    ,fkProductTypeId smallint
    ,fkBrightpearlCategoryId smallint REFERENCES brightpearl_yeti.brightpearlCategory (brightpearlCategoryId)
    ,fkSeasonId smallint
    ,sku varchar(100)
    ,barcode varchar(255)
    ,productGroupId smallint
    ,featured bool
    ,dimensionsLength varchar(20)
    ,dimensionsHeight varchar(20)
    ,dimensionsWidth varchar(20)
    ,dimensionsVolume varchar(20)
    ,salesChannelName varchar(255)
    ,productName varchar(255)
    ,productCondition varchar(20)
    ,status varchar(50)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false
    ,PRIMARY KEY(productId, fkOptionValueId)
    ,CONSTRAINT U_PROD_T UNIQUE (dbproductIdOptionValue)
);

drop table if exists brightpearl_yeti.orders;
create table brightpearl_yeti.orders
(
    orderId int NOT NULL
        CONSTRAINT PK_ORD PRIMARY KEY
    ,parentOrderdId int NULL
    ,orderTypeCode varchar(20)
    ,orderStatus varchar(100)
    ,reference varchar(255)
    ,fkcontactId int REFERENCES brightpearl_yeti.contacts (contactId)
    ,country varchar(100)
    ,tax varchar(100)
    ,acknowledged bool
    ,orderPaymentStatus varchar(20) NOT NULL
    ,stockStatusCode varchar(3) NOT NULL
    ,allocationStatusCode varchar(3) NOT NULL
    ,shippingStatusCode varchar(3) NOT NULL
    ,shippingMethodId smallint
    ,accountingCurrencyCode varchar(3)
    ,exchangeRate decimal (6,2)
    ,placedOn timestamptz NOT NULL
    ,closedOn timestamptz NOT NULL
    ,deliveryDate timestamptz
    ,taxdate timestamptz
    ,createdById smallint
    ,totalValueNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,taxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseNet decimal (10,2) NOT NULL DEFAULT 0.00
    ,baseTaxAmount decimal (8,2) NOT NULL DEFAULT 0.00
    ,baseTotal decimal (10,2) NOT NULL DEFAULT 0.00
    ,total decimal (10,2) NOT NULL DEFAULT 0.00
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false

);

drop table if exists brightpearl_yeti.orderItems;
create table brightpearl_yeti.orderItems
(
    dbOrderItemOptionId varchar(50) NOT NULL
        CONSTRAINT PK_ORDITEM PRIMARY KEY
    ,orderItemId int NOT NULL
    ,fkOrderId int REFERENCES brightpearl_yeti.orders (orderId)
    ,fkproductId int NOT NULL
    ,quantity smallint
    ,itemCost decimal(10,2)
    ,taxCode varchar(10)
    ,taxRate decimal(8,2)
    ,itemNet decimal(10,2)
    ,itemTax decimal(8,2)
    ,productOptionName varchar(50)
    ,productOptionValue varchar(50)
    ,currencyCode varchar(3)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false    
);

drop table if exists brightpearl_yeti.contacts;
create table brightpearl_yeti.contacts
(
    contactId int 
    CONSTRAINT PK_CONT PRIMARY KEY
    ,firstName varchar(255)
    ,lastName varchar(255)
    ,email varchar(200)
    ,countryIso varchar(3)
    ,createdOn timestamptz NOT NULL
    ,updatedOn timestamptz NOT NULL
    ,rowimportdate timestamp DEFAULT now()
    ,isdeleted bool DEFAULT false

);