## Large File Processor 
Large File Processing for Postman Assignment

### STEPS to RUN THE Code
- git clone `https://github.com/RheagalFire/Postman-Assignment.git`
- cd `Postman-Assignment`
- open terminal and build docker image using command `docker build -t "image_name" .`
- Run the docker image using comman `docker run "image_name"`
- SSH into a Docker container using `winpty docker exec -it "container_id" bash`
- conatainer Id can be obtained using `docker ps` command. 
- Inside the conatiner's terminal run `python3 create_update.py`

```
If you have a POSTGRES Server setup you can also create the tables just by changing the URI in .env file with your DB_URI. 
```

### Tables
The Above Steps will start a Postgres Server with three Tables as follows: 
- product_list table <br><br>
![img_1](/images/Untitled.png)

This Table is the Table from the CSV file containing 500000 rows. 

- updated_table <br><br>
![img_2](/images/updated_table.png)

This Table is grouped by sku and contains 'sku' as the primary key, This is made for carrying out updates. No. of Rows = 466693

- agg_table <br><br>
![img_3](/images/agg_table.png)

This Table is groued by same name and count as the column where count denotes no. of products related to each name. No. of Rows = 222024

### How to update the Database 
- To update the Database inside the container run update.py file with arguments in order of :`python3 update.py sku name description`.<br><br>
![img_3](/images/update_query.png)

After the Update changes will be reflected in all the Tables. 

#### Product Table to reflect changes after Update 
![img_4](/images/pd-au.png)
#### Agg Table to reflect changes after Update
![img_5](/images/agg-au.png)
#### Updated Table to reflect changes after Update
![img_6](/images/up-au.png)

### How to Query the Database
- Inside the container run this command `psql -U postgres -d postgres`
- To query the product_list table run `SELECT * FROM product_list;`
- To query the updated_table run `SELECT * FROM updated_table;`
- To query the agg_table run `SELECT * FROM agg_table;`

### What all is done from POINTS TO ACHIEVE 
- According to my assumptions from reading the problem statement none of the points has been left out from points to achieve. 
- All the Code follow the concept of OOPS. 
- Support for non blocking parallel ingestion of file into table.
- Support for updating the database with `sku` as the primary key. 
- All the product details are ingested into single table called `product_list`.
- An aggregated table is made with `name` and `no. of products` as columns. 

### What would I do if Given more days 
- Come up with a better design patter to solve the problem. 
- Properly Document the Whole code.
- Make an API to update the Above tables. 

### Assumptions Made
- The Database is updated with one record at a time. 
- It is necessary to ingest the given `csv` file(in its as is state) into a table. 
- All the Modifications are handled with `SQL queries` and not with `pandas`.



