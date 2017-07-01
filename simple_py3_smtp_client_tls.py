#used resources from Ratan Dey @ NYU Poly
#run in Python 3.6

import socket
import ssl
import base64


def open_tls_socket(svrname, port):
    # Create socket called clientSocket and establish a TCP connection with mailserver
    #taken from https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tls_sock = context.wrap_socket(s, server_hostname = svrname)
    tls_sock.connect((svrname, port))

    #fetched_cert = ssl_sock.getpeercert()
    #print (fetched_cert)
    return tls_sock

def auth_account(user, passwd, socket):
    #https://stackoverflow.com/questions/33397024/mail-client-in-python-using-sockets-onlyno-smtplib
    heloCommand = 'HELO Clarice\r\n'
    socket.send(heloCommand.encode())
    helo_response = socket.recv(1024)
    #print (recv.decode())
    base64_str = ("\x00"+user+"\x00"+passwd).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    socket.send(authMsg)
    auth_response = socket.recv(1024)
    return helo_response, auth_response

def auth_response_search(decoded_msg):
    responses = '235'
    for t in responses:
        i = decoded_msg.find(t)
        if t != -1:
            return True
        else:
            printf("Authentication error or reponse undefined in this version.")
            return False

""""
for future imap client work
def imap_response_search(decoded_msg):
    #https://tools.ietf.org/html/rfc5530
    #support for imap responses, OK, NO, BAD
    #finding the key words in response:
    #https://stackoverflow.com/questions/18937562/finding-substring-in-python
    responses = 'OK', 'NO', 'BAD'
    for t in responses:
        i = decoded_msg.find(t)
        if i != -1:
            print('IMAP resonse of {} from server.'.format(t))
            return True
        else:
            print('No standard response from IMAP server.')
            return False
"""

def smtp_response_search(decoded_msg):
    #http://www.greenend.org.uk/rjk/tech/smtpreplies.html
    #only supporing a few smtp replies, 220, service ready
    #250, Requested mail action OK, completed
    #230
    responses = '250', '220'
    for t in responses:
        i = decoded_msg.find(t)
        if t is '250':
            response = 'Requested mail action okay, completed.'
            print('SMTP response code {}, {}.'.format(t, response))
            return True
        elif t is '220':
            response = 'Mail Action Completed.'
            print('SMTP response code {}, {}.'.format(t, response))
            return True
        else:
            print("SMTP response code not implemented or returning error.")
            return False

# Choose a mail server (e.g. Google mail server) and call it mailserver
msg = '\r\n I love computer networks!'
endmsg = '\r\n.\r\n'

#account info
user = input('Please enter address for Gmail Account: ')
passwd = input('Please enter password for ' + user + ': ')

recipient_addr = input('Please enter recipient address: ')

#Gmail outbound server and port , smtp.gmail.com, 465
#https://support.google.com/mail/answer/7126229?hl=en
smtp_mailserver = 'smtp.gmail.com'
smtp_mailserver_port = 465


smtp_tls_sock = open_tls_socket(smtp_mailserver, smtp_mailserver_port)
recv = smtp_tls_sock.recv(1024)
#print (recv.decode())
if (smtp_response_search(recv.decode())):
    print('Continue...Authentication for SMTP.')
    #need to now authenticate account
    helo_response, auth_response = auth_account(user, passwd, smtp_tls_sock)
    print ('helo response {}'.format(helo_response.decode()), end='')
    print ('auth response {}'.format(auth_response.decode()), end='')
    if auth_response_search(auth_response.decode()):
        print ('Continue with SMTP message send.')
        #https://stackoverflow.com/questions/33397024/mail-client-in-python-using-sockets-onlyno-smtplib
        from_field = "MAIL FROM:<" + user + ">\r\n"
        print("Sending MAIL FROM field.")
        smtp_tls_sock.send(from_field.encode())
        if smtp_response_search(smtp_tls_sock.recv(1024).decode()):
            recipient_field = "RCPT TO:<" + recipient_addr + ">\r\n"
            print("Sending RCPT TO field.")
            smtp_tls_sock.send(recipient_field.encode())
            if smtp_response_search(smtp_tls_sock.recv(1024).decode()):
                data = 'DATA\r\n'
                print("Sending DATA field.")
                smtp_tls_sock.send(data.encode())
                if smtp_response_search(smtp_tls_sock.recv(1024).decode()):
                    smtp_tls_sock.send(msg.encode())
                    smtp_tls_sock.send(endmsg.encode())
                    if smtp_response_search(smtp_tls_sock.recv(1024).decode()):
                        quit = 'QUIT\r\n'
                        print("Sending QUIT.")
                        smtp_tls_sock.send(quit.encode())
                        if smtp_response_search(smtp_tls_sock.recv(1024).decode()):
                            print('SMTP requests completed successfully.')
"""
#for future incoming mail option....
#Send mail Option
#https://support.google.com/mail/answer/7126229?hl=en
imap_mailserver = 'imap.gmail.com'
imap_mailserver_port = 993

imap_tls_sock = open_tls_socket(imap_mailserver, imap_mailserver_port)
recv = imap_tls_sock.recv(1024)
#print (recv.decode())

if imap_response_search(recv.decode()):
    print('Continue...Authentication for IMAP...')
    #need to now authenticate account
else:
    print('Please check connection settings.')
"""
