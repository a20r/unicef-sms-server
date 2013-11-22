
import android
import threading
import os
import smsreader as reader
import database as db
import pprint
import time

class SMSServer(reader.SMSReader):
    """
    SMS Server that receives formatted data and makes the corresponding
    HTTP requests.
    """

    def __init__(self):
        super(SMSServer, self).__init__()

    def outgoingThread(self):
        """
        Thread target that pulls data from the REST api on the server
        and broadcasts messages out to phones via SMS
        """

        while True:
            messageList = db.toSend()
            print messageList
            if messageList:
                for messageDict in messageList:
                    for number in messageDict["numbers"]:
                        # threading.Thread(
                        #     target = lambda: droid.smsSend(
                        #         number, message
                        #     )
                        # ).start()
                        self.droid.smsSend(number, messageDict["message"])
            time.sleep(3)

    def incomingThread(self):
        """
        Constantly reads the inbox for new messages and sends them to the
        server with the associated phone number for processing and storage
        """

        while True:
            if self.droid.smsGetMessageCount(True).result > 0:
                messageDict = self.readMessages()
                pprint.pprint(messageDict)
                for numberStr in messageDict:
                    db.passSMS(numberStr, messageDict[numberStr])


    def start(self):
        """
        Starts the main process
        """

        outThread = threading.Thread(target = self.outgoingThread)
        inThread = threading.Thread(target = self.incomingThread)

        outThread.start()
        inThread.start()

        #outThread.join()
        #inThread.join()

if __name__ == "__main__":
    try:
        sServer = SMSServer()
        sServer.start()
    except Exception as e:
        print e
        exit()
