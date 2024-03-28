#!/usr/bin/env python3
import socket as sock
import asyncio
import time
import argparse
import logging
import sys
import socket

BUFF_SIZE = 4096

logger = logging.getLogger(__name__)

async def create_relay(s, dst_addr, dst_port, loop):
    conn_no = 0
    while True:
        conn_no += 1
        s1, s1_addr = await loop.sock_accept(s)  # while awaiting sock_accept no other task is run
        logger.info('New incoming Connection id ' + str(conn_no) + ' from ' + s1_addr[0] + ":" + str(s1_addr[1]))

        s2 = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        s2.setblocking(False)
        logger.debug('Trying to connect to ' + dst_addr + ":" + str(dst_port) + " for id " + str(conn_no))

        await loop.sock_connect(s2, (dst_addr, dst_port))
        loop.create_task(relay(s1, s2, loop, 'SERVER-' + str(conn_no)))
        loop.create_task(relay(s2, s1, loop, 'CLIENT-' + str(conn_no)))
        # await asyncio.sleep(1000)        # while awaiting sleep the relay tasks are run

async def relay(s1, s2, loop, name):
    while True:
        data = await loop.sock_recv(s1, BUFF_SIZE)
        if not data:
            break
        logger.debug(name + " " + str(bytes(data).hex()))
        await loop.sock_sendall(s2, data)

    logger.debug('Socket Terminated for ' + name)
    s2.shutdown(socket.SHUT_WR)

def init_relay(listen_port, dst_addr, dst_port = None, listen_addr = None):
    if listen_addr == None:
        listen_addr = '0.0.0.0'
    if dst_port == None:
        dst_port = listen_port

    s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    s.setblocking(False)
    s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    s.bind((listen_addr, listen_port))
    s.listen()
    logger.info("Listening on " + listen_addr + ":" + str(listen_port))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_relay(s, dst_addr, dst_port, loop))


if __name__ == '__main__':
    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') #  %(name)s 

    parser = argparse.ArgumentParser(
        prog='relay_socket',
        description='Listen to a socket, and create a new connection to a remote address and relay information in both direction',
        epilog='Epilog here?')
    parser.add_argument('-b', '--listen-address', default=None)      # option that takes a value
    parser.add_argument('-p', '--listen-port', required=True, type=int)
    parser.add_argument('-d', '--destination-address', required=True)
    parser.add_argument('-P', '--destination-port', default=None, type=int)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('-D', '--debug', action='store_true', default=False)

    parser.add_argument('-l', '--log-file', default=None)


    args = parser.parse_args()

    #logging.basicConfig(level=logging.DEBUG)#filename='myapp.log', level=logging.INFO)
    if args.debug == True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.verbose:
        handler = logging.StreamHandler(stream=sys.stdout)
        #handler.setLevel(logging.DEBUG)
        handler.setFormatter(logFormatter)
        logger.addHandler(handler)

    if args.log_file:
        logFileFormatter = logging.Formatter('%(created)f %(levelname)s %(message)s') #  %(name)s 
        fileHandler = logging.FileHandler("{0}".format(args.log_file))
        fileHandler.setFormatter(logFileFormatter)
        logger.addHandler(fileHandler)

    #logger.setLevel(logging.DEBUG)

    print(args)
    print("AA")
    #Namespace(listen_address=None, listen_port='5000', destination_address='23.171.128.3', destination_port=None, verbose=False)
    init_relay(args.listen_port, args.destination_address, args.destination_port, args.listen_address)
