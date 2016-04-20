Runtime:
    python 2.7

Running the code:
    navigate to the project root directory
    run python main.py
    ctrl-c to exit

Testing the code:
    Two options:
    1. run python -m unittest discover from the command line inside the project root directory
    2. run "sudo pip install nose", and then run "nosetests" from the command line inside the project root directory

Design Rationale:
The main layers in this exercise:
    1. Network - defines the socket server that listens, the connection that reads the input and the protocol interpreter.
        If we ever want to change the protocol we can either fix the LineProtocol, or create a new protocol handler
    2. Storage - I defined an abstract storage interface, and then implemented an in-memory storage that complies with that interface.
            This allows us to create an SQLStorage if we wanted to, or "RedisStorage" or "MemCacheStorage" and so on.
            The storage is "stupid" , meaning it knows how to add/get/remove and some other commands, but it is not aware of business logic rules
    3. Business logic - encapsulates the access to the storage, and handles higher level logic (like deciding if all
                    conditions apply in order to perform an action), it adds another layer, but it also gives us
                    robustness and flexibility.

The nice thing is that for future maintenance, it sort of lets you to mix and match.
In the future I can have a "UDPListener", with a "BinaryProtocol" and a "RedisStorage" , given that i implement them.


