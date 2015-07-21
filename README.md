# WhatBot


**Requirements:**
- **Yowsup** - pip install yowsup2
- **MySQLdb** - pip install mysql-python
- **BlockIo** - pip install block-io
- **Untangle** - pip install untangle
- **Requests** - pip install requests 

**Setup:**

. Create a mysql database with following schema:

```
CREATE TABLE whatdata (
   id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
   tag  varchar(25) DEFAULT NULL,
   user  varchar(100) DEFAULT NULL,
   balance  int(11) DEFAULT NULL,
   address  varchar(100) DEFAULT NULL,
   coinapi  varbinary(200) DEFAULT NULL
) 
```
