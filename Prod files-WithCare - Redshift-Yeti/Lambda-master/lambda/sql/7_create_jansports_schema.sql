CREATE SCHEMA brightpearl_jansports;

GRANT USAGE ON SCHEMA brightpearl_jansports TO vvast_admin;

GRANT SELECT ON ALL TABLES in SCHEMA brightpearl_jansports TO vvast_admin;

CREATE TABLE brightpearl_jansports.brand (
	brandid int2 NOT NULL,
	brandname varchar(100) NULL,
	branddescription varchar(255) NOT NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_brand PRIMARY KEY (brandid)
);

CREATE TABLE brightpearl_jansports.brightpearlcategory (
	brightpearlcategoryid int2 NOT NULL,
	brightpearlcategoryname varchar(100) NULL,
	parentid int2 NULL,
	active bool NOT NULL,
	description varchar(255) NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_bpcat PRIMARY KEY (brightpearlcategoryid)
);

CREATE TABLE brightpearl_jansports.errorlog (
	logid serial NOT NULL,
	loginname varchar(50) NOT NULL,
	modulename varchar(50) NOT NULL,
	errordescription varchar(255) NULL,
	createdon timestamptz NOT NULL DEFAULT now(),
	updatedon timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT pk_log PRIMARY KEY (logid)
);

CREATE TABLE brightpearl_jansports.productsoptionvalue (
	optionvalueid int2 NOT NULL,
	optionvaluename varchar(255) NULL,
	optionid int2 NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_prodop PRIMARY KEY (optionvalueid)
);

CREATE TABLE brightpearl_jansports.producttype (
	producttypeid int2 NOT NULL,
	producttypename varchar(100) NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_prodtyp PRIMARY KEY (producttypeid)
);

CREATE TABLE brightpearl_jansports.season (
	seasonid int2 NOT NULL,
	seasonname varchar(100) NOT NULL,
	seasondescription varchar(255) NULL,
	datefrom date NOT NULL,
	dateto date NOT NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_season PRIMARY KEY (seasonid)
);

DROP TABLE IF EXISTS brightpearl_jansports.products
CREATE TABLE brightpearl_jansports.products (
	dbproductidoptionvalue varchar(20) NOT NULL,
	productid int4 NOT NULL,
	fkbrandid int4 NOT NULL,
	fkoptionvalueid int2 NOT NULL,
	optionname varchar(50) NOT NULL,
	fkproducttypeid int2 NULL,
	fkbrightpearlcategoryid int2 NULL,
	fkseasonid int2 NULL,
	sku varchar(100) NULL,
	barcode varchar(255) NULL,
	productgroupid int2 NULL,
	featured bool NULL,
	dimensionslength varchar(20) NULL,
	dimensionsheight varchar(20) NULL,
	dimensionswidth varchar(20) NULL,
	dimensionsvolume varchar(20) NULL,
	saleschannelname varchar(255) NULL,
	productname varchar(255) NULL,
	productcondition varchar(20) NULL,
	status varchar(50) NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT products_pkey PRIMARY KEY (productid, fkoptionvalueid),
	CONSTRAINT u_prod_t UNIQUE (dbproductidoptionvalue)
);


-- brightpearl_jansports.products foreign keys

ALTER TABLE brightpearl_jansports.products ADD CONSTRAINT products_fkbrandid_fkey FOREIGN KEY (fkbrandid) REFERENCES brightpearl_jansports.brand(brandid);
ALTER TABLE brightpearl_jansports.products ADD CONSTRAINT products_fkbrightpearlcategoryid_fkey FOREIGN KEY (fkbrightpearlcategoryid) REFERENCES brightpearl_jansports.brightpearlcategory(brightpearlcategoryid);

CREATE TABLE brightpearl_jansports.productprice (
	dbproductpricevalue varchar(10) NOT NULL,
	fkproductid int4 NOT NULL,
	fkpricelistid int2 NULL,
	quantitypricenumber varchar(10) NOT NULL,
	quantitypricevalue numeric(10,2) NOT NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false
);

CREATE TABLE brightpearl_jansports.productavailability (
	productavailabilityid varchar(25) NOT NULL,
	productid int4 NOT NULL,
	instock int2 NULL DEFAULT 0,
	onhand int2 NULL DEFAULT 0,
	allocated int2 NULL DEFAULT 0,
	intransit int2 NULL DEFAULT 0,
	warehouse int2 NULL DEFAULT 0,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_prodava PRIMARY KEY (productavailabilityid)
);

CREATE TABLE brightpearl_jansports.pricelist (
	pricelistid int2 NOT NULL,
	pricelistname varchar(100) NULL,
	code varchar(50) NOT NULL,
	currencycode varchar(3) NULL,
	pricelisttypecode varchar(4) NOT NULL,
	gross bool NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_price PRIMARY KEY (pricelistid)
);

CREATE TABLE brightpearl_jansports.contacts (
	contactid int4 NOT NULL,
	firstname varchar(255) NULL,
	lastname varchar(255) NULL,
	email varchar(200) NULL,
	countryiso varchar(3) NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_cont PRIMARY KEY (contactid)
);

CREATE TABLE brightpearl_jansports.orders (
	orderid int4 NOT NULL,
	parentorderdid int4 NULL,
	ordertypecode varchar(20) NULL,
	orderstatus varchar(100) NULL,
	reference varchar(255) NULL,
	fkcontactid int4 NULL,
	country varchar(100) NULL,
	tax varchar(100) NULL,
	acknowledged bool NULL,
	orderpaymentstatus varchar(20) NOT NULL,
	stockstatuscode varchar(3) NOT NULL,
	allocationstatuscode varchar(3) NOT NULL,
	shippingstatuscode varchar(3) NOT NULL,
	shippingmethodid int2 NULL,
	accountingcurrencycode varchar(3) NULL,
	exchangerate numeric(8,6) NULL,
	placedon timestamptz NOT NULL,
	closedon timestamptz NOT NULL,
	deliverydate timestamptz NULL,
	taxdate timestamptz NULL,
	createdbyid int2 NULL,
	totalvaluenet numeric(10,2) NOT NULL DEFAULT 0.00,
	taxamount numeric(8,2) NOT NULL DEFAULT 0.00,
	basenet numeric(10,2) NOT NULL DEFAULT 0.00,
	basetaxamount numeric(8,2) NOT NULL DEFAULT 0.00,
	basetotal numeric(10,2) NOT NULL DEFAULT 0.00,
	total numeric(10,2) NOT NULL DEFAULT 0.00,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_ord PRIMARY KEY (orderid)
);

CREATE TABLE brightpearl_jansports.orderitems (
	dborderitemoptionid varchar(50) NOT NULL,
	orderitemid int4 NOT NULL,
	fkorderid int4 NULL,
	fkproductid int4 NOT NULL,
	quantity int2 NULL,
	itemcost numeric(10,2) NULL,
	taxcode varchar(10) NULL,
	taxrate numeric(8,2) NULL,
	itemnet numeric(10,2) NULL,
	itemtax numeric(8,2) NULL,
	productoptionname varchar(50) NULL,
	productoptionvalue varchar(50) NULL,
	currencycode varchar(3) NULL,
	createdon timestamptz NOT NULL,
	updatedon timestamptz NOT NULL,
	rowimportdate timestamp NULL DEFAULT now(),
	isdeleted bool NULL DEFAULT false,
	CONSTRAINT pk_orditem PRIMARY KEY (dborderitemoptionid)
);