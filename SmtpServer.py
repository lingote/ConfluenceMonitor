import smtpd
import asyncore


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        return


#server = CustomSMTPServer(('192.168.10.49', 1025), ('mail', 25), decode_data=True)
server = smtpd.PureProxy(('192.168.10.49', 1025), ('mail', 25), decode_data=True)

asyncore.loop()