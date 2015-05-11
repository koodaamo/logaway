# -*- coding: utf-8 -*-

import logging
import pickle #as Pickle
import treq
from klein import Klein,  run, route
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.static import File
from twisted.web.server import Site
from autobahn.twisted.wamp import Application, ApplicationSession, ApplicationRunner

logging.basicConfig()
from twisted.python import log
#
# WAMP publisher
#

class LogPublisherComponent(Application):
   "An application component that publishes log entries via WAMP"

   logger = logging.getLogger("publisher")
   logger.setLevel(logging.INFO)

   def __init__(self, realm = "logging"):
      Application.__init__(self)
      self._realm = realm

   def onConnect(self):
      self.join(self._realm)

   @inlineCallbacks
   def submit(self, sourcehost, loggername, logrecord):
      yield self.session.publish("logging", logrecord)

   @inlineCallbacks
   def onJoin(self, details):
      self.logger.warn("log publisher session started")
      yield

wamppublisher = LogPublisherComponent()


#
# UDP LOG RECORD RECEIVER
#

class ReceivePythonLogRecord(DatagramProtocol):

   def __init__(self, publisher):
      self.publisher = publisher

   def datagramReceived(self, data, (host, port)):
      entry = pickle.loads(data[4:])
      record = logging.makeLogRecord(entry)
      self.publisher.submit(host, record.name, entry)

udpreceive = ReceivePythonLogRecord(wamppublisher)


#
# WEB CLIENT APPLICATION
#

webapp = Klein()

@webapp.route('/', methods=['GET'])
def showentries(request):
   return File("./static/html/")

@webapp.route('/static/', branch=True)
def static(request):
   return File("./static")


if __name__ == "__main__":
   reactor.listenUDP(9999, udpreceive)
   #reactor.listenTCP(8080, Site(webapp.resource()))
   wamppublisher.run("ws://localhost:8888", "logging")
