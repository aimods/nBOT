global logfolder
global logfilename
global db
global LoginMethod
global LineLogin
global LinePassword
global LineToken
global check_in
global pidid
global botowner
global NAIBOSS

global ReREGIS
global ErrMSG


logfolder = '/var/log/nai'
logfilename = '%s/nai.log'%logfolder

db    = ['localhost',           #
         'NaiBot',              # Username
         '**************',      # Password
         'NaiBot',              # Database
         'utf8mb4']             # Charset // utf8 will not support Emojicon << Please don't edit this line //

LoginMethod = 0                 # 0 = Username
                                # 1 = Token

LineLogin = "*********"
LinePassword = "********"

LineToken = ""

encKey = "************"

NAIBOSS = "****************"
pidid = NAIBOSS  # bot LINE mid
botowner = "**************"


#======= UX ========#

ReREGIS = "HELP\n==========\n /reg <username> <Password>\n Contact %s \n for more information" % botowner


ErrMSG = {
    0 : "We can't process your request at this moment.\nPlease wait a minute and try again\nIf you are login from LINE PC, Please logout and login agian",
    1 : "Task complete",
    #1xxx - database.py
    #10xx - _Register
    1001: "Only accept [A-Z], [a-z] anf [0-9]",
    1002: "Username is not avilable",
    1003: "You only can have one account.\nPlease use\n  \"/forgot user\" to retive your Username \n  \"/forgot passwd\" to reset Password",
    1004: "Thanks for your registation but currently we are not accept the new user",
    1005: "Welcome new NAI member\nlearn more about us at \nhttps://www.mods.in.th/linebot",
    1006: "Good bye you will no longer got any messsage from us. \n We very sad to hear that but you can\n\n%s" % ReREGIS,
    2001: "Can't update send message status",
    3001: "We need 13 digit Thai national ID, or 13 digit TAX ID\nPlease type /id <13 digit ID>",
    3002: "You are verification member",
    3003: "Sorry, we can't verify your ID.\nPlease contact %s for further support" % botowner,
    3004: "To start verify process please use /verify",
    3005: "Thank you for verification\n Next step: \nplease send your photocopy of your ID for reference.\n\nContact %s for more information" % botowner,
}


