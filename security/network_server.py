
import select, socket, sys, queue
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('127.0.0.1', 8080))
server.listen(5)
inputs = [server]
outputs = []
message_queue = queue.Queue()
status = {}

#This dict allows mapping to house - IP and pin to location being monitored.
#List the assigned ips here


hardware_mappings = {}



#code obtained from:
#https://steelkiwi.com/blog/working-tcp-sockets/
#edit to use singular message queue. Will run in thread
#will provide data stream to GUI




def check_sensors():
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs, 0)

    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            #message_queues[connection] = Queue.Queue()
        else:
    
            data = s.recv(1024)
    
            if data:
                message_queue.put(data)
                #if s not in outputs:
                #    outputs.append(s)
            #else:
            #    if s in outputs:
            #        outputs.remove(s)
            #    inputs.remove(s)
            #    s.close()
            #    del message_queues[s]

    #will be used for roll call - check all nodes are connected and say something if not. 
    #for s in writable:
    #    else:
    #        s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        #del message_queues[s]


        
