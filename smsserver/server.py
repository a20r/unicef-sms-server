
import android
import threading
import os
import smsreader as reader
import database as db
import pprint

class SMSServer(reader.SMSReader):
    """
    SMS Server that receives formatted data and makes the corresponding
    HTTP requests.
    """

    def __init__(self):
        super(SMSServer, self).__init__()

    def outgoingThread():
        """
        Thread target that pulls data from the REST api on the server
        and broadcasts messages out to phones via SMS
        """

        while True:
            messageDict = db.toSend()
            if messageDict:
                for number in messageDict:
                    threading.Thread(
                        target = lambda: droid.smsSend(
                            number, messageDict[number]
                        )
                    ).start()

    def incomingThread():
        """
        Constantly reads the inbox for new messages and sends them to the
        server with the associated phone number for processing and storage
        """

        while True:
            if self.droid.smsGetMessageCount(True).result > 0:
                messageDict = self.readMessages()
                pprint.pprint(messageDict)
                for numberStr in messageDict:
                    db.passSMS(phoneNumber, smsString)


    def start(self):
        """
        Starts the main process
        """

        #threading.Thread(target = outgoingThread).start()
        threading.Thread(target = incomingThread).start()
        os.join()

if __name__ == "__main__":
    #test_messageReader()
    try:
        sServer = SMSServer()
        sServer.start()
    except Exception as e:
        print e
        exit()
