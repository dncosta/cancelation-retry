# moip-cancelation-retry
Scripts that can eventually be useful

# pags-retry

Sends pending refunds to PagSeguro.
How it works:

1. First it retrieves the pending refunds from the database through Metabase's API. 
The query itself is written in SQL and is stored by Metabase. Any changes needed must be done there

2. The connection with metabase depends on:
a. Being in Moip's network
b. Having a Metabase user with access to te query mentioned

How to use it:

1. Just include your user and passwords in the variables `username`and `password`, then the script should work just fine.
