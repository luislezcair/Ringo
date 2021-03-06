import logging
from collections import deque
from sleekxmpp import ClientXMPP

logging.basicConfig(level=logging.INFO)


class XMPPClient(ClientXMPP):
    def __init__(self, jid, password, room, nick):
        ClientXMPP.__init__(self, jid, password)

        self.room = room.lower()
        self.nick = nick

        self.add_event_handler("session_start", self.session_start)

        self.add_event_handler("muc::%s::message" % self.room,
                               self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

        self.add_event_handler("socket_error", self.on_socket_error)

        self.register_plugin('xep_0045')

        self.msg_queue = deque()
        self.ready_to_send = False
        self.disconnect_after_send = False

        self.ca_certs = 'ringoserver/xmpp/xmpp_cert.pem'

    def on_socket_error(self, args):
        logging.error("Socket error %s" % args)
        self.stop.set()

    def session_start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    @staticmethod
    def muc_message(msg):
        logging.debug("MUC MESSAGE RECEIVED! FROM %s" % msg['from'].bare)

    def muc_online(self, presence):
        if presence['muc']['nick'] == self.nick:
            logging.log(logging.DEBUG, "GOT MY OWN PRESENCE!!!!")
            self.ready_to_send = True

            if not self.has_users():
                # TODO: don't send the message. Disconnect and connect to GCM
                logging.info("GO TO INTERNET MODE")
                self.disconnect(wait=False)
                logging.info("Disconnected...")
                return

            # If we have messages in the queue, send them
            if self.msg_queue:
                logging.debug("Sending queued messages...")
                for m in self.msg_queue:
                    self._send_msg_to_muc(m)
                    if self.disconnect_after_send:
                        self.disconnect(wait=True)

                self.msg_queue.clear()

    def send_muc_message(self, msg):
        if self.ready_to_send:
            self._send_msg_to_muc(msg)
            if self.disconnect_after_send:
                self.disconnect(wait=True)
        else:
            logging.debug("Message added to the queue")
            self.msg_queue.append(msg)

    def _send_msg_to_muc(self, msg):
        self.send_message(mto=self.room, mbody=msg, mtype='groupchat')

    def has_users(self):
        """Returns True if there are other users connected to the room"""
        users = self.plugin['xep_0045'].getRoster(self.room)
        return len(users) > 1
