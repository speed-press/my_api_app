# Introduction

This project stemmed from a requirement to use a db that wasn't built
for the api, but rather the api was just layered on top to access a key
subset of information in rather large tables. It didn't make sense to go
the SQL alchemy route built into flask and define the tables/objects in
that manner, but rather just use sql queries with argument placement.
Since this isn't a public api, we didn't worry about SQL injection.

It was also a learning experience for myself for than anything.

Author Notes:

- The api_template design was specifically for simple endpoint design in
which there isn't a hard requirement for each endpoint requiring 
differentsetups that the current template couldn't support.
    - You can still implement the standard configuration as seen in the 
    example inside '/myapp/store/api.py'
    - For testing, a placeholder custom function was implemented in the
    api file that does not access the db
- The SQL implementation isn't mature and doesn't incldue all the 
functions beyond SELECT / INSERT. 
- Auth is not built out.
    - There is an api_key implementation, but does not include how that
    is generated.
- DB connection uses PYODBC and thus requires a connection string. The 
associated fields are inn the db config file 'config/db_config.ini'. 
Theres also a yaml version, but wasn't set up quite yet. 
    - The API template has the required get_db fields commented out
    until an actual DB config set up.

-Victor


## Initial Configuration

    ```

