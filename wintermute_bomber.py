import datetime
import os
import random
import sys
import time
import glob
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonOther

api__id = ""
api__hash = ""
a_settings = []
with open("settings.conf") as f_settings:
    a_settings = f_settings.readlines()
for line in a_settings:
    if line.startswith("api__id"):
        api__id = line.replace("api__id", "").strip(" =\n")
    if line.startswith("api__hash"):
        api__hash = line.replace("api__hash", "").strip(" =\n")
if api__id == "":
    print("No api__id found in settings.conf.")
    sys.exit()
if api__hash == "":
    print("No api__hash found in settings.conf.")
    sys.exit()

app = None
session_name = ""
clrscr = "cls"
if os.name == "posix":
    clrscr = "clear"
random.seed()

while True:
    os.system(clrscr)
    sessions = glob.glob("*.session")
    if len(sessions) > 0:
        print("\nAvailable sessions:")
        for i in range(0, len(sessions)):
            print("[" + str(i) + "] - " + sessions[i][:-8])
    print("[C] - Create new session")
    print("[Q] - Quit")
    res = input("[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "] Select session: ")
    if res.isnumeric():
        if len(sessions) > 0:
            if int(res) >= 0:
                if int(res) < len(sessions):
                    session_name = sessions[int(res)][:-8]
                    break
    elif res.lower() == "c":
        session_name = input("Enter new session name: ")
        app = Client(session_name, api__id, api__hash, hide_password = True)
        app.start()
        app.stop()
    elif res.lower() == "q":
        sys.exit()

app = Client(session_name, api__id, api__hash)
app.start()
msg = "Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainian citizens and soldiers."

while True:
    os.system(clrscr)
    print("Current session: " + session_name)
    t_lists = glob.glob("*.targets")
    if len(t_lists) > 0:
        print("Available targets lists:")
        for i in range(0, len(t_lists)):
            print("[" + str(i) + "] - " + t_lists[i][:-8])
    print ("[C] - Custom single target")
    print ("[Q] - Quit")
    targets = []
    res = input("[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "] Select target(s): ")
    if res.isnumeric():
        if len(t_lists) > 0:
            if len(t_lists) > 0:
                if int(res) >= 0:
                    if int(res) < len(t_lists):
                        with open(t_lists[int(res)]) as listfile:
                            targets = listfile.readlines()
    elif res.lower() == "c":
        target = input("Enter target: ")
        targets.append(target)
    elif res.lower() == "q":
        app.stop()
        break
    if len(targets) > 0:
        reports_count = int(input("Enter reports count (per target): "))
        t_peers = []
        for target in targets:
            t_target = target.strip("\n")
            i_start = t_target.find("t.me/") + 5
            if i_start == 4:
                i_start = 0
            i_end = t_target.find("/", i_start)
            if i_end == -1:
                i_end = len(t_target)
            p_target = t_target[i_start:i_end]
            t_peer = None
            try:
                t_peer = app.resolve_peer(p_target)
            except:
                pass
            if random.randint(0, 1):
                time.sleep(1)
            if t_peer is not None:
                print("Target [" + p_target + "] locked.")
                t_peers.append([p_target, t_peer, 0])
            else:
                print("Target [" + p_target + "] not resolved.")
        input("Enter to continue...")
        os.system(clrscr)
        print("Current session: " + session_name)
        if len(t_peers) > 0:
            dt_begin = datetime.datetime.now()
            print("[" + dt_begin.strftime("%d.%m.%Y %H:%M:%S") + "] Start bombing.")
            for t_peer in t_peers:
                print(t_peer[0] + "\033[30G" + str(t_peer[2]) + "/" + str(reports_count))
            while True:
                finish = True
                for i_peer in range(0, len(t_peers)):
                    if t_peers[i_peer][2] < reports_count:
                        finish = False
                        queue = random.randint(1, 5)
                        if queue > reports_count - t_peers[i_peer][2]:
                            queue = reports_count - t_peers[i_peer][2]
                        for i in range(0, queue):
                            s = app.send(ReportPeer(peer = t_peers[i_peer][1], reason = InputReportReasonOther(), message = msg))
                            if random.randint(0, 1):
                                time.sleep(1)
                            if s:
                                t_peers[i_peer][2] += 1
                                print("\033[" + str(3 + i_peer) + ";0H" + t_peers[i_peer][0] + "\033[30G" + str(t_peers[i_peer][2]) + "/" + str(reports_count))
                if finish:
                    break
            dt_end = datetime.datetime.now()
            print("\033[" + str(3 + len(t_peers)) + ";0H[" + dt_end.strftime("%d.%m.%Y %H:%M:%S") + "] Done in " + str(dt_end - dt_begin) + ".")
        else:
            print("No peers.")
        input("Enter to continue...")
