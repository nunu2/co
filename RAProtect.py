from LINEPY import *
from akad.ttypes import *
import time, asyncio, json, threading, codecs, sys, os, re, urllib, requests, wikipedia, html5lib, timeit, pafy, youtube_dl
from bs4 import BeautifulSoup
mulai = time.time()

RASadmin = ["mid"]
RAKey    = "ra "
 
def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '%02d Hari %02d Jam %02d Menit %02d Detik' % (days, hours, mins, secs)
    
class LineBot(object):
    
    def __init__(self, resp, authQR=None):
        self.resp = resp
        self.resp = self.resp+' '
        self.authQR = authQR
        self.login(authQR)
        self.fetch()
        
    def login(self, auth):
        if auth == None:
            self.client = LINE()
        else:
            self.client = LINE(idOrAuthToken=auth)
        self.client.log("Auth Token : " + str(self.client.authToken))
        self.mid = self.client.getProfile().mid
        akun = open('RAwait.json','r')
        self.wait = json.load(akun)
        setting = open('RAset.json','r')
        self.RAset = json.load(setting)
        
    def fetch(self):
        while True:
            try:
                self.operations = self.client.poll.fetchOperations(self.client.revision, 10)
                for op in self.operations:
                    if (op.type != OpType.END_OF_OPERATION):
                        self.client.revision = max(self.client.revision, op.revision)
                        self.bot(op)
            except Exception:
                pass
        
    def bot(self, op):
        cl = self.client
        wait = self.wait
        try:
            if op.type == 0:
                return
            
            if op.type == 11:
                if op.param1 in self.RAset["RAprotqr"]:
                    if cl.getGroup(op.param1).preventedJoinByTicket == False:
                        if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                            cl.reissueGroupTicket(op.param1)
                            X = cl.getGroup(op.param1)
                            X.preventedJoinByTicket = True
                            cl.updateGroup(X)
                            
                if op.param2 in self.wait["RAblacklist"]:
                    if cl.getGroup(op.param1).preventedJoinByTicket == False:
                        if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                            cl.reissueGroupTicket(op.param1)
                            X = cl.getGroup(op.param1)
                            X.preventedJoinByTicket = True
                            cl.updateGroup(X)
                            cl.kickoutFromGroup(op.param1,[op.param2])
            
            if op.type == 13:
                if self.mid in op.param3:
                    if self.wait["RAautojoin"] == True:
                        if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RABots"]:
                            cl.acceptGroupInvitation(op.param1)
                            cl.sendText(op.param1,"bye! \n " +str(cl.getGroup(op.param1).name))
                            cl.leaveGroup(op.param1)
                        else:
                            cl.acceptGroupInvitation(op.param1)
            
            if op.type == 13:
                if op.param2 in self.wait["RAblacklist"]:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    
                if op.param1 in self.RAset["RAprotinvite"]:
                    if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                        group = cl.getGroup(op.param1)    
                        cl.cancelGroupInvitation(op.param1,[op.param3])
                            
                        
                if op.param3 in self.wait["RAblacklist"]:
                    group = cl.getGroup(op.param1)
                        if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                            cl.cancelGroupInvitation(op.param1,[op.param3])
                            self.wait["RAblacklist"][op.param2] = True
                            f=codecs.open('RAwait.json','w','utf-8')
                            json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                            cl.kickoutFromGroup(op.param1,[op.param2])
                
            if op.type == 17:
                if op.param2 in self.wait["RAblacklist"]:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    
                if op.param1 in self.RAset["RAgreet"]:
                    if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                        if cl.getContact(op.param2).videoProfile != None:
                            cl.sendVideoWithURL(op.param1, "http://dl.profile.line.naver.jp/"+cl.getContact(op.param2).pictureStatus+"/vp.small")
                            cl.sendText(op.param1," "+str(cl.getContact(op.param2).displayName)+"\n\n"+str(self.wait["RAmessage"][op.param1]["Pesan"]))
                        else:
                            cl.sendImageWithURL(op.param1,"http://dl.profile.line.naver.jp/{}".format(str(cl.getContact(op.param2).pictureStatus)))
                            cl.sendText(op.param1," "+str(cl.getContact(op.param2).displayName)+"\n\n"+str(self.wait["RAmessage"][op.param1]["Pesan"]))
                        
            
            if op.type == 19:
                if op.param1 in self.RAset["RAprotkick"]:
                    if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                        self.wait["RAblacklist"][op.param2] = True
                        f=codecs.open('RAwait.json','w','utf-8')
                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                        try:
                            cl.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            pass
                
                if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"] and op.param3 in RASadmin:
                    self.wait["RAblacklist"][op.param2] = True
                    f=codecs.open('RAwait.json','w','utf-8')
                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                    
                if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"] and op.param3 in self.wait["RAAdmin"]:
                    self.wait["RAblacklist"][op.param2] = True
                    f=codecs.open('RAwait.json','w','utf-8')
                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                    
                if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"] and op.param3 in self.wait["RAStaff"]:
                    self.wait["RAblacklist"][op.param2] = True
                    f=codecs.open('RAwait.json','w','utf-8')
                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    cl.inviteIntoGroup(op.param1,[op.param3])
                    
            if op.type == 19:
                if op.param3 in self.wait["RABots"]:
                    cl.inviteIntoGroup(op.param1,[op.param3])
                    if op.param2 not in RASadmin and op.param2 not in self.wait["RAAdmin"] and op.param2 not in self.wait["RAStaff"] and op.param2 not in self.wait["RABots"]:
                        self.wait["RAblacklist"][op.param2] = True
                        f=codecs.open('RAwait.json','w','utf-8')
                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                        cl.kickoutFromGroup(op.param1,[op.param2])
            
            if op.type == 32:
                if op.param1 in self.RAset["RAprotcancel"]:
                    if op.param2 not in RASadmin or op.param2 not in self.wait["RAAdmin"] or op.param2 not in self.wait["RAStaff"] or op.param2 not in self.wait["RABots"]:
                        cl.kickoutFromGroup(op.param1,[op.param2])
                        self.wait["RAblacklist"][op.param2] = True
                        f=codecs.open('RAwait.json','w','utf-8')
                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                        try:
                            if op.param3 not in self.wait["RAblacklist"]:
                                cl.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            if op.param3 not in self.wait["RAblacklist"]:
                                cl.inviteIntoGroup(op.param1,[op.param3])
            
            if op.type == 46:
                if op.param2 in self.wait["RABots"]:
                    cl.removeAllMessages()
                
            if op.type == 55:
                if op.param1 in self.RAset["RAreadPoint"]:
                    if op.param2 in self.RAset["RAreadMember"][op.param1]:
                        pass
                    else:
                        self.RAset["RAreadMember"][op.param1][op.param2] = True
                else:
                    pass
            
            if op.type == 26:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 2:
                    if msg.toType == 0:
                        to = sender
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 13:
                        if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                            if msg.to in self.wait["RAwblacklist"]:
                                if msg.contentMetadata["mid"] in self.wait["RAblacklist"]:
                                    cl.sendText(msg.to,"Terblacklist")
                                else:
                                    self.wait["RAblacklist"][msg.contentMetadata["mid"]] = True
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Akun terblacklist")
                                    
                            elif msg.to in self.wait["RAdblacklist"]:
                                if msg.contentMetadata["mid"] in self.wait["RAblacklist"]:
                                    del self.wait["RAblacklist"][msg.contentMetadata["mid"]]
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Terhapus dari blacklist")
                                else:
                                    cl.sendText(msg.to,"Akun tidak ada di blacklist")
                            elif msg.to in self.wait["RAautoscan"]:
                                msg.contentType = 0
                                cl.sendText(msg.to,msg.contentMetadata["mid"])
                            
                        if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                            if msg.to in self.wait["RASadmin"]:
                                if msg.contentMetadata["mid"] in self.wait["RAAdmin"]:
                                    cl.sendText(msg.to,"Telah menjadi admin")
                                else:
                                    self.wait["RAAdmin"][msg.contentMetadata["mid"]] = True
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Terdaftar admin")
                            elif msg.to in self.wait["RASDadmin"]:
                                if msg.contentMetadata["mid"] in self.wait["RAAdmin"]:
                                    del self.wait["RAAdmin"][msg.contentMetadata["mid"]]
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Terhapus dari admin")
                                else:
                                    cl.sendText(msg.to,"Tidak ada di adminlist")
                            elif msg.to in self.wait["RASstaff"]:
                                if msg.contentMetadata["mid"] in self.wait["RAStaff"]:
                                    cl.sendText(msg.to,"Telah menjadi staff")
                                else:
                                    self.wait["RAStaff"][msg.contentMetadata["mid"]] = True
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Terdaftar staff")
                            elif msg.to in self.wait["RASDstaff"]:
                                if msg.contentMetadata["mid"] in self.wait["RAStaff"]:
                                    del self.wait["RAStaff"][msg.contentMetadata["mid"]]
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Terhapus dari staff")
                                else:
                                    cl.sendText(msg.to,"Tidak ada di stafflist")
                                
                        if msg._from in RASadmin:
                            if msg.to in self.wait["RASbot"]:
                                if msg.contentMetadata["mid"] in self.wait["RABots"]:
                                    cl.sendText(msg.to,"Bot sudah terdaftar")
                                else:
                                    self.wait["RABots"][msg.contentMetadata["mid"]] = True
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Bot Terdaftar")
                            elif msg.to in self.wait["RASDbot"]:
                                if msg.contentMetadata["mid"] in self.wait["RABots"]:
                                    del self.wait["RABots"][msg.contentMetadata["mid"]]
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Bot terhapus")
                                else:
                                    cl.sendText(msg.to,"Bot tidak ada di list")
                    
                    elif msg.contentType == 1:
                        if msg._from in RASadmin:
                            if self.mid in self.RAset["RAfoto"]:
                                path = cl.downloadObjectMsg(msg_id)
                                del self.RAset["RAfoto"][self.mid]
                                cl.updateProfilePicture(path)
                                cl.sendMessage(msg.to,"Foto berhasil dirubah")
                            elif msg.to in self.RAset["RAfoto"]:
                                path = cl.downloadObjectMsg(msg_id)
                                cl.updateProfilePicture(path)
                                del self.RAset["RAfoto"][msg.to]
                                cl.sendMessage(msg.to,"Foto berhasil diperbaharui")
                            if msg.toType == 2:
                                if msg.to in self.RAset["RAGfoto"]:
                                    path = cl.downloadObjectMsg(msg_id)
                                    del self.RAset["RAGfoto"][msg.to]
                                    cl.updateGroupPicture(msg.to, path)
                                    cl.sendMessage(msg.to,"Foto grup diperbaharui")
                                    
                    elif msg.contentType == 0:
                        if msg.to in self.wait["RAautoread"]:
                            cl.sendChatChecked(msg.to,msg_id)
                        if text is None:
                            return
                        else:
                
     #------------------------------- Start Menu ------------------------------#

                            if msg.text == self.resp + 'msamenu':
                                if msg._from in RASadmin:
                                    md = "🔰 RAFAMILY Protection\n\n"
                                    md += "🔰" +RAKey+ " absen\n"
                                    md += "🔰" +RAKey+ " spbot\n"
                                    md += "🔰" +RAKey+ " cname 「text」\n"
                                    md += "🔰" +RAKey+ " cbio 「text」\n"
                                    md += "🔰" +RAKey+ " cfoto\n"
                                    md += "🔰" +RAKey+ " cleanblacklist\n"
                                    md += "🔰" +RAKey+ " byeall\n"
                                    md += "🔰" +RAKey+ " leaveall\n"
                                    md += "🔰" +RAKey+ " cleanmember\n"
                                    md += "🔰" +RAKey+ " restart\n"
                                    md += "🔰" +RAKey+ " masuksemua\n"
                                    md += "🔰" +RAKey+ " removechat\n"
                                    md += "🔰" +RAKey+ " leave「namagroup」\n"
                                    md += "🔰" +RAKey+ " scblack 「on/off」\n"
                                    md += "🔰" +RAKey+ " scublack 「on/off」\n"
                                    md += "🔰" +RAKey+ " scadmin 「on/off」\n"
                                    md += "🔰" +RAKey+ " scuadmin 「on/off」\n"
                                    md += "🔰" +RAKey+ " scstaff 「on/off」\n"
                                    md += "🔰" +RAKey+ " scustaff 「on/off」\n"
                                    md += "🔰" +RAKey+ " autoread 「on/off」\n"
                                    md += "🔰" +RAKey+ " ngebot 「on/off」\n"
                                    md += "🔰" +RAKey+ " buangbot 「on/off」\n"
                                    md += "🔰" +RAKey+ "「block/allow」invite\n"
                                    md += "🔰" +RAKey+ "「block/allow」ourl\n"
                                    md += "🔰" +RAKey+ "「block/allow」cancel\n"
                                    md += "🔰" +RAKey+ "「block/allow」kick\n"
                                    md += "🔰" +RAKey+ "「block/allow」semua\n"
                                    md += "🔰" +RAKey+ " bl「@」\n"
                                    md += "🔰" +RAKey+ " ubl「@」\n"
                                    md += "🔰" +RAKey+ " adadd「@」\n"
                                    md += "🔰" +RAKey+ " addell「@」\n"
                                    md += "🔰" +RAKey+ " stadd「@」\n"
                                    md += "🔰" +RAKey+ " stdell「@」\n"
                                    md += "🔰" +RAKey+ " nganubot「@」\n"
                                    md += "🔰" +RAKey+ " cuekinbot「@」\n"
                                    md += "Fungsi Diatas untuk semua Bot"
                                    md += "\n\n"
                                    md += "🔰" +self.resp+ " pengaturan\n"
                                    md += "🔰" +self.resp+ " cekmid「on/off」\n"
                                    md += "🔰" +self.resp+ "「allow/block」greet\n"
                                    md += "🔰" +self.resp+ " ourl / curl\n"
                                    md += "🔰" +self.resp+ " informasi\n"
                                    md += "🔰" +self.resp+ " listgroup\n"
                                    md += "🔰" +self.resp+ " cname「text」\n"
                                    md += "🔰" +self.resp+ " cbio「text」\n"
                                    md += "🔰" +self.resp+ " cfoto\n"
                                    md += "🔰" +self.resp+ " cfotogroup\n"
                                    md += "🔰" +self.resp+ " bc「text」\n"
                                    md += "🔰" +self.resp+ " kick「@」\n"
                                    md += "🔰" +self.resp+ " listbl\n"
                                    md += "🔰" +self.resp+ " listteam\n"
                                    md += "🔰" +self.resp+ " listbot\n"
                                    md += "🔰" +self.resp+ " liststatus\n"
                                    md += "Fungsi Diatas untuk inisial Bot"
                                    cl.sendText(msg.to,md)
                                    
                            elif msg.text == self.resp + 'mamenu':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    md = "🔰 RAFAMILY Admin Protection\n\n"
                                    md += "🔰" +RAKey+ " absen\n"
                                    md += "🔰" +RAKey+ " spbot\n"
                                    md += "🔰" +RAKey+ " cleanblacklist\n"
                                    md += "🔰" +RAKey+ " byeall\n"
                                    md += "🔰" +RAKey+ " scblack 「on/off」\n"
                                    md += "🔰" +RAKey+ " scublack 「on/off」\n"
                                    md += "🔰" +RAKey+ " scstaff 「on/off」\n"
                                    md += "🔰" +RAKey+ " scustaff 「on/off」\n"
                                    md += "🔰" +RAKey+ "「block/allow」invite\n"
                                    md += "🔰" +RAKey+ "「block/allow」ourl\n"
                                    md += "🔰" +RAKey+ "「block/allow」cancel\n"
                                    md += "🔰" +RAKey+ "「block/allow」kick\n"
                                    md += "🔰" +RAKey+ "「block/allow」semua\n"
                                    md += "🔰" +RAKey+ " bl「@」\n"
                                    md += "🔰" +RAKey+ " ubl「@」\n"
                                    md += "🔰" +RAKey+ " stadd「@」\n"
                                    md += "🔰" +RAKey+ " stdell「@」\n"
                                    md += "Fungsi Diatas untuk semua Bot"
                                    md += "\n\n"
                                    md += "🔰" +self.resp+ " pengaturan\n"
                                    md += "🔰" +self.resp+ " cekmid「on/off」\n"
                                    md += "🔰" +self.resp+ "「allow/block」greet\n"
                                    md += "🔰" +self.resp+ " ourl / curl\n"
                                    md += "🔰" +self.resp+ " informasi\n"
                                    md += "🔰" +self.resp+ " listgroup\n"
                                    md += "🔰" +self.resp+ " listidgroup\n"
                                    md += "🔰" +self.resp+ " cfotogroup\n"
                                    md += "🔰" +self.resp+ " bc「text」\n"
                                    md += "🔰" +self.resp+ " kick「@」\n"
                                    md += "🔰" +self.resp+ " listbl\n"
                                    md += "🔰" +self.resp+ " listteam\n"
                                    md += "🔰" +self.resp+ " listbot\n"
                                    md += "🔰" +self.resp+ " liststatus\n"
                                    md += "🔰" +self.resp+ " sprespon\n"
                                    cl.sendText(msg.to,md)
                                    
                            elif msg.text == self.resp + 'msmenu':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    md = "🔰 RAFAMILY Staff Protection\n\n"
                                    md += "🔰" +RAKey+ " absen\n"
                                    md += "🔰" +RAKey+ " spbot\n"
                                    md += "🔰" +RAKey+ " byeall\n"
                                    md += "🔰" +RAKey+ " cleanblacklist\n"
                                    md += "🔰" +RAKey+ " scblack 「on/off」\n"
                                    md += "🔰" +RAKey+ " scublack 「on/off」\n"
                                    md += "🔰" +RAKey+ "「block/allow」invite\n"
                                    md += "🔰" +RAKey+ "「block/allow」ourl\n"
                                    md += "🔰" +RAKey+ "「block/allow」cancel\n"
                                    md += "🔰" +RAKey+ "「block/allow」kick\n"
                                    md += "🔰" +RAKey+ "「block/allow」semua\n"
                                    md += "🔰" +RAKey+ " bl「@」\n"
                                    md += "🔰" +RAKey+ " ubl「@」\n"
                                    md += "Fungsi Diatas untuk semua Bot"
                                    md += "\n\n"
                                    md += "🔰" +self.resp+ " pengaturan\n"
                                    md += "🔰" +self.resp+ " cekmid「on/off」\n"
                                    md += "🔰" +self.resp+ "「allow/block」greet\n"
                                    md += "🔰" +self.resp+ " ourl / curl\n"
                                    md += "🔰" +self.resp+ " informasi\n"
                                    md += "🔰" +self.resp+ " listgroup\n"
                                    md += "🔰" +self.resp+ " kick「@」\n"
                                    md += "🔰" +self.resp+ " listbl\n"
                                    md += "🔰" +self.resp+ " listteam\n"
                                    md += "🔰" +self.resp+ " listbot\n"
                                    md += "🔰" +self.resp+ " sprespon\n"
                                    cl.sendText(msg.to,md)
                                    
                                    
                            elif msg.text == self.resp + 'pengaturan':
                                if msg._from in RASadmin:
                                    md = "Group {}\n\n".format(str(cl.getGroup(msg.to).name))
                                    if msg.to in self.wait["RASadmin"]: md+="✅ Add Admin\n"
                                    else: md+="❎ Add Admin\n"
                                    if msg.to in self.wait["RASDadmin"]: md+="✅ Dell Admin\n"
                                    else: md+="❎ Dell Admin\n"
                                    if msg.to in self.wait["RASstaff"]: md+="✅ Add Staff\n"
                                    else: md+="❎ Add Staff\n"
                                    if msg.to in self.wait["RASDstaff"] == True: md+="✅ Dell Staff\n"
                                    else: md+="❎ Dell Staff\n"
                                    if msg.to in self.wait["RAwblacklist"]: md+="✅ Blacklist\n"
                                    else: md+="❎ Blacklist\n"
                                    if msg.to in self.wait["RAdblacklist"]: md+="✅ Unblacklist\n"
                                    else: md+="❎ Unblacklist\n"
                                    if msg.to in self.wait["RAautoscan"]: md+="✅ Cek mid\n"
                                    else: md+="❎ Cek mid\n"
                                    if msg.to in self.wait["RASbot"]: md+="✅ Tambahbot\n"
                                    else: md+="❎ Tambahbot\n"
                                    if msg.to in self.wait["RASDbot"]: md+="✅ Buangbot\n"
                                    else: md+="❎ Buangbot\n"
                                    if self.wait["RAautojoin"] == True: md+="✅ Auto Join\n"
                                    else: md+="❎ Auto Join\n"
                                    if msg.to in self.wait["RAautoread"]: md+="✅ Autoread\n"
                                    else: md+="❎ Autoread\n"
                                    if msg.to in self.RAset["RAprotinvite"]: md+="✅ Block inivte\n"
                                    else: md+="❎ Block invite\n"
                                    if msg.to in self.RAset["RAprotqr"]: md+="✅ Block ourl \n"
                                    else: md+="❎ Block ourl\n"
                                    if msg.to in self.RAset["RAprotkick"]: md+="✅ Block kick member \n"
                                    else: md+="❎ Block kick member off\n" 
                                    if msg.to in self.RAset["RAprotcancel"]: md+="✅ Block cancel member \n"
                                    else: md+="❎ Block cancel member off\n"
                                    if msg.to in self.RAset["RAgreet"]: md+="✅ Greet Message \n"
                                    else: md+="❎ Greet off\n"
                                    cl.sendText(msg.to,md)
                                    
                                if msg._from in self.wait["RAAdmin"]:
                                    if msg.to in self.wait["RASstaff"]: md+="✅ Add Staff\n"
                                    else: md+="❎ Add Staff\n"
                                    if msg.to in self.wait["RASDstaff"] == True: md+="✅ Dell Staff\n"
                                    else: md+="❎ Dell Staff\n"
                                    if msg.to in self.wait["RAwblacklist"]: md+="✅ Blacklist\n"
                                    else: md+="❎ Blacklist\n"
                                    if msg.to in self.wait["RAdblacklist"]: md+="✅ Unblacklist\n"
                                    else: md+="❎ Unblacklist\n"
                                    if msg.to in self.wait["RAautoscan"]: md+="✅ Cek mid\n"
                                    else: md+="❎ Cek mid\n"
                                    if self.wait["RAautojoin"] == True: md+="✅ Auto Join\n"
                                    else: md+="❎ Auto Join\n"
                                    if msg.to in self.wait["RAautoread"]: md+="✅ Autoread\n"
                                    else: md+="❎ Autoread\n"
                                    if msg.to in self.RAset["RAprotinvite"]: md+="✅ Block inivte\n"
                                    else: md+="❎ Block invite\n"
                                    if msg.to in self.RAset["RAprotqr"]: md+="✅ Block ourl \n"
                                    else: md+="❎ Block ourl\n"
                                    if msg.to in self.RAset["RAprotkick"]: md+="✅ Block kick member \n"
                                    else: md+="❎ Block kick member off\n" 
                                    if msg.to in self.RAset["RAprotcancel"]: md+="✅ Block cancel member \n"
                                    else: md+="❎ Block cancel member off\n"
                                    if msg.to in self.RAset["RAgreet"]: md+="✅ Greet Message \n"
                                    else: md+="❎ Greet off\n"
                                    cl.sendText(msg.to,md)
                                    
                                if msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.wait["RAwblacklist"]: md+="✅ Blacklist\n"
                                    else: md+="❎ Blacklist\n"
                                    if msg.to in self.wait["RAdblacklist"]: md+="✅ Unblacklist\n"
                                    else: md+="❎ Unblacklist\n"
                                    if msg.to in self.wait["RAautoscan"]: md+="✅ Cek mid\n"
                                    else: md+="❎ Cek mid\n"
                                    if self.wait["RAautojoin"] == True: md+="✅ Auto Join\n"
                                    else: md+="❎ Auto Join\n"
                                    if msg.to in self.wait["RAautoread"]: md+="✅ Autoread\n"
                                    else: md+="❎ Autoread\n"
                                    if msg.to in self.RAset["RAprotinvite"]: md+="✅ Block inivte\n"
                                    else: md+="❎ Block invite\n"
                                    if msg.to in self.RAset["RAprotqr"]: md+="✅ Block ourl \n"
                                    else: md+="❎ Block ourl\n"
                                    if msg.to in self.RAset["RAprotkick"]: md+="✅ Block kick member \n"
                                    else: md+="❎ Block kick member off\n" 
                                    if msg.to in self.RAset["RAprotcancel"]: md+="✅ Block cancel member \n"
                                    else: md+="❎ Block cancel member off\n"
                                    if msg.to in self.RAset["RAgreet"]: md+="✅ Greet Message \n"
                                    else: md+="❎ Greet off\n"
                                    cl.sendText(msg.to,md)
                                        
                            elif msg.text == RAKey + "scblack on":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.wait["RAwblacklist"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RAwblacklist"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk blacklist")
                            
                            elif msg.text == RAKey + "scblack off":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.wait["RAwblacklist"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RAwblacklist"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Blacklist nonaktif")
                            
                            elif msg.text == RAKey + "scublack on":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.wait["RAdblacklist"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RAdblacklist"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk ubblacklist")
                            
                            elif msg.text == RAKey + "scublack off":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.wait["RAdblacklist"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RAdblacklist"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Unblacklist nonaktif")
                                        
                            elif msg.text == RAKey + "scadmin on":
                                if msg._from in RASadmin:
                                    if msg.to in self.wait["RASadmin"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASadmin"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk tambah admin")
                            
                            elif msg.text == RAKey + "scadmin off":
                                if msg._from in RASadmin:
                                    if msg.to not in self.wait["RASadmin"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASadmin"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Tambah admin nonaktif")
                            
                            elif msg.text == RAKey + "scuadmin on":
                                if msg._from in RASadmin:
                                    if msg.to in self.wait["RASDadmin"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASDadmin"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk hapus admin")
                            
                            elif msg.text == RAKey + "scuadmin off":
                                if msg._from in RASadmin:
                                    if msg.to not in self.wait["RASDadmin"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASDadmin"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Hapus admin nonaktif")
                            
                            
                            elif msg.text == RAKey + "scstaff on":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    if msg.to in self.wait["RASstaff"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASstaff"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk tambah staff")
                            
                            elif msg.text == RAKey + "scstaff off":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    if msg.to not in self.wait["RASstaff"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASstaff"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Tambah staff nonaktif")
                                        
                            elif msg.text == RAKey + "scustaff on":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    if msg.to in self.wait["RASDstaff"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASDstaff"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak untuk hapus staff")
                            
                            elif msg.text == RAKey + "scustaff off":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    if msg.to not in self.wait["RASDstaff"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASDstaff"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Hapus staff nonaktif")
                            
                            elif msg.text == RAKey + "autoread on":
                                if msg._from in RASadmin:
                                    if msg.to in self.wait["RAautoread"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RAautoread"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Autoread aktif")
                            
                            elif msg.text == RAKey + "autoread off":
                                if msg._from in RASadmin:
                                    if msg.to not in self.wait["RAautoread"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RAautoread"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Autoread nonaktif")
                            
                            elif msg.text == self.resp + "cekmid on":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.wait["RAautoscan"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RAautoscan"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Cekmid aktif")
                            
                            elif msg.text == self.resp + "cekmid off":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.wait["RAautoscan"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RAautoscan"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Cekmid nonaktif")
                            
                            elif msg.text == RAKey + "ngebot on":
                                if msg._from in RASadmin:
                                    if msg.to in self.wait["RASbot"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASbot"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak tambah bot")
                            
                            elif msg.text == RAKey + "ngebot off":
                                if msg._from in RASadmin:
                                    if msg.to not in self.wait["RASbot"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASbot"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Tambah bot nonaktif")         
                    
                            elif msg.text == RAKey + "buangbot on":
                                if msg._from in RASadmin:
                                    if msg.to in self.wait["RASDbot"]:
                                        cl.sendText(msg.to, "Sudah aktif")
                                    else:
                                        self.wait["RASDbot"][msg.to] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Kirim kontak buang bot")
                            
                            elif msg.text == RAKey + "buangbot off":
                                if msg._from in RASadmin:
                                    if msg.to not in self.wait["RASDbot"]:
                                        cl.sendText(msg.to, "Belum aktif")
                                    else:
                                        del self.wait["RASDbot"][msg.to]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Buang bot nonaktif")
                                        
                            elif msg.text == RAKey + "block invite":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.RAset["RAprotinvite"]:
                                        cl.sendText(msg.to,"Block invite sudah diamankan")
                                    else:
                                        self.RAset["RAprotinvite"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block invite telah di tutup")
                            
                            elif msg.text == RAKey + "allow invite":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAprotinvite"]:
                                        cl.sendText(msg.to,"Block invite belum diamankan")
                                    else:
                                        del self.RAset["RAprotinvite"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block invite telah di buka")
                            
                            elif msg.text == RAKey + "block ourl":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.RAset["RAprotqr"]:
                                        cl.sendText(msg.to,"Block ourl sudah diamankan")
                                    else:
                                        self.RAset["RAprotqr"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block ourl telah di tutup")
                            
                            elif msg.text == RAKey + "allow ourl":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAprotqr"]:
                                        cl.sendText(msg.to,"Block ourl belum diamankan")
                                    else:
                                        del self.RAset["RAprotqr"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block ourl telah di buka")
                            
                            elif msg.text == RAKey + "block cancel":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.RAset["RAprotcancel"]:
                                        cl.sendText(msg.to,"Block cancel sudah diamankan")
                                    else:
                                        self.RAset["RAprotcancel"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block cancel telah di tutup")
                                        
                            elif msg.text == RAKey + "allow cancel":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAprotcancel"]:
                                        cl.sendText(msg.to,"Block cancel belum diamankan")
                                    else:
                                        del self.RAset["RAprotcancel"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block cancel telah di buka")
                            
                            elif msg.text == RAKey + "block kick":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.RAset["RAprotkick"]:
                                        cl.sendText(msg.to,"Block kick sudah diamankan")
                                    else:
                                        self.RAset["RAprotkick"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block kick telah di tutup")
                            
                            elif msg.text == RAKey + "allow kick":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAprotkick"]:
                                        cl.sendText(msg.to,"Block kick belum diamankan")
                                    else:
                                        del self.RAset["RAprotkick"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Block kick telah di buka")
                                        
                            elif msg.text == RAKey + "block semua":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to in self.RAset["RAprotqr"] or msg.to in self.RAset["RAprotcancel"] or msg.to in self.RAset["RAprotkick"]:
                                        cl.sendText(msg.to,"Group sudah diamankan")
                                    else:
                                        self.RAset["RAprotinvite"][msg.to] = True
                                        self.RAset["RAprotqr"][msg.to] = True
                                        self.RAset["RAprotcancel"][msg.to] = True
                                        self.RAset["RAprotkick"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Akses telah di tutup")
                            
                            elif msg.text == RAKey + "allow semua":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAprotqr"] or msg.to not in self.RAset["RAprotcancel"] or msg.to not in self.RAset["RAprotkick"]:
                                        cl.sendText(msg.to,"Group belum diamankan")
                                    else:
                                        #del self.RAset["RAprotinvite"][msg.to]
                                        del self.RAset["RAprotqr"][msg.to]
                                        del self.RAset["RAprotcancel"][msg.to]
                                        del self.RAset["RAprotkick"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Akses telah di buka")            
                            
                            elif msg.text == self.resp + "allow greet":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.wait["RAmessage"]:
                                        cl.sendText(msg.to,"Maaf "+str(cl.getContact(msg._from).displayName)+"\n\nsilahkan atur dahulu pesan pembukanya menggunakan\n\n"+self.resp+"cwelcome isi pesanya")
                                    else:
                                        self.RAset["RAgreet"][msg.to] = True
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Pesan sambutan diaktifkan")
                            
                            elif msg.text == self.resp + "block greet":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.to not in self.RAset["RAgreet"]:
                                        cl.sendText(msg.to,"Pesan sambutan tidak aktif")
                                    else:
                                        del self.RAset["RAgreet"][msg.to]
                                        f=codecs.open('RAset.json','w','utf-8')
                                        json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to,"Pesan sambutan dimatikan")
                                        
        #------------------- Protect Command Finish ------------------#  
        
        #------------------- Main Command Start ----------------------#
        
                            elif msg.text == RAKey +'absen':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                        cl.sendText(msg.to,"Hai "+str(cl.getGroup(msg.to).name)+" ")
                                        
                            elif msg.text == RAKey + 'spbot':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    start = time.time()
                                    cl.sendText("u3b07c57b6239e5216aa4c7a02687c86d", '.')
                                    cl.sendText(msg.to, '%s ' % (time.time()-start))
                                    
                            elif msg.text == self.resp +"sprespon":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    get_profile_time_start = time.time()
                                    get_profile = cl.getProfile()
                                    get_profile_time = time.time() - get_profile_time_start
                                    get_group_time_start = time.time()
                                    get_group = cl.getGroupIdsJoined()
                                    get_group_time = time.time() - get_group_time_start
                                    get_contact_time_start = time.time()
                                    get_contact = cl.getContact(self.mid)
                                    get_contact_time = time.time() - get_contact_time_start
                                    cl.sendText(msg.to, "speed respon\n + Get Profile\n   %.10f\n + Get Contact\n   %.10f\n + Get Group\n   %.10f" % (get_profile_time/4,get_contact_time/4,get_group_time/4))
                                    
                            elif RAKey +"cname " in msg.text:
                                if msg._from in RASadmin:
                                    string = msg.text.replace(RAKey + "cname ","")
                                    profile_B = cl.getProfile()
                                    profile_B.displayName = string
                                    cl.updateProfile(profile_B)
                                    cl.sendText(msg.to,"Sukses.\nnama : {}".format(str(string)))
                                    
                            elif RAKey +"cbio " in msg.text:
                                if msg._from in RASadmin:
                                    string = msg.text.replace(RAKey + "cbio ","")
                                    profile_B = cl.getProfile()
                                    profile_B.statusMessage = string
                                    cl.updateProfile(profile_B)
                                    cl.sendText(msg.to,"Sukses.\n\n{}".format(str(string)))
                                    
                            elif msg.text == RAKey +"cfoto":
                                if msg._from in RASadmin:
                                    self.RAset["RAfoto"][msg.to] = True
                                    cl.sendText(msg.to,"Kirim fotonya.")
                            
                            elif msg.text == RAKey +'cleanblacklist':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    group = cl.getGroup(msg.to)
                                    gMembMids = [contact.mid for contact in group.members]
                                    matched_list = []
                                    if matched_list != []:
                                        cl.sendText(msg.to,"Peringatan user bl")
                                    for tag in self.wait["RAblacklist"]:
                                        matched_list+=filter(lambda str: str == tag, gMembMids)
                                    if matched_list == []:
                                        cl.sendText(msg.to,"User bl tidak ada")
                                        return
                                    for jj in matched_list:
                                        cl.kickoutFromGroup(msg.to,[jj])
                                        
                            elif msg.text == RAKey +'byeall':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.toType == 2:
                                        x = cl.getGroup(msg.to)
                                        cl.leaveGroup(msg.to)
                                            
                            elif msg.text == RAKey +'leaveall':
                                if msg._from in RASadmin:
                                    gid = cl.getGroupIdsJoined()
                                    for i in gid:
                                        cl.leaveGroup(i)
                                        
                            elif RAKey + "cleanmember" in msg.text:
                                if msg._from in RASadmin:
                                    gs = cl.getGroup(msg.to)
                                    targets = []
                                    for x in gs.members:
                                        targets.append(x.mid)
                                    for a in self.wait["RABots"]:
                                        if a in targets:
                                            try:
                                                targets.remove(a)
                                            except:
                                                pass
                                    for b in self.wait["RAAdmin"]:
                                        if b in targets:
                                            try:
                                                targets.remove(b)
                                            except:
                                                pass
                                    for c in RASadmin:
                                        if c in targets:
                                            try:
                                                targets.remove(c)
                                            except:
                                                pass
                                    for d in self.wait["RAStaff"]:
                                        if d in targets:
                                            try:
                                                targets.remove(d)
                                            except:
                                                pass
                                    cl.sendText(msg.to,"Byebye")
                                    for target in targets:
                                        try:
                                            cl.kickoutFromGroup(msg.to,[target])
                                        except:
                                            pass
                                        
                            elif msg.text == RAKey + 'restart':
                                if msg._from in RASadmin:
                                    cl.sendText(msg.to,"Tunggu Sebentar..")
                                    python3 = sys.executable
                                    os.execl(python3, python3, *sys.argv)
                                    
                            elif RAKey +"masuksemua" in msg.text:
                                if msg._from in RASadmin:
                                    gs = cl.getGroup(msg.to)
                                    targets = []
                                    for x in gs.members:
                                        targets.append(x.mid)
                                    for a in self.wait["RABots"]:
                                        if a in targets:
                                            try:
                                                targets.remove(a)
                                            except:
                                                pass
                                    cl.sendText(msg.to,"Sudah masuk di list")
                                    for target in targets:
                                        if target not in RASadmin:
                                            if target not in self.wait["RAAdmin"]:
                                                if target not in self.wait["RAStaff"]:
                                                    try:
                                                        self.wait["RABots"][target] = True
                                                        f=codecs.open('RAwait.json','w','utf-8')
                                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                        cl.sendText(msg.to,"Berhasil..")
                                                    except:
                                                        pass
                                    
                                    
                            elif msg.text == RAKey + 'removechat':
                                if msg._from in RASadmin:
                                    try:
                                        cl.removeAllMessages(op.param2)
                                        cl.sendText(msg.to,"Chat Bersih....")
                                    except:
                                        pass
                                    
                            elif RAKey +'leave ' in msg.text:
                                if msg._from in RASadmin:
                                    ng = msg.text.replace(RAKey + 'leave ','')
                                    gid = cl.getGroupIdsJoined()
                                    for i in gid:
                                        h = cl.getGroup(i).name
                                        if h == ng:
                                            cl.leaveGroup(i)
                                                
                            elif RAKey + "bl" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"] or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                self.wait["RAblacklist"][target] = True
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" telah di blacklist")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" sudah di blacklist")
                                                
                            elif RAKey + "ubl" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"] or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                del self.wait["RAblacklist"][target]
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" dihapus dari blacklist")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" tidak ada di blacklist")
                                                
                            elif RAKey + "adadd" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                self.wait["RAAdmin"][target] = True
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" diangkat menjadi admin")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" maaf kamu sudah menjadi admin")
                                                
                            elif RAKey + "addell" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                del self.wait["RAAdmin"][target]
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" sudah tidak menjadi admin")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" maaf kamu belum pernah menjadi admin")
                                                
                            elif RAKey + "stadd" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"]:
                                            pass
                                        else:
                                            try:
                                                self.wait["RAStaff"][target] = True
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" diangkat menjadi staff")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" maaf kamu sudah menjadi staff")
                                                
                            elif RAKey + "stdell" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"]:
                                            pass
                                        else:
                                            try:
                                                del self.wait["RAStaff"][target]
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" sudah tidak menjadi staff")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" maaf kamu belum pernah menjadi staff")
                                                
                            elif RAKey + "nganubot" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"] or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                self.wait["RABots"][target] = True
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" masuk kedalam LISTBOT")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" sudah ada di LISTBOT")
                                                
                            elif RAKey + "cuekinbot" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"] or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                del self.wait["RABots"][target]
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" dikeluarkan dari LISTBOT")
                                            except:
                                                cl.sendText(msg.to," "+str(cl.getContact(target).displayName)+" belum ada di LISTBOT")
                                                
        #------------------- Main Command Finish ----------------------#
        
        #------------------- Bot Command Start ----------------------# 
        
                            
        
                            elif msg.text == self.resp + 'ourl':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.toType == 2:
                                        x = cl.getGroup(msg.to)
                                        if x.preventedJoinByTicket == True:
                                            x.preventedJoinByTicket = False
                                            cl.updateGroup(x)
                                        gurl = cl.reissueGroupTicket(msg.to)
                                        cl.sendText(msg.to," "+str(cl.getGroup(msg.to).creator.displayName)+ " izin membuka link ya..\n\nline://ti/g/{}".format(str(gurl)))
                            
                            elif msg.text == self.resp + 'curl':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if msg.toType == 2:
                                        X = cl.getGroup(msg.to)
                                        X.preventedJoinByTicket = True
                                        cl.updateGroup(X)
                            
                            elif msg.text == self.resp + 'informasi':
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    a = cl.getGroupIdsJoined()
                                    b = cl.getAllContactIds()
                                    hasil = "Informasi {} V.3".format(str(cl.getProfile().displayName))
                                    hasil += "\n\nNama group  : {}".format(str(cl.getGroup(msg.to).name))
                                    hasil += "\nCreator group : {}".format(str(cl.getGroup(msg.to).creator.displayName))
                                    hasil += "\nMember group: {}".format(str(len(cl.getGroup(msg.to).members)))
                                    hasil += "\nDiatas adalah informasi group ini"
                                    hasil += "\n\nUntuk bot sendiri kita mempunyai informasi sudah bergabung ke {} group".format(str(len(a)))
                                    hasil += " memiliki {} teman".format(str(len(b)))
                                    hasil += ", sekian informasi tersebut."
                                    eltime = time.time() - mulai
                                    cin = " "+waktu(eltime)
                                    hasil += "\n\noiya aku sudah online\n {}".format(str(cin))
                                    path = "http://dl.profile.line-cdn.net/" +str(cl.getGroup(msg.to).pictureStatus)
                                    cl.sendImageWithURL(msg.to,path)
                                    cl.sendText(msg.to,hasil)
                                    
                            
                            elif self.resp +"listgroup" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    proses = msg.text.split(" ")
                                    urutan = msg.text.replace(proses[0]+" ","")
                                    count = urutan.split("|")
                                    logika = str(count[0])
                                    if len(count) == 1:
                                        gid = cl.getGroupIdsJoined()
                                        no = 0
                                        hasil = "List group\n"
                                        for i in gid:
                                            no += 1
                                            hasil += "\n" +str(no)+ ". " +str(cl.getGroup(i).name)
                                        hasil += "\n\nTotal {} group".format(str(len(gid)))
                                        cl.sendText(msg.to,hasil)
                                        if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                            cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+"\nSilahkan pilih keinginan:\n\n[Cek member]\n"+self.resp+"listgroup | angka\n\n[Chat group]\n"+self.resp+"gchat text | angka\n\n[daftar gbc]\n"+self.resp+"gdaftarbc angka\n\n[hapus gbc]\n"+self.resp+"ghapusbc angka\n\n[glist bc]\n"+self.resp+"glistbc\n\n[hapusall gbc]\n"+self.resp+"hapusallbc\n\n[leave group]\n"+RAKey+"gleave angka")
                                        else:
                                            cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+"\n\nSilahkan pilih keinginan:\n\n[Cek member]\n"+self.resp+"listgroup | angka\n\n[Chat group]\n"+self.resp+"gchat text | angka")
                                    elif len(count) == 2:
                                        try:
                                            num = int(count[1])
                                            G = cl.getGroupIdsJoined()[num - 1]
                                            group = cl.getGroup(G)
                                            no = 0
                                            hasil = "Group {}\n".format(str(group.name))
                                            for member in group.members:
                                                no += 1
                                                hasil += "\n" + str(no) + ". " + str(member.displayName)
                                            hasil += "\n"
                                            cl.sendText(msg.to,hasil)
                                        except Exception as e:
                                            cl.sendText(msg.to," "+str(e))
                                    
                            elif self.resp +"cname " in msg.text:
                                if msg._from in RASadmin:
                                    string = msg.text.replace(self.resp + "cname ","")
                                    profile_B = cl.getProfile()
                                    profile_B.displayName = string
                                    cl.updateProfile(profile_B)
                                    cl.sendText(msg.to,"Sukses.\nnama : {}".format(str(string)))
                            
                            elif self.resp +"cbio " in msg.text:
                                if msg._from in RASadmin:
                                    string = msg.text.replace(self.resp+"cbio ","")
                                    profile_B = cl.getProfile()
                                    profile_B.statusMessage = string
                                    cl.updateProfile(profile_B)
                                    cl.sendText(msg.to,"Sukses.\n\n{}".format(str(string)))
                            
                            elif msg.text == self.resp +"cfoto":
                                if msg._from in RASadmin:
                                    self.RAset["RAfoto"][self.mid] = True
                                    cl.sendText(msg.to,"Kirim fotonya.")
                        
                            elif msg.text == self.resp +"cfotogroup":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    self.RAset["RAGfoto"][msg.to] = True
                                    cl.sendText(msg.to,"Kirim fotonya.")
                            
                            elif self.resp +"bc " in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    teks = msg.text.replace(self.resp+"bc ","")
                                    a = cl.getGroupIdsJoined()
                                    try:
                                        if text == "":
                                            cl.sendText(msg.to,"Tidak ada pesan")
                                        else:
                                            for gid in a:
                                                if gid in self.wait["RAlimit"]:
                                                    cl.sendText(gid,"Broadcast dari "+str(cl.getContact(msg._from).displayName)+"\n\n{}".format(str(teks)))
                                                cl.sendText(msg.to,"sukses broadcast")
                                    except Exception as e:
                                        cl.sendText(msg.to,(e))
                                            
                            elif self.resp + "kick" in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    key["MENTIONEES"][0]["M"]
                                    targets = []
                                    for x in key["MENTIONEES"]:
                                        targets.append(x["M"])
                                    for target in targets:
                                        if target in RASadmin or target in self.wait["RAAdmin"] or target in self.wait["RAStaff"]:
                                            pass
                                        else:
                                            try:
                                                cl.kickoutFromGroup(msg.to,[target])
                                            except:
                                                pass
                                            
                            elif msg.text == self.resp +"listbl":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if self.wait["RAblacklist"] == {}:
                                        cl.sendText(msg.to,"Tidak ada akun terblacklist")
                                    else:
                                        no = 0
                                        hasil = "User\n"
                                        for mi_d in self.wait["RAblacklist"]:
                                            no += 1
                                            hasil += "\n" +str(no)+ ". " +str(cl.getContact(mi_d).displayName)
                                        hasil += "\n\nTotal {} blacklist".format(str(len(self.wait["RAblacklist"])))
                                        cl.sendText(msg.to,hasil)
                                        
                            elif msg.text == self.resp +"listteam":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    a = "Super admin"
                                    b = "Level Admin"
                                    c = "Level Staff"
                                    aa = 0
                                    for m_id in RASadmin:
                                        aa += 1
                                        a += "\n" +str(aa)+ ". " +str(cl.getContact(m_id).displayName)
                                    for m_id in self.wait["RAAdmin"]:
                                        aa += 1
                                        b += "\n" +str(aa)+ ". " +str(cl.getContact(m_id).displayName)
                                    for m_id in self.wait["RAStaff"]:
                                        aa += 1
                                        c += "\n" +str(aa)+ ". " +str(cl.getContact(m_id).displayName)
                                    cl.sendText(msg.to,"User\n\n"+a+"\n\n"+b+"\n\n"+c+"\n\nTotal %s team" %(str(len(RASadmin)+len(self.wait["RAAdmin"])+len(self.wait["RAStaff"]))))
                                    
                            elif msg.text == self.resp +"listbot":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    if self.wait["RABots"] == {}:
                                        cl.sendText(msg.to,"Bot belum terdaftar")
                                    else:
                                        no = 0
                                        hasil = "User\n"
                                        for m_id in self.wait["RABots"]:
                                            no += 1
                                            hasil += "\n" +str(no)+ ". " +str(cl.getContact(m_id).displayName)
                                        hasil += "\n\nTotal {} BOT".format(str(len(self.wait["RABots"])))    
                                        cl.sendText(msg.to,hasil)
                                        
                            elif msg.text == self.resp +"liststatus":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    a = "Status Protect QR"
                                    b = "Status Protect Invite"
                                    c = "Status Protect Cancel"
                                    d = "Status Protect Kick"
                                    e = "Status Greet message"
                                    f = "Status Autoread Message"
                                    aa = 0
                                    for gid in self.RAset["RAprotqr"]:
                                        aa += 1
                                        a += "\n" +str(aa)+ ". " +cl.getGroup(gid).name
                                    for gid in self.RAset["RAprotinvite"]:
                                        aa += 1
                                        b += "\n" +str(aa)+ ". " +cl.getGroup(gid).name
                                    for gid in self.RAset["RAprotcancel"]:
                                        aa += 1
                                        c += "\n" +str(aa)+ ". " +cl.getGroup(gid).name
                                    for gid in self.RAset["RAprotkick"]:
                                        aa += 1
                                        d += "\n" +str(aa)+ ". " +cl.getGroup(gid).name
                                    for gid in self.RAset["RAgreet"]:
                                        aa += 1
                                        e += "\n" +str(aa)+ ". " +cl.getGroup(gid).name
                                    for gid in self.wait["RAautoread"]:
                                        aa += 1
                                        f += "\n" +str(aa)+ ". " +cl.getGroup(gid).name    
                                    cl.sendText(msg.to,"🔰List status\n\n"+a+"\n\n"+b+"\n\n"+c+"\n\n"+d+"\n\n"+e+"\n\n"+f+"\n\nTotal %s Group" %(str(len(self.RAset["RAprotqr"])+len(self.RAset["RAprotcancel"])+len(self.RAset["RAprotkick"])+len(self.RAset["RAgreet"])+len(self.wait["RAautoread"]))))
                                    
                            elif '/ti/g/' in msg.text.lower():
                                if msg._from in RASadmin:
                                    link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                    links = link_re.findall(msg.text)
                                    n_links=[]
                                    for l in links:
                                        if l not in n_links:
                                            n_links.append(l)
                                    for ticket_id in n_links:
                                        if self.wait["RAautojoin"] == True:
                                            group = cl.findGroupByTicket(ticket_id)
                                            cl.acceptGroupInvitationByTicket(group.id,ticket_id)
        
        #------------------- Bot Command Finish ----------------------# 
        
        #------------------- Bot Change Start ----------------------#
                            elif self.resp +"cwelcome " in text.lower():
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    teks = text.replace(self.resp+"cwelcome ","")
                                    self.wait["RAmessage"][msg.to] = {"Pesan":teks,"Creator":cl.getGroup(msg.to).creator.displayName}
                                    self.RAset["RAgreet"][msg.to] = True
                                    f=codecs.open('RAset.json','w','utf-8')
                                    json.dump(self.RAset, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    f=codecs.open('RAwait.json','w','utf-8')
                                    json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Greet message aktif\n\npesan telah diatur menjadi :\n"+str(self.wait["RAmessage"][msg.to]["Pesan"]))
                            
        #------------------- Bot Remote Start ----------------------#
                            elif self.resp +"gchat " in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"] or msg._from in self.wait["RAStaff"]:
                                    keyword = msg.text.replace(self.resp+"gchat ","")
                                    query = keyword.split("|")
                                    teks = query[0]
                                    urutan = query[1]
                                    a = cl.getGroupIdsJoined()
                                    try:
                                        groups = a[int(urutan)-1]
                                        cl.sendText(groups,"Hallo "+str(cl.getGroup(groups).creator.displayName)+"\nada pesan dari group "+str(cl.getGroup(msg.to).name)+"\n\nisi pesan :\n{}".format(str(teks)))
                                        cl.sendContact(groups,msg._from)
                                    except Exception as e:
                                        cl.sendText(msg.to,(e))
                                        
                            elif self.resp +"gdaftarbc " in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    number = msg.text.replace(self.resp+"gdaftarbc ","")
                                    a = cl.getGroupIdsJoined()
                                    try:
                                        b = a[int(number)-1]
                                        self.wait["RAlimit"][b] = True
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+" berhasil menambahkan "+str(cl.getGroup(b).name)+" kedalam listbc")
                                    except Exception as e:
                                        cl.sendText(msg.to,(e))
                                        
                            elif self.resp +"ghapusbc " in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    number = msg.text.replace(self.resp+"ghapusbc ","")
                                    a = cl.getGroupIdsJoined()
                                    try:
                                        b = a[int(number)-1]
                                        del self.wait["RAlimit"][b]
                                        f=codecs.open('RAwait.json','w','utf-8')
                                        json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+" berhasil menghapus "+str(cl.getGroup(b).name)+" dari listbc")
                                    except Exception as e:
                                        cl.sendText(msg.to,(e))
                                        
                            elif msg.text == self.resp +"glistbc":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    if self.wait["RAlimit"] == {}:
                                        cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+" tidak ada group yg terdaftar")
                                    else:
                                        no = 0
                                        hasil = "Group\n"
                                        for gid in self.wait["RAlimit"]:
                                            no += 1
                                            hasil += "\n" +str(no)+ ". " + str(cl.getGroup(gid).name)
                                        hasil += "\n\nTotal {} group".format(str(len(self.wait["RAlimit"])))
                                        cl.sendText(msg.to,hasil)
                                        
                            elif msg.text == self.resp +"hapusallbc":
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    _name = msg.text.replace(self.resp +"hapusallbc","")
                                    _nametarget = _name.rstrip('  ')
                                    targets = []
                                    for a in self.wait["RAlimit"]:
                                        targets.append(a)
                                    if targets == []:
                                        cl.sendText(msg.to," "+str(cl.getContact(msg._from).displayName)+" tidak ada group yg terdaftar")
                                    else:
                                        try:
                                            for target in targets:
                                                del self.wait["RAlimit"][target]
                                                f=codecs.open('RAwait.json','w','utf-8')
                                                json.dump(self.wait, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                cl.sendText(msg.to,"List terhapus")
                                        except Exception as e:
                                            cl.sendText(msg.to,(e))
                                            
                            elif RAKey +"gleave " in msg.text:
                                if msg._from in RASadmin or msg._from in self.wait["RAAdmin"]:
                                    number = msg.text.replace(RAKey+"gleave ","")
                                    a = cl.getGroupIdsJoined()
                                    try:
                                        groups = a[int(number)-1]
                                        cl.leaveGroup(groups)
                                    except Exception as e:
                                        cl.sendText(msg.to,(e))    
        
                                        
        #------------------- Bot Remote finish ----------------------#                                
                                
                                    
                            
                    
                            
        except Exception as e:
            print(e)
