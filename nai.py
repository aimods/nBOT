# -*- coding: utf-8 -*-

import sys
import os
import logging
import logging.handlers
import ipgetter
import random
from database import _mLog, _Register, _DelUser, _fetchMSG, _sentMsg, _VerifyUser, _idCard
from sys import exit
from time import time
from datetime import datetime
from line import LineClient, LineGroup, LineContact, LineMessage
from curve.ttypes import TalkException, ToType, OperationType, Provider, Message, ContentType
from cons import *



PID = os.getpid()


logging.handlers.TimedRotatingFileHandler(logfilename, when='h')
logging.basicConfig(filename=logfilename, format='%(asctime)s %(message)s [%(levelname)s]', level=logging.DEBUG)



pfilename = "%s/%s.pid" % ( logfolder, pidid)

if os.path.isfile(pfilename):
    errmsg =  "NAIBOT (Code name: NAI - %s) is running" % pidid
    logging.info(errmsg)
    exit(0)
else:
    pfile = open(pfilename,'w')
    pfile.write(str(PID))
    pfile.close()


try:
    if LoginMethod:
        client = LineClient(authToken=LineToken, is_mac=1, com_name="NaiBot")
    else:
        client = LineClient(LineLogin, LinePassword, is_mac=1, com_name="NaiBot")
except:
    print "Login Failed"

client.ready()





### Notify Bot Start  ###

boss = client.getContactOrRoomOrGroupById(NAIBOSS)
ext_ip = ipgetter.myip()
BotName = client.profile
#share_ip = ipgetter.IPgetter().test()
bossMsg = "NaiBot (%s) - Start from %s" % (BotName.name, ext_ip)
logging.info(bossMsg)
boss.sendMessage(bossMsg)

logging.info("Login Successful")
Token = "Token = %s"%client.authToken
logging.info(Token)

