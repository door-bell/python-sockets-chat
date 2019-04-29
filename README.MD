# Python Sockets Chat: CS322

This repo contains a client and server application that communicates using my own application layer protocol over TCP.

## Setup

The code should work out of the box, just verify python version (at least 3.6):

```
$ python --version
Python 3.7.2
```

Start the server:

```
$ python server.py
Starting server at 127.0.0.1
```

Start clients (up to 5) in separate terminals:
```
$ python client.py
...
```

By default, the client automatically connects to 127.0.0.1:8555 without prompting for an IP address/port.

If you run into issues, check `/etc/hosts` or the windows `C:\Windows\System32\Drivers\etc\hosts` and look for an IP address that might work as a subsitute to 127.0.0.1, like `localhost` or your computer's hostname. Then, simply change the `HOST = ...` line in server.py and client.py to use that IP address.

## The Protocol:

![Protocol Diagram](https://i.imgur.com/A5WZoMu.jpg)

## The Server Implementation

![Server Diagram](https://i.imgur.com/s88R4fP.jpg)

# Work hours

|  Date  	| Hours 	| Total 	|
|:------:	|:-----:	|:-----:	|
| Feb 11 	|  2.25 	|  2.25 	|
| Feb 12 	|  0.5  	|  2.75 	|
| Feb 13 	|   1   	|  3.75 	|
| Feb 14 	|  0.5  	|  4.25 	|
| Feb 15 	|  0.33 	|  4.58 	|
| Feb 16 	|  0.33 	|  4.91 	|
| Feb 17 	|   2   	|  6.91 	|
| Feb 19 	|  1.66 	|  8.57 	|
| Mar 12    |  0.5      |  9.07     |
| Mar 21    |  0.2      |  9.27     |
| Mar 22    |  0.1      |  9.37     |

## View commits and specific times in the Terminal:

`git log --pretty=format:"%h%x09%an%x09%ad%x09%s"`

Sometimes I worked for a while before a commit was made, and sometimes commits were spread out in strange ways. The work hours are reasonably accurate despite these irregularities.
