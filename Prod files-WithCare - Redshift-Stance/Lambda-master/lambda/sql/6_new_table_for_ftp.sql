create schema countwise;

CREATE TABLE countwise.footfall
(
    content_site varchar(255) NOT NULL
    ,content_date date NOT NULL
    ,content_time time
    ,content_in int NOT NULL
    ,content_bypass int NOT NULL
    ,rowimportdate timestamp DEFAULT now()    
);