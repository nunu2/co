from LINEPY import *
from akad.ttypes import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import time, asyncio, json, threading, codecs, sys, os, re, urllib, requests, wikipedia, html5lib, timeit, pafy, youtube_dl

line = LINE("EuxMKJA4TO7axX82XGua.RarV+yhk8E2V4GZUoAJCQG.jeAWIruR/vLFQCA4mtmOBrGpwrnlQ1QHCpw0CrSjJi0=")
line.log("Auth Token : " + str(line.authToken))
line.log("Timeline Token : " + str(line.tl.channelAccessToken))


cl = line
oepoll = OEPoll(cl)
mid = cl.profile.mid
RAOwner = ["ud62334f46b0f181f69beaf801ab3c75a"]
Setbot = codecs.open("setting.json","r","utf-8")
Setmain = json.load(Setbot) 

def bot(op):
    try:
        if op.type == 5:
            if Setmain["autoadd"] == True:
                cl.sendMessageWithMention(op.param1, op.param1,"Hai","\nsalam kenal ya\n\n{}".format(str(Setmain["RAmessage"])))
                

        if op.type == 13:
            if mid in op.param3:
              if op.param2 in RAOwner or op.param2 in Setmain["RABots"]  or op.param2 in Setmain["RAAdmin"]:                    
                if Setmain["autojoin"] == True:                 
                    cl.acceptGroupInvitation(op.param1)

        if op.type == 11:
           if Setmain["protectqr"] == True:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"] and op.param2 not in Setmain ["RAStaff"]:
                   G = cl.getGroup(op.param1)
                   G.preventJoinByTicket = True
                   cl.kickoutFromGroup(op.param1,[op.param2])
                   cl.updateGroup(G)
                   Setmain["blacklist"][op.param2] = True        
        if op.type == 13:
           if Setmain["protectguest"] == True:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"] and op.param2 not in Setmain ["RAStaff"]: 
                  cl.cancelGroupInvitation(op.param1,[op.param3])
                  cl.kickoutFromGroup(op.param1,[op.param2]) 
                  Setmain["blacklist"][op.param2] = True
        if op.type == 13:
            if op.param3 in Setmain["blacklist"]:
                cl.cancelGroupInvitation(op.param1,[op.param3])
                cl.kickoutFromGroup(op.param1,[op.param2])
            else:
                pass                
        if op.type == 17:
            if op.param2 in Setmain["blacklist"]:
                cl.kickoutFromGroup(op.param1,[op.param2])
            else:
                pass
        if op.type == 32:
           if Setmain["cancel"] == True:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"] and op.param2 not in Setmain ["RAStaff"]:   
                  cl.kickoutFromGroup(op.param1,[op.param2])
                  Setmain["blacklist"][op.param2] = True            
        if op.type == 19:
           if Setmain["protect"] == True:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"] and op.param2 not in Setmain ["RAStaff"]:
                  cl.kickoutFromGroup(op.param1,[op.param2]) 
                  Setmain["blacklist"][op.param2] = True                
        if op.type == 19:
           if op.param3 in Setmain["RABots"]:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"]:    
                   cl.inviteIntoGroup(op.param1,[op.param3])            
                   cl.kickoutFromGroup(op.param1,[op.param2])
                   Setmain["blacklist"][op.param2] = True
               else:
                   pass
        if op.type == 19:
           if op.param3 in RAOwner and op.param3 in Setmain["RAAdmin"] and op.param3 in Setmain["RAStaff"]:
               if op.param2 not in RAOwner and op.param2 not in Setmain["RABots"] and op.param2 not in Setmain["RAAdmin"]:    
                   cl.inviteIntoGroup(op.param1,[op.param3])            
                   cl.kickoutFromGroup(op.param1,[op.param2])
                   Setmain["blacklist"][op.param2] = True
               else:
                   pass
                                        
        if op.type == 46:
            if op.param2 in mid:
                cl.removeAllMessages() 
        if op.type == 28:
           if Setmain["larangan"] == True:
               if op.param2 not in RAOwner:
                  cl.kickoutFromGroup(op.param1,[op.param2])
        if op.type == 19:
            if mid in op.param3:
               Setmain["blacklist"][op.param2] = True                
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
                    if Setmain["autoscan"] == True:
                        msg.contentType = 0
                        cl.sendText(msg.to,msg.contentMetadata["mid"])
                if msg._from in RAOwner:
                   if Setmain["botadd"] == True:
                     if msg.contentMetadata["mid"] in Setmain["RABots"]:
                        cl.sendMessage(msg.to,"Contact itu sudah jadi anggota bot")
                        Setmain["botadd"] = True
                     else:
                        Setmain["RABots"].append(msg.contentMetadata["mid"])
                        Setmain["botadd"] = True
                        cl.sendMessage(msg.to,"Berhasil menambahkan ke anggota bot")
                if Setmain["botdell"] == True:
                    if msg.contentMetadata["mid"] in Setmain["RABots"]:
                        Setmain["RABots"].remove(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"Berhasil menghapus dari anggota bot")
                    else:
                        Setmain["botdell"] = True
                        cl.sendMessage(msg.to,"Contact itu bukan anggota bot saints")
#ADD STAFF
                if msg._from in RAOwner:
                  if Setmain["staffadd"] == True:
                    if msg.contentMetadata["mid"] in Setmin["RAStaff"]:
                        cl.sendMessage(msg.to,"Contact itu sudah jadi staff")
                        Setmain["staffadd"] = True
                    else:
                        Setmain["RAStaff"].append(msg.contentMetadata["mid"])
                        Setmain["staffadd"] = True
                        cl.sendMessage(msg.to,"Berhasil menambahkan ke staff")
                if Setmain["staffdell"] == True:
                    if msg.contentMetadata["mid"] in Setmain["RAStaff"]:
                        Setmain["RAStaff"].remove(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"Berhasil menghapus dari staff")
                        Setmain["staffdell"] = True
                    else:
                        Setmain["staffdell"] = True
                        cl.sendMessage(msg.to,"Contact itu bukan staff")
#ADD ADMIN
                if msg._from in RAOwner:
                  if Setmain["adminadd"] == True:
                    if msg.contentMetadata["mid"] in Setmain["RAAdmin"]:
                        cl.sendMessage(msg.to,"Contact itu sudah jadi admin")
                        Setmain["adminadd"] = True
                    else:
                        Setmain["RAAdmin"].append(msg.contentMetadata["mid"])
                        Setmain["adminadd"] = True
                        cl.sendMessage(msg.to,"Berhasil menambahkan ke admin")
                if Setmain["admindell"] == True:
                    if msg.contentMetadata["mid"] in RAAdmin:
                        Setmain["RAAdmin"].remove(msg.contentMetadata["mid"])
                        cl.sendMessage(msg.to,"Berhasil menghapus dari admin")
                    else:
                        Setmain["admindell"] = True
                        cl.sendMessage(msg.to,"Contact itu bukan admin")
#ADD BLACKLIST
                if msg._from in RAOwner:
                  if Setmain["wblacklist"] == True:
                    if msg.contentMetadata["mid"] in Setmain["blacklist"]:
                        cl.sendMessage(msg.to,"Contact itu sudah ada di blacklist")
                        Setmain["wblacklist"] = True
                    else:
                        Setmain["blacklist"][msg.contentMetadata["mid"]] = True
                        Setmain["wblacklist"] = True
                        cl.sendMessage(msg.to,"Berhasil menambahkan ke blacklist user")
                if Setmain["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in Setmain["blacklist"]:
                        del Setmain["blacklist"][msg.contentMetadata["mid"]]
                        cl.sendMessage(msg.to,"Berhasil menghapus dari blacklist user")
                    else:
                        Setmain["dblacklist"] = True
                        cl.sendMessage(msg.to,"Contact itu tidak ada di blacklist")
#TALKBAN                        
                        
                elif msg.contentType == 0:
                    if Setmain["autoread"] == True:
                        cl.sendChatChecked(msg.to, msg_id)
                    if text is None:    
                        return
                    else:
                        
            #---------------------- Start Command ------------------------#
                        
                        if text.lower() == "menu":
                          if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in ["RAStaff"]:                        
                              md = " 🔎² 🔎² αя вσтѕ 🔎² \n\n"
                              md += "🔎² .cek「@」\n"
                              md += "🔎² .gid\n"
                              md += "🔎² .yid\n"
                              md += "🔎² .pengaturan\n"
                              md += "🔎² .restart\n"
                              md += "🔎² .removechat\n"
                              md += "🔎² .cekmid 「on/off」\n"
                              md += "🔎² .autoread 「on/off」\n"
                              md += "🔎² menu1\n"
                              cl.sendText(msg.to, md)
                            
                        if text.lower() == "menu1":
                          if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                        
                              md = " 🔎² 🔎² αя вσтѕ 🔎²  \n\n"
                              md += "🔎² .protect on/off\n"
                              md += "🔎² .qr on/of\n"
                              md += "🔎² .invite on/off\n"
                              md += "🔎² .larangan on/off\n"                            
                              md += "🔎² .hai\n"
                              md += "🔎² .respon\n"                            
                              md += "🔎² .spbot\n"
                              md += "🔎² .clearban\n"
                              md += "🔎² .pulang\n"                                
                              md += "🔎² .listbl\n"                                
                              cl.sendText(msg.to, md)                            
                            
                        elif text.lower() == ".set":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:
                                ginfo = cl.getGroup(msg.to)                               
                                md = "\n\npengaturan di group\n " +str(ginfo.name) + "\n\n"
                                if Setmain["autoscan"] == True: md+="✅  cekmid\n"
                                else: md+="❎ cekmid\n"
                                if Setmain["autoread"] == True: md+="✅ autoread\n"
                                else: md+="❎ autoread\n"
                                if Setmain["protect"] == True: md+="✅ protect\n"
                                else: md+="❎ protect\n"
                                if Setmain["protectqr"] == True: md+="✅ qr\n"
                                else: md+="❎ qr\n"
                                if Setmain["protectguest"] == True: md+="✅ invite\n"
                                else: md+="❎ invite\n"
                                if Setmain["autojoin"] == True: md+="✅ autojoin\n"
                                else: md+="❎ autojoin\n" 
                                if Setmain["larangan"] == True: md+="✅ larangan\n"
                                else: md+="❎ larangan\n"                                     
                                cl.sendText(msg.to, md)
                                
            #---------------------- On/Off Command -------------------# 
            
                        elif text.lower() == ".autoread on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                    
                                if Setmain["autoread"] == False:
                                    Setmain["autoread"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Autoread diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".autoread off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                            
                                if Setmain["autoread"] == True:
                                    Setmain["autoread"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Autoread dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah off")

                        elif text.lower() == "cancel on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:                            
                                if Setmain["cancel"] == False:
                                    Setmain["cancel"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == "cancel off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:          
                                if Setmain["cancel"] == True:
                                    Setmain["cancel"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","di nonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah off")
                                                
                        elif text.lower() == ".protect on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:      
                                if Setmain["protect"] == False:
                                    Setmain["protect"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect group diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".protect off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:  
                                if Setmain["protect"] == True:
                                    Setmain["protect"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect group dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","sudah off")

                        elif text.lower() == ".larangan on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:
                                if Setmain["larangan"] == False:
                                    Setmain["larangan"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","larangan group diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".larangan off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:          
                                if Setmain["larangan"] == True:
                                    Setmain["larangan"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","larangan group dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","sudah off")                                    

                        elif text.lower() == ".join on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:  
                                if Setmain["autojoin"] == False:
                                    Setmain["autojoin"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","already on")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".join off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:                            
                                if Setmain["autojoin"] == True:
                                    Setmain["autojoin"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","already off")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","sudah off")                                    
                                    
                                    
                        elif text.lower() == ".invite on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:
                                if Setmain["protectguest"] == False:
                                    Setmain["protectguest"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect invite diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".invite off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:                            
                                if Setmain["protectguest"] == True:
                                    Setmain["protectguest"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect invite dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","sudah off")                                    
                                    
            
                        elif text.lower() == ".qr on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:   
                                if Setmain["protectqr"] == False:
                                    Setmain["protectqr"] = True
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect Qr diaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".qr off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:
                                if Setmain["protectqr"] == True:
                                    Setmain["protectqr"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","protect Qr dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah off")                                   
                                    
                        elif text.lower() == ".cekmid on":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]: 
                                if Setmain["autoscan"] == False:
                                    Setmain["autoscan"] = True
                                    ginfo = cl.getGroup(msg.to)
                                    msgs = "cekmid diaktifkan\nDi Group  " +str(ginfo.name)
                                    cl.sendText(msg.to, msgs)                                    
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah aktif")
                                    
                        elif text.lower() == ".cekmid off":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:    
                                if Setmain["autoscan"] == True:
                                    Setmain["autoscan"] = False
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Cekmid dinonaktifkan")
                                else:
                                    cl.sendMessageWithMention(msg.to,msg._from,"","Sudah off")            
                            
            #---------------- Fungsi Command ------------------#
                        
                                                                       
                        elif ".cek" in text.lower():
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                         
                                key = eval(msg.contentMetadata["MENTION"])
                                keys = key["MENTIONEES"][0]["M"]
                                ra = cl.getContact(keys)
                                try:
                                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/{}".format(str(ra.pictureStatus)))
                                    cl.sendMessageWithMention(msg.to,ra.mid,"[Nama]\n","\n\n[Bio]\n{}".format(str(ra.statusMessage)))
                                except:
                                    pass
                            
                        elif text.lower() == ".gid":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                                
                                cl.sendMessageWithMention(msg.to, msg._from,"","\nMemproses..")
                                cl.sendText(msg.to,msg.to)
                            
                        elif text.lower() == ".yid":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                            
                                cl.sendMessageWithMention(msg.to, msg._from,"","\nMemproses..")
                                cl.sendText(msg.to,msg._from)
                        
                        elif text.lower() == ".respon":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                                 
                                cl.sendMessageWithMention(msg.to,msg._from,""," ")
                            
                        elif text.lower() == ".spbot":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                             
                                start = time.time()
                                cl.sendText(msg.to, "Loading...")
                                elapsed_time = time.time() - start
                                cl.sendText(msg.to, "%s " % (elapsed_time))
                          
                        elif text.lower() == ".restart":
                            if msg._from in RAOwner:
                                cl.sendMessageWithMention(msg.to,msg._from,"","Tunggu Sebentar..")
                                python3 = sys.executable
                                os.execl(python3, python3, *sys.argv)
                                
                        elif text.lower() == ".removechat":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:     
                                try:
                                    cl.removeAllMessages(op.param2)
                                    cl.sendMessageWithMention(msg.to,msg._from,"","chat bersih...")
                                except:
                                    pass        
                                                    
                        elif text.lower() == ".pulang":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:
                                ra = cl.getGroup(msg.to)
                                #cl.sendMessageWithMention(msg.to,ra.creator.mid,"Maaf pemilik group","\naku keluar dulu ya..")
                                cl.leaveGroup(msg.to)
                        elif text.lower() ==".clearban":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:                                  
                                Setmain["blacklist"] = {}
                                cl.sendMessageWithMention(msg.to,msg._from,"","blacklist di kosongkan.")                                 

                        elif text.lower() == ".listgroup":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:  
                               ma = ""
                               a = 0
                               gid = cl.getGroupIdsJoined()
                               for i in gid:
                                   G = cl.getGroup(i)
                                   a = a + 1
                                   end = "\n"
                                   ma += "╠ " + str(a) + ". " +G.name+ "\n"
                               cl.sendText(msg.to,"╔══[ ℓιsт gяσυρ ]\n║\n"+ma+"║\n╚══[ тσтαℓ「"+str(len(gid))+"」gяσυρ ]")                                
                                
                        elif text.lower() == ".listbl":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:
                                if Setmain["blacklist"] == {}:
                                    cl.sendMessageWithMention(msg.to, msg._from,"Maaf","blacklist kosong")
                                else:
                                    no = 0
                                    hasil = "🔎² αя вσтѕ 🔎²\n"
                                    for a in cl.getContacts(Setmain["blacklist"]):
                                        no += 1
                                        hasil += "\n" + str(no) + ". " + str(a.displayName)
                                    hasil += "\n\nтσтαℓ {} вℓα¢ℓιsт".format(str(len(cl.getContacts(Setmain["blacklist"]))))
                                    cl.sendText(msg.to,hasil)

                        elif text.lower() == "admin":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:   
                                if Setmain["RAAdmin"] == {}:
                                    cl.sendMessageWithMention(msg.to, msg._from,"Maaf","belom ada admin")
                                else:
                                    no = 0
                                    hasil = "🔎² αя вσтѕ 🔎²\n"
                                    for a in cl.getContacts(Setmain["RAAdmin"]):
                                        no += 1
                                        hasil += "\n" + str(no) + ". " + str(a.displayName)
                                    hasil += "\n\nтσтαℓ {} вℓα¢ℓιsт".format(str(len(cl.getContacts(Setmain["RAAdmin"]))))
                                    cl.sendText(msg.to,hasil)
                        elif text.lower() == "bots":
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"] or msg._from in Setmain["RAStaff"]:        
                                if Setmain["RABots"] == {}:
                                    cl.sendMessageWithMention(msg.to, msg._from,"Maaf","belom ada bots")
                                else:
                                    no = 0
                                    hasil = "🔎² αя вσтѕ 🔎²\n"
                                    for a in cl.getContacts(Setmain["RABots"]):
                                        no += 1
                                        hasil += "\n" + str(no) + ". " + str(a.displayName)
                                    hasil += "\n\nтσтαℓ {} вℓα¢ℓιsт".format(str(len(cl.getContacts(Setmain["RABots"]))))
                                    cl.sendText(msg.to,hasil)
                                                                        
                        elif ".hai" in text.lower():
                            if msg._from in RASuper:
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                targets = []
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    if target in Setmain["RABots"]:
                                        pass
                                    else:
                                        try:
                                            #cl.sendMessageWithMention(msg.to,target,"Maaf","aku kick")
                                            klist = [cl]
                                            kicker = random.choice(klist)
                                            kicker.kickoutFromGroup(msg.to,[target])
                                        except:
                                            pass 
                        elif "adminadd " in text.lower():
                            if msg._from in RAOwner:
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           Setmain["RAAdmin"][target] = True
                                           cl.sendMessage(msg.to,"Berhasil menambahkan admin")
                                       except:
                                           pass
                        elif "staffadd " in text.lower():
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           Setmain["RAStaff"][target] = True
                                           cl.sendMessage(msg.to,"Berhasil menambahkan staff")
                                       except:
                                           pass
                        elif "botadd " in text.lower():
                            if msg._from in RAOwner:
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           Setmain["RABots"][target] = True
                                           cl.sendMessage(msg.to,"Berhasil menambahkan bots")
                                       except:
                                           pass
                        elif ". " in text.lower():
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:                            
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           Setmain["blaclist"][target] = True
                                       except:
                                           pass                                        
                        elif "botdell " in text.lower():
                            if msg._from in RAOwner:
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           del Setmain["RABots"][target]
                                           cl.sendMessage(msg.to,"Berhasil menghapus bots")
                                       except:
                                           pass
                        elif "admindell " in text.lower():
                            if msg._from in RAOwner:
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           del Setmain["RAAdmin"][target]
                                           cl.sendMessage(msg.to,"Berhasil menghapus admin")
                                       except:
                                           pass
                        elif "staffdell " in text.lower():
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:    
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           del Setmain["RAStaff"][target]
                                           cl.sendMessage(msg.to,"Berhasil menghapus staff")
                                       except:
                                           pass
                        elif "Unban " in text.lower():
                            if msg._from in RAOwner or msg._from in Setmain["RAAdmin"]:                            
                               key = eval(msg.contentMetadata["MENTION"])
                               key["MENTIONEES"][0]["M"]
                               targets = []
                               for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                               for target in targets:
                                       try:
                                           del Setmain["blacklist"][target]
                                           cl.sendMessage(msg.to,"Berhasil menghapus blacklist")
                                       except:
                                           pass
                                        
                        elif "kick @α я" in text.lower():
                            if Setmain["larangan"] == True:                            
                                cl.sendMessageWithMention(msg.to, msg._from,"wooiiii","mau kick bosku ya")
                                cl.kickoutFromGroup(msg.to, [msg._from])
                        elif "dor @α я" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooiii","mau kick bosku ya")
                                cl.kickoutFromGroup(msg.to, [msg._from])                            
                            
                        elif "!kick @α я" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooii","mau kick bosku ya")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                            
                        elif ".kick @α я" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooii","mau kick bosku ya")
                                cl.kickoutFromGroup(msg.to, [msg._from])  
                        elif "!hust @α я" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau kick bosku ya")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif "kickal" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from])   
                        elif "kickall" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif ".kickal" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif "!kickal" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif ".hay" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif "!hai" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif "nuke" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from]) 
                        elif ".nuke" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")   
                        elif "!nuke" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")   
                        elif "kick" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")                                
                        elif "kibar" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from])  
                        elif "crash" in text.lower():
                            if Setmain["larangan"] == True:                             
                                cl.sendMessageWithMention(msg.to, msg._from,"wooyyyy","mau ngpin lu")
                                cl.kickoutFromGroup(msg.to, [msg._from])                             
                        elif '/ti/g/' in msg.text.lower():
                            if msg._from in RASuper:
                                link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                links = link_re.findall(msg.text)
                                n_links=[]
                                for l in links:
                                    if l not in n_links:
                                        n_links.append(l)
                                for ticket_id in n_links:
                                    if Setmain["autojoin"] == True:
                                        ra = cl.findGroupByTicket(ticket_id)
                                        cl.acceptGroupInvitationByTicket(ra.id,ticket_id)
                                        
                                    else:    
                                        cl.sendMessageWithMention(msg.to,msg._from,"Maaf","\naktifkan auotojoin dulu")

    except Exception as error:
        print (error)
        
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                oepoll.setRevision(op.revision)
                thread = threading.Thread(target=bot, args=(op,))
                thread.start()
    except Exception as e:
        print(e)
