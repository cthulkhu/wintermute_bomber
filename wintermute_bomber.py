import datetime
import msvcrt
import os
import random
import sys
import time
import glob
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonOther

if not os.path.exists("settings.conf"):
    print("No settings.conf file found.")
    print("Generating blank settings.conf...")
    with open("settings.conf", "w") as f_settings:
        f_settings.write("# https://my.telegram.org/apps\n")
        f_settings.write("# api__id = \n")
        f_settings.write("# api__hash = \n")
        print("Done. Have a look into it.")
    sys.exit()

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
border_top = 4
fstop = 3
msg = "Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainian citizens and soldiers."
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

while True:
    os.system(clrscr)
    print(session_name + ".session")
    t_lists = glob.glob("*.targets")
    if len(t_lists) > 0:
        print("Available targets lists:")
        for i in range(0, len(t_lists)):
            print("[" + str(i) + "] - " + t_lists[i][:-8])
    print ("[C] - Custom single target")
    print ("[Q] - Quit")
    targets = []
    res = input("[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "] Select target(s): ")
    tlist_name = "Custom"
    if res.isnumeric():
        if len(t_lists) > 0:
            if len(t_lists) > 0:
                if int(res) >= 0:
                    if int(res) < len(t_lists):
                        with open(t_lists[int(res)]) as listfile:
                            targets = listfile.readlines()
                            tlist_name = t_lists[int(res)]
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
            t_target = target.strip(" \n")
            i_start = t_target.find("t.me/") + 5
            if i_start == 4:
                i_start = 0
            i_end = t_target.find("/", i_start)
            if i_end == -1:
                i_end = len(t_target)
            p_target = t_target[i_start:i_end]
            if p_target == "":
                continue
            if p_target.startswith("+"):
                continue
            if p_target.startswith("joinchat"):
                continue
            dup = False
            for t_peer in t_peers:
                if t_peer[0] == p_target:
                    dup = True
                    break
            if dup:
                continue
            print("Target [" + p_target + "]:\033[30G\33[33msearching...\33[0m", end = "\r")
            t_peer = None
            try:
                t_peer = app.resolve_peer(p_target)
            except:
                t_peer = None
            time.sleep(1)
            if t_peer is not None:
                print("Target [" + p_target + "]:\033[30G\33[32mlocked.\33[0m\33[K")
                t_peers.append([p_target, t_peer, 0, 0, 0]) # [string name, InputPeer peer, int reports_successful, int reports_failed, int fails_sequence]
            else:
                print("Target [" + p_target + "]:\033[30G\33[31mnot resolved.\33[0m\33[K")
        input("Enter to continue...")
        os.system(clrscr)

        print(session_name + ".session " + tlist_name)
        if len(t_peers) > 0:
            reports_tcount = len(t_peers) * reports_count
            reports_tsent = 0
            reports_tfailed = 0
            dt_begin = datetime.datetime.now()
            print("[" + dt_begin.strftime("%d.%m.%Y %H:%M:%S") + "] Start bombing.")
            print("\033[3;0H[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "] \33[32m" + str(reports_tsent) + "\33[0m/\33[31m" + str(reports_tfailed) + "\33[0m/" + str(reports_tcount) + "\33[K")
            for t_peer in t_peers:
                print(t_peer[0] + "\033[30G\33[32m" + str(t_peer[2]) + "\33[0m/\33[31m" + str(t_peer[3]) + "\33[0m/" + str(reports_count))

            while True:
                finish = True
                for i_peer in range(0, len(t_peers)):
                    if t_peers[i_peer][2] < reports_count:
                        if t_peers[i_peer][4] < fstop:
                            finish = False
                            if not random.randint(0, 3):
                                queue = random.randint(1, 5)
                                if queue > reports_count - t_peers[i_peer][2]:
                                    queue = reports_count - t_peers[i_peer][2]
                                for i in range(0, queue):
                                    s = False
                                    try:
                                        s = app.send(ReportPeer(peer = t_peers[i_peer][1], reason = InputReportReasonOther(), message = msg))
                                        time.sleep(1)
                                    except:
                                        s = False
                                    if s:
                                        t_peers[i_peer][2] += 1
                                        t_peers[i_peer][4] = 0
                                        reports_tsent += 1
                                    else:
                                        t_peers[i_peer][3] += 1
                                        t_peers[i_peer][4] += 1
                                        reports_tfailed += 1

                                    print("\033[3;0H\33[K\r[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "] \33[32m" + str(reports_tsent) + "\33[0m/\33[31m" + str(reports_tfailed) + "\33[0m/" + str(reports_tcount) + "\33[K")
                                    if t_peers[i_peer][2] >= reports_count:
                                        print("\033[" + str(border_top + i_peer) + ";0H\33[K\r\33[32m" + t_peers[i_peer][0] + "\33[0m\033[30G\33[32m" + str(t_peers[i_peer][2]) + "\33[0m/\33[31m"  + str(t_peers[i_peer][3]) + "\33[0m/" + str(reports_count) + "\033[40G" + ("\33[31m!\33[0m" * t_peers[i_peer][4]) + "\033[50G" + ("\33[32m#\33[0m" * int(20 * t_peers[i_peer][2] / reports_count)))
                                        break
                                    if t_peers[i_peer][4] >= fstop:
                                        print("\033[" + str(border_top + i_peer) + ";0H\33[K\r\33[31m" + t_peers[i_peer][0] + "\33[0m\033[30G\33[32m" + str(t_peers[i_peer][2]) + "\33[0m/\33[31m"  + str(t_peers[i_peer][3]) + "\33[0m/" + str(reports_count) + "\033[40G" + ("\33[31m!\33[0m" * t_peers[i_peer][4]) + "\033[50G" + ("\33[31m#\33[0m" * int(20 * t_peers[i_peer][2] / reports_count)))
                                        break
                                    print("\033[" + str(border_top + i_peer) + ";0H\33[K\r" + t_peers[i_peer][0] + "\033[30G\33[32m" + str(t_peers[i_peer][2]) + "\33[0m/\33[31m"  + str(t_peers[i_peer][3]) + "\33[0m/" + str(reports_count) + "\033[40G" + ("\33[31m!\33[0m" * t_peers[i_peer][4]) + "\033[50G" + ("#" * int(20 * t_peers[i_peer][2] / reports_count)))

                    if msvcrt.kbhit():
                        ch = str(msvcrt.getch())
                        if ch == "b'p'":
                            print("\033[1;50H[" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "]")
                            act = input("\033[2;50HPaused. [C]ontinue/[Q]uit?")
                            if act.lower() == "q":
                                finish = True
                                break
                            print("\033[1;50H\33[K")
                            print("\033[2;50H\33[K")

                if finish:
                    break

            dt_end = datetime.datetime.now()
            print("\033[" + str(border_top + len(t_peers)) + ";0H[" + dt_end.strftime("%d.%m.%Y %H:%M:%S") + "] Done in " + str(dt_end - dt_begin) + ".")

        else:
            print("No peers.")

        input("Enter to continue...")
