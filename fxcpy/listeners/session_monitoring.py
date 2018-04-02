# The MIT License (MIT)
#
# Copyright (c) 2018 James K Bowler, Data Centauri Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from forexconnect import (
    SessionStatusListener,
    IO2GSessionStatus
)

from eventfd import EventFD
from . import Counter

from ..logger import Log
log = Log().logger

class SessionMonitoring(SessionStatusListener):
    def __init__(self, session):
        super(). __init__()
        log.debug("")
        self.reset()
        self.sessionId = ""
        self.pin = ""
        self._refcount = Counter(1)
        self._status = IO2GSessionStatus.Disconnected
        self._session = session
        self.event = EventFD()
        self._session.addRef()

    def __del__(self):
        log.debug("")
        self.event.clear()        

    def get_status(self):
        log.debug("")
        return self._status

    def set_status(self, value):
        log.debug("")
        self._status = value

    status = property(get_status, set_status)
    
    # C++ CallBack
    def addRef(self):
        #log.debug("")
        self._refcount.increment()
        ref = self._refcount.value
        return ref

    # C++ CallBack
    def release(self):
        #log.debug("")
        self._refcount.decrement()
        ref = self._refcount.value
        if self._refcount.value == 0:
            del self
        return ref
    
    # C++ CallBack
    def _on_session_status_changed(self, status):
        self._status = status
        if status == IO2GSessionStatus.Disconnected:
            self.connected = False
            self.event.set()
            log.debug("State: {}".format("Disconnected"))
        elif status == IO2GSessionStatus.Connecting:
            log.debug("State: {}".format("Connecting"))
        elif status == IO2GSessionStatus.TradingSessionRequested:
            log.debug("State: {}".format("TradingSessionRequested"))
            descriptors = self._session.getTradingSessionDescriptors();
            found = False
            if descriptors is not None:
                for i in range(descriptors.size()):
                    desc = descriptors.get(i)
                    log.warning(" id: {} name: {} description: {}".format(
                        desc.getID(), desc.getName(), desc.getDescription())
                    )
                    if self.sessionId == desc.getID:
                        found = True
                        break

            if found:
                self._session.setTradingSession(self.sessionId, self.pin)
                pass
            else:
                pass
        elif status == IO2GSessionStatus.Connected:
            self.connected = True
            self.event.set()
            
        elif status == IO2GSessionStatus.Reconnecting:            
            log.debug("State: {}".format("Reconnecting"))
        elif status == IO2GSessionStatus.Disconnecting:
            log.debug("State: {}".format("Disconnecting"))
        elif status == IO2GSessionStatus.SessionLost:
            log.debug("State: {}".format("SessionLost"))        

    # C++ CallBack
    def _on_login_failed(self, error):
        log.debug("")
        print("Login error %s" % (error))
        self.error = True

    def reset(self):
        log.debug("")
        self.connected = False
        self.error = False

    def has_error(self):
        log.debug("")
        return self.error

    def wait_events(self):
        log.debug("")
        try: return self.event.wait()
        finally: self.event.clear()

    def is_connected(self):
        log.debug("")
        return self.connected