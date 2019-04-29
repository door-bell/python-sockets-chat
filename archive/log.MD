# Cumulative Log

This file contains the contents of all log files in each version of the source code I created.


## 5ab4a63

From the initial commit to this version, I used the following "guide" 
in supplement to my guide to get things up and running quickly:

https://www.journaldev.com/15906/python-socket-programming-server-client

I believe that this article contained some code that I used, but now 
for whatever reason I can't find it anywhere. I know that I used this 
guide because I included it in a commit message (9364838).

Anyway, the main achievement in this iteration is that I learned to use 
the threading library to "listen" for messages from the server in the 
background while still taking input. However, the listen method is connecting 
to a socket from within a while true loop, so it's clearly not refined in any way.

At this point I was getting a 'broken pipe error' which probably 
had to do with the very broken while true loop.

An additional note: I realized that quitting the client program would 
result in the server getting flooded with empty messages. This is why 
the client_thread method checks "if not msg" in order to break out and 
close the socket if it detects the client quit the program / disconnected.

## b0cd0ff

In this iteration, I fixed the broken pipe error from 
the last version, and made big progress in multi-threading the
server.

Client achievements:
    I moved around some of the socket code and fixed the broken
    pipe error: The while true loop for the listen thread works!
    
    The client has a bit of a nicer input prompt, and must wait one
    second before sending another message (this is implemented in 
    the client side, so technically they don't need to wait)

Server achievements:
    The server was completely rewritten.
    
    The server is now multi-threaded. The main thread listens 
    for new connections, and when a new connection is opened it 
    creates a 'client thread' that first waits for a message from 
    the client and then sends the message to the client.

## 662ac11

Client achievements:
    The client no longer uses a global socket variable, instead it 
    passes it along as a parameter to follow better programming practices. 
    
Server achievements:
    I realized that the previous server would not send messages 
    to everyone as soon as they are received as a chat server 
    should, so I created a separate thread for message broadcasting.
    This means that multiple connected clients can both send and 
    receive messages simultaneously (yay!). 

This is also the last commit of the first day of binge programming 
this project.

## 20b7bf1

At this point in development, I was facing the issue of 
the client-side code not taking input very nicely.
I wanted the prompt on the last line of output, and messages
to be inserted above it. Over the next few commits up to this version,
I tried my very best to solve this issue. However, after many hours 
of fiddling and researching special escape characters, I realized
that it was more trouble than it was worth, considering this is 
a *networking* project. 

However, there was still a major change in terms of 
the protocol:

Starting off I had no clear vision of how the protocol should 
look, but in this iteration it took its form. I came up with 
the following message format for the application messages:
    {NICKNAME}: {MESSAGE}
The client sends a message like this, and the server simply 
echoes this out to all other connected clients.

## 13fbf78

This very small iteration contained a few changes:

Client changes:
    I started to use stdout instead of the plain print function
    in order to keep output consistent (my dreams of a pretty CLI
    were still kicking)

Server changes:
    I added mutex locks to the global variables in order to 
    prevent two threads from using the variables at the same time.
    This prevents any possible race conditions and other non-deterministic
    nightmares (though I never experienced one in development).

## 17f84e4

Client achievements:
    Added a mutex for writing to stdout (turns out sys.stdout.write
    is not thread safe).

    I added a keyword "later" that would indicate the client intends to 
    disconnect from the server. This is much more graceful than the 
    abrupt CTRL+C disconnects I was using before, but also not exactly ideal 
    since a user might want to end their message with "later" but not disconnect.

    After researching the threading library docs, I learned that there is 
    an option for the Thread object that makes it a daemon, which means 
    that the thread will exit if the main thread exits. This is a much better 
    practice because we no longer have to exit these threads before 
    exiting the program (which I wasn't doing in the first place: oops)
        I made the listen thread a daemon so that it would close with the main
        thread.

Server achievements: 
    I learned that a thread should return a value after it is done running, 
    otherwise python gets angry. So, I added a return value to the client thread 
    so that disconnected clients would have their thread closed. 

    The server also checks for this "later" keyword and breaks out of the 
    infinite loop of receiving messages if the client's message ends with it.

## 423a3ce

Server achivements:
    Added command parsing code. In this iteration, any message that 
    begins with a / is considered a command. The user's message is passed 
    to handleCommand() to handle whatever functionality is necessary.


## e222c07

At this point I was having issues implementing a potential 
"whisper" command, because it would be impossible to tell 
which socket belongs to which nickname. So, I re-factored much
of the server side code.
Additionally, I had a change in philosophy for the protocol's 
message order, so this is a pretty big version.

Protocol (client + sever):
    Now, the client's first message to the server must be their 
    desired nickname to avoid duplicate nicknames. The client can 
    assume if it does not get an OK signal that the nickname is 
    in use or is invalid in some other way.

Server:
    Re-factored how we keep track of clients. Now, they are 
    stored in a dictionary mapping nicknames -> socket objects.
    This will enable the server to target particular nicknames when
    sending messages. 
    This changed involved lots of renaming but also lots of re-considering 
    how to detect commands and broadcast messages. 
    This also made it possible to detect nicknames that are already in use.

My code was starting to get ugly at this point, particularly in 
the handling of commands.

## 4f81e27

This version only included changes in the server code.

Server:
    Properly check for duplicate nicknames
    Iterate through clients properly when broadcasting.
    Make broadcast thread a daemon. This thread is constantly running when
    the server is on, so it is convenient to not need to close the thread 
    when the server is closed.

    Re-factor command parsing so that we can get the arguments in a more 
    convenient way. 
    Implement a whisper command: Since we are now keeping track of 
    nicknames, we can send messages to specific sockets. 

## edcaf9b

  This version was where I finally came to a concrete 
form of my protocol. 

The client's first message to the server is still the desired 
nickname. The client will receive an "OK" message if the nickname is valid, 
and then any messages the clients send is now considered a message by the 
server. The main change is in the format of these messages.

Before, the client sent a nickname and a the text of the message with each 
message. This meant that someone could potentially send a message with someone 
else's nickname. 

BUT: now, the client only sends the text of their message. The server keeps track of 
who sent the messages by keeping the 'nickname' variable local to each client's 
individual thread.

## 8859110

From the last version to this one, there was a lot of 
polishing of the code and a little change in functionality.

Server:
    The hello command is now a novelty command, it no longer
    is a part of the core protocol.


A list of minor changes include:
    Moving/removing whitespace
    Fixing command parsing (no more regex required!)
    Changing the nickname verification method to look nicer
    Switch all strings over to fstrings (Python 3)
    Remove input prompt since I could never keep things pretty anyway
