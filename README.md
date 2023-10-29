# FTP
A python implementation of an FTP client and server. It uses socket programming in Python in order to send & receive file across client & server. The server is multi-threaded and can connect to several clients at the same time.

## Usage
The server can be started with ``` python3 server.py PORT_NUMBER ```. 
Similarly, the client would be started with ```python3 client.py PORT_NUMBER```, where the PORT_NUMBER must be the one used to start the server.

Once the client is connected to the server, the commands must be run from the client. The program offers full bidirectional access, meaning that the client can send as well as receive files to the server. The nomenclature followed is that the commands meant to be run on the server are typed as is, versus the commands meant to be run on the client system itself are prepended with a ```!```.

### Example
On the server - 

```python3 server.py 1010```.

On the client - 
```
python3 client.py 1010
ftp> !ls
command_map.txt    server.py    test    suffix-try.py    client.py    bugs.txt    ftp.txt    .git    'RFC 959 - File Transfer Protocol.html'    .idea    
ftp> !cd ..       
OK
ftp> !ls
temporal    ftp
ftp> get server.py
OK
ftp> !ls
temporal    ftp    server.py
ftp> bye
```

In this example, we navigated the client to it's parent folder (with ```!cd ..```) & transfered the file _server.py_ from the server to the client (with ```get server.py```). Finally, we close the connection from client side with ```bye```.


Full list of commands -
```
ls: Run ls on server
!ls: Run ls on client
cd: Navigate on server
!cd: Navigate on client
pwd: Print working directory on server
!pwd: Print working directory on client
get: Transfer file from server to client
mget: Transfer multiple files from server to client
put: Transfer file from client to server
mput: Transfer multiple files from client to server
mkdir: Create a directory on server
!mkdir: Create a directory on client
rm: Remove a file or directory on server
!rm: Remove a file or directory on client
sys: Print system running on server
!sys: Print system running on client
user: Authenticating user (username, and password)
```