while True:

    OT = OperationType
    debug = client._debug()
    msg = ""
    t0 = ""
    loc = 0
    # status = 0
    # clat = 0
    # clon = 0
    # print debug
    if debug:
        
        def normalMsg():
            if debug.message._from:
                sender = client.getContactOrRoomOrGroupById(debug.message._from)
                created = datetime.fromtimestamp(debug.message.createdTime/1000)
                msg = debug.message.text
                t0 = client.getContactOrRoomOrGroupById(debug.message.to)
            
            if debug.message.location:
                # lat = debug.message.location.latitude
                # lon = debug.message.location.longitude
                # loc = 1
                msg =  "Location"
                inputChatlog = _mLog(debug.message.id,
                                     debug.message._from,
                                     debug.message.createdTime/1000,
                                     debug.message.location.latitude,
                                     debug.message.location.longitude,
                                     msg,
                                     debug.message.to,
                                     0,
                                     debug.message.contentType)
            
            
            if debug.message.contentType == ContentType.STICKER:
                ST = debug.message.contentMetadata
                msg = str(ST).replace("'", "\'")
                # "{'STKPKGID' : '%s','STKTXT' : '%s','STKVER' : '%s','STKID' : '%s'}" % (ST.STKPKGID, ST.STKTXT,ST.STKVER,ST.STKID)
                # status =  1
                inputChatlog = _mLog(debug.message.id,
                                     debug.message._from,
                                     debug.message.createdTime/1000,
                                     # debug.message.location.latitude,
                                     0,
                                     # debug.message.location.longitude,
                                     0,
                                     msg,
                                     debug.message.to,
                                     1,
                                     debug.message.contentType)
                logging.debug(ErrMSG[inputChatlog])
           
            if debug.message.contentType == ContentType.IMAGE:
                print debug
            
            if debug.message.contentType == 0:
                # print msg
                # print msg.count('/reg')
                # print msg.count(' ')
                # print msg.split(' ')
                if msg.count('+') == 3:
                    vMsg = []
                    vMsg = msg.split('+')
                    if vMsg[0] == "TTL":
                        filename = "%s/%s"%(logfolder,vMsg[1])
                        file = open(filename,'w')   # Trying to create a new file or open one
                        file.close()
                        debugmsg = "File %s Created - %s (%s)"%(filename,vMsg[2],msg)
                        logging.debug(debugmsg)

                elif msg.count('/reg') != 0:
                    vMsg = msg.split(' ')
                    # print vMsg
                    if vMsg[0] == '/reg':
                        LLNAME = client.getContactOrRoomOrGroupById(debug.message._from)

                        if len(vMsg) !=3:
                            LLNAME.sendMessage(ReREGIS)
                            return 0
                        
                        lName = vMsg[1]
                        lID = debug.message._from
                        lPass = vMsg[2]
                        lphase = msg
                        pPicURL = LLNAME.profileImage
                        
                        regLog = _Register(lID, lName, lPass, lphase, LLNAME.name,pPicURL)
                        logging.debug(regLog)
                        if regLog > 1:
                            LLNAME.sendMessage(ErrMSG[regLog])

                elif msg.count('/bye') != 0:
                    delUser = _DelUser(debug.message._from)
                    LLNAME = client.getContactOrRoomOrGroupById(debug.message._from)
                    
                    if delUser > 0:
                        LLNAME.sendMessage(ErrMSG[delUser])

                elif msg.upper() == "CHECK":
                    debugmsg = "%s sent %s" %(sender,msg)
                    logging.info(debugmsg)
                    
                elif msg.count('/verify') !=0:
                    vUser = _VerifyUser(debug.message._from)
                    logging.debug(vUser)
                    
                    sender.sendMessage(ErrMSG[vUser])
                    debugmsg = "%s - %s" % (sender, ErrMSG[vUser])
                    logging.debug(debugmsg)
                
                elif msg.count('/id') != 0:
                    vMsg = msg.split(' ')
                    
                    if len(vMsg[1]) != 13:
                        sender.sendMessage(ErrMSG[3001])
                        logging.debug(vMsg[1])
                    else:
                        vTIN = _idCard(vMsg[1], debug.message._from)
                        logging.debug(vTIN)
                        
                        sender.sendMessage(ErrMSG[vTIN])
                        
                         
                    

                else:
                    inputChatlog = _mLog(debug.message.id,
                                         debug.message._from,
                                         debug.message.createdTime/1000,
                                         0,
                                         0,
                                         msg,
                                         debug.message.to,
                                         0,
                                         debug.message.contentType)
                    logging.debug(ErrMSG[inputChatlog])
        
        
        # print "at  %s - %s to %s\n \"%s\"" % (created, sender, t0, msg)
        # print inputChatlog
        
        
        _ACTION = {
            #4: "ADD_CONTACT",
            #5: "NOTIFIED_ADD_CONTACT",
            #6: "BLOCK_CONTACT",
            #7: "UNBLOCK_CONTACT",
            #12: "INVITE_INTO_GROUP",
            #13: inviteToGroup,
            #31: "CANCEL_INVITATION_GROUP",
            #32: "NOTIFIED_CANCEL_INVITATION_GROUP",
            #14: "LEAVE_GROUP",
            #15: "NOTIFIED_LEAVE_GROUP",
            #16: "ACCEPT_GROUP_INVITATION",
            #17: "NOTIFIED_ACCEPT_GROUP_INVITATION",
            #34: "REJECT_GROUP_INVITATION",
            #35: "NOTIFIED_REJECT_GROUP_INVITATION",
            #18: "KICKOUT_FROM_GROUP",
            #19: "NOTIFIED_KICKOUT_FROM_GROUP",
            #20: "CREATE_ROOM",
            #21: "INVITE_INTO_ROOM",
            #22: "NOTIFIED_INVITE_INTO_ROOM",
            #23: "LEAVE_ROOM",
            #24: "NOTIFIED_LEAVE_ROOM",
            #25: "SEND_MESSAGE",
            26: normalMsg,
            #27: "SEND_MESSAGE_RECEIPT",
            #28: "RECEIVE_MESSAGE_RECEIPT",
            #29: "SEND_CONTENT_RECEIPT",
            #40: "SEND_CHAT_CHECKED",
            #41: "SEND_CHAT_REMOVED",
            #54: "FAILED_SEND_MESSAGE",
            #55: "NOTIFIED_READ_MESSAGE",
        }
        
        
        if debug.type in _ACTION.keys():
            if debug.message._from != "u085311ecd9e3e3d74ae4c9f5437cbcb5":
                _ACTION[debug.type]()
            else:
                debugmsg = "LINE said '%s'" % debug.message.text
                logging.info(debugmsg)

        for list in _fetchMSG():
            if list[1] == 0:
                SendTo = client.getContactOrRoomOrGroupById(list[2])
                msg = list[3]
        
                if list[5] != None:
                    if list[5] < datetime.now():
                        debugmsg = "Schedule MSG ID %s sent at %s" % (list[0],datetime.now())
                        logging.info(debugmsg)
                        sSend = SendTo.sendMessage(msg)
                        action = _sentMsg(list[0])
                        if action == 2001:
                            debugmsg = "%s \nID = %s \nTime = %s"%(ErrMSG[action],list[0],datetime.now())
                            logging.warning(debugmsg)
                            boss.sendMessage(debugmsg)
    
                else:
                    debugmsg = "MSG ID %s sent at %s" % (list[0],datetime.now())
                    logging.info(debugmsg)
                    sSend = SendTo.sendMessage(msg)
                    action = _sentMsg(list[0])
                    if action == 2001:
                        debugmsg = "%s \nID = %s \nTime = %s"%(ErrMSG[action],list[0],datetime.now())
                        logging.warning(debugmsg)
                        boss.sendMessage(debugmsg)
                    
    client.ready()

