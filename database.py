# -*- coding: utf-8 -*-

import MySQLdb
import logging
import logging.handlers
from cons import *
import suds.client
from sslcontext import create_ssl_context, HTTPSTransport
from suds.sudsobject import asdict
import re,pyperclip


logging.handlers.TimedRotatingFileHandler(logfilename, when='h')
logging.basicConfig(filename=logfilename, format='%(asctime)s %(message)s [%(levelname)s]', level=logging.DEBUG)

def _IDRegex(PID):
    CreditRegex = re.compile(r'''((\d{1})(\s*|\-*)(\d{4})(\s*|\-*)(\d{5})(\s*|\-*)(\d{2})(\s*|\-*)(\d{1})(\s*|\-*))''',re.VERBOSE)

    text = "1234567890123"
    matches=[]

    for groups in [CreditRegex.sub(r'\2 **** \6 ** *',PID]:
        groups.rstrip()
        matches.append(groups)
    fID = str(matches.strip('[]')
    return fID

def _fetchMSG():
    sql = "SELECT * FROM nai_Send WHERE sendStatus = 0"
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()

    cursor.execute(sql)
    results = cursor.fetchall()

    return results
    
def _VerifyUser(memID):
    sql = "SELECT * FROM nai_Member WHERE memMID = \"%s\"" % memID
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()

    cursor.execute(sql)
    results = cursor.fetchone()
    logging.debug(results[5])
    logging.debug(results[6])
    logging.debug(results[7])
    logging.debug(results[8])

    if results[7]:
        if results[8]:
            return 3002
        else:
            return 3001
    else:
        sql = "UPDATE nai_Member SET memVerify = 1 WHERE memMID =\"%s\"" % memID
        try:
            cursor.execute(sql)
            connection.commit()
            return 3001
    
        except:
            connection.rollback()
            return 0

def _idCard(TIN,
            memMID):
            
    sql = "SELECT * FROM nai_Member WHERE memMID = \"%s\"" % memMID
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()

    cursor.execute(sql)
    results = cursor.fetchone()
    
    if results[7]:
        if results[8]:
            return 3002
        else:
            sslverify = False
            cafile = None
            capath = None

            kwargs = {}
            sslContext = create_ssl_context(sslverify, cafile, capath)
            kwargs['transport'] = HTTPSTransport(sslContext)
            url = 'https://rdws.rd.go.th/serviceRD3/checktinpinservice.asmx?wsdl'
            client = suds.client.Client(url, **kwargs)

            results = client.service.ServiceTIN('anonymous','anonymous', TIN)
            logging.debug(results)
        
            if results.vIsExist:
                debugmessage = "PIN = %s is exist in RD Database" % _IDRegex(TIN)
                logging.info(debugmessage)
                sql = "UPDATE nai_Member SET memVerify = 1, memNID = AES_ENCRYPT(\"%s\",\"%s\") WHERE memMID =\"%s\"" % (TIN, encKey, memMID)
                logging.debug(sql)
                
                try:
                    cursor.execute(sql)
                    connection.commit()
                    return 3005
    
                except:
                    connection.rollback()
                    return 0
            else:
                debugmessage = "PIN = %s is not exist in RD Database" % _IDRegex(TIN)
                logging.info(debugmessage)
                return 3003
    else:
        return 3004
               
         
           
    
def _sentMsg(msgID):
    sql = "UPDATE nai_Send SET sendStatus = 1, sendSent = NOW() WHERE sendID = %s" % int(msgID)
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        connection.commit()
    
    except:
        connection.rollback()
        return 2001


def _DelUser(memMid):
    sql = "DELETE FROM nai_Member WHERE memMid = \"%s\"" % memMid
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()
    try:
        
        CharSet = "set names %s;"%db[4]
        cursor.execute(CharSet)
        
        cursor.execute(sql)
        
        connection.commit()
        return 1006
    
    except:
        connection.rollback()
        return 0


def _Register(memMid,
              memDispName,
              memPassword,
              memRegisterPhase,
              LINEname,
              profileImage):
    
    debugmsg = "%s\n%s\n%s\n%s\n%s\n"%(memMid, memDispName, memPassword, memRegisterPhase, LINEname)
    logging.debug(debugmsg)
    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()


    
    try:

        sql = "SELECT * FROM nai_Member WHERE memMid =\"%s\""%memMid
        logging.debug(sql)



        cursor.execute(sql)
        data = cursor.fetchone()

        if data != None:
            debugmsg = "%s is regestered before (%s, %s)" % (memDispName, memMid, LINEname)
            logging.debug(debugmsg)
            return 1003

        try:
            memDispName.decode('ascii')
        except UnicodeDecodeError:
            debugmsg = "%s was not a ascii-encoded unicode string (%s, %s)" % (memDispName, memMid, LINEname)
            logging.debug(debugmsg)
            return 1001
        else:
            tmp = str(memDispName)
            vuser = tmp.upper()
            sql = "SELECT * FROM nai_Member WHERE UCASE(`memDispName`) = \"%s\""%vuser
            logging.debug(sql)
            cursor.execute(sql)
            results = cursor.fetchone()
            logging.debug(results)


            if results != None:
                debugmsg = "%s is alredy in use (%s, %s)" % (memDispName, memMid, LINEname)
                logging.debug(debugmsg)
                return 1002
 
        try:
            sql = "INSERT INTO nai_Member (memMid, memDispName, memPassword, memRegisterPhase, memStatus, memRegisterd, profileImage) VALUES ('%s', '%s', SHA1(\"%s\"), '%s', 1, NOW(),'%s')" % (memMid, memDispName, memPassword, memRegisterPhase, profileImage)

            CharSet = "set names %s;"%db[4]
            results = cursor.execute(CharSet)
    
            debugmsg = sql
            logging.debug(debugmsg)

            results = cursor.execute(sql)
            connection.commit()
            return 1005
        except:
            connection.rollback()
            return 1004
    
                
    finally:
        connection.close()



def _mLog(msgID,
          senderID,
          recvTime,
          mLat,
          mLon,
          mText,
          mRecv,
          status,
          mContent):
    
    text = "\"%s\"" % (mText.replace("\n","<br>"))
    sql = "INSERT INTO nai_MsgLog (msgID, senderID, recvTime, mLat, mLon, mText, mRecv, status, mContent) VALUES (%s, \"%s\", %s, %s, %s, %s, \"%s\", %s, \"%s\")"%(msgID, senderID, recvTime, mLat, mLon, text, mRecv,status, mContent)


    logging.debug(sql)

    connection = MySQLdb.connect(db[0], db[1], db[2], db[3])
    cursor = connection.cursor()
    
    try:
        
        try:
        
            CharSet = "set names %s;"%db[4]
            cursor.execute(CharSet)
            cursor.execute(sql)
            logging.debug(cursor)
            connection.commit()
            return 1
    
        except:
            connection.rollback()
            return 0

    finally:
        connection.close()
