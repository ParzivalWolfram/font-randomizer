#fairly standard imports, just with Very Funny Changed Names to piss off the two people who ever actually read this
from os import system as run
from time import sleep as wait
from random import choice as choose
from random import randint as roll

#settings and whatnot
debug = True #if true, print what it set everything to and how many iterations have gone by so far
targetCount = 1024 #set to negative number to infinitely spin, something something -1 rule
waitTime = 15 #time between changes
restoreFile = "/home/parzival/.cache/tester.12" #stick a path to a backup of the font vars from dconf here and it'll restore them after
minFontSize = 7 #these two are pretty self explanatory, set to preference
maxFontSize = 14 #these are my preferences, as some of the default fonts are fucking MASSIVE dude

#done for faster development, fuck with it if you want i guess, idk, i'm not your boss
#yes, we use /tmp for storing files. Why? We don't need permanent storage and deleting files
#causes disk I/O, which is slightly more important nowadays, since SSDs wear and all.
fetchCommand = "fc-list --format=\"'%{family[0]} %{style[0]}\\n\" > /tmp/fontlist.ass"
fetchDeleteCommand = "rm -f /tmp/fontlist.ass"
applyCommand = "dconf load /org/ < /tmp/newsettings.ass"
applyDeleteCommand = "rm -f /tmp/newsettings.ass"
fixCommand = "dconf load /org/ < "+str(restoreFile)

#begin the trash
run(fetchCommand)
fontListFile = open("/tmp/fontlist.ass","r")
fontList = fontListFile.readlines()
fontListFile.close()
run(fetchDeleteCommand) #trying not to clutter /tmp
fontListTemp = []
for i in fontList: #this is part of allowing for sizes, because i'm stupid and can't think of a better way to do this
        fontListTemp.append(i.strip("\n"))
fontList = fontListTemp
del fontListTemp #freeing ram is my passion

#this is Cinnamon-specific and very very ugly, change to accomodate your DE/WM
partHeaders = ["[cinnamon/desktop/interface]\nfont-name=","[cinnamon/desktop/wm/preferences]\ntitlebar-font=","[gnome/desktop/interface]\ndocument-font-name=","[gnome/gedit/preferences/print]\nprint-font-body-pango=","print-font-header-pango=","print-font-numbers-pango=","[nemo/desktop]\nfont="]

loopnum = 1
try:
        while loopnum != targetCount:
                outputFile = open("/tmp/newsettings.ass","w")
                arrayBuffer = []
                for i in partHeaders:
                        arrayBuffer.append(i+choose(fontList)+" "+str(roll(minFontSize,maxFontSize))+"'\n")
                if debug:
                        print("Iteration: "+str(loopnum))
                        print("File contents:")
                        print("=====================================") #these make it look a little nicer, imo
                for i in arrayBuffer:
                        print(i)
                        outputFile.write(i)
                if debug:
                        print("=====================================")
                outputFile.flush()
                outputFile.close()
                run(applyCommand)
                run(applyDeleteCommand) #trying to not clutter /tmp
                wait(waitTime)
                loopnum += 1
except:
        print("Stop requested or error occured, restoring from backup...")
finally:
        run(fixCommand)
