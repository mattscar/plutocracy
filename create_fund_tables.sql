CREATE TABLE sp500 (ticker varchar(8) CONSTRAINT firstkey PRIMARY KEY, name varchar(50) NOT NULL, sector sector_type NOT NULL, subsector subsector_type NOT NULL);

