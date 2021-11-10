import socket
import logging
from emoji import demojize
from multiprocessing import Process
from string import Template

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])


"""
Get token here: https://twitchapps.com/tmi/
"""

server = 'irc.chat.twitch.tv'
port = 6667
nickname = '<YOUR_USERNAME>'
token = '<YOUR_TOKEN>'
channels = ['#channel1','#channel2']


def main(channel='#commanderroot'):
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                if resp.find('PRIVMSG') != -1 and not(resp.startswith(':streamelements')) and not(resp.startswith(':nightbot')) and not(resp.startswith(':streamlabs')):
                    chattername = resp[1:resp.find('!')]
                    chattext = demojize(resp[resp.find(':', 1) + 1:resp.find('\n')])
                    output = Template('$who in $where: $what').substitute(where=channel, who=chattername, what=chattext)
                    logging.info(output)

    except KeyboardInterrupt:
        sock.close()

if __name__ == '__main__':
    processes = []
    for irc in channels:
        proc = Process(target=main, args=(irc,))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    exit()
