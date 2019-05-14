# The Web Server

Initialize the CouchDB database and create a web application virtulizing the findings.

----

To start, simply run the following command, it will listen to 127.0.0.1:8000.

```python3 web.py```

To start the server listening to a customized port:

```python3 web.py -p <the port>```

Note that the server will NOT initialize the CouchDB database if it listens to a port other than 8000.
