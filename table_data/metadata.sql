
CREATE TABLE orders_data (
	productid INTEGER, 
	productname VARCHAR(4000), 
	category VARCHAR(50), 
	categoryid INTEGER, 
	orderid INTEGER, 
	customerid INTEGER, 
	orderstatus VARCHAR(50), 
	returneligible BOOLEAN, 
	shippingdate VARCHAR(50)
)


CREATE TABLE product_data (
	productid INTEGER, 
	productname VARCHAR(4000), 
	merchantid INTEGER, 
	clusterid INTEGER, 
	clusterlabel VARCHAR(4000), 
	categoryid INTEGER, 
	category VARCHAR(50), 
	price REAL, 
	stockquantity INTEGER, 
	description VARCHAR(4000), 
	rating REAL
)

