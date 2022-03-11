import datetime
import os
import random
import time
import glob
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonOther
from apicred import api__id, api__hash

app = None
session_name = ""

while True:
    os.system("cls")
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
        exit()

app = Client(session_name, api__id, api__hash)
app.start()
msg = "Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainian citizens and soldiers."

while True:
    os.system("cls")
    print("Current session: " + session_name)
    t_lists = glob.glob("*.targets")
    if len(t_lists) > 0:
        print("Available targets lists:")
        for i in range(0, len(t_lists)):
            print("[" + str(i) + "] - " + t_lists[i][:-8])
    print ("[A] - Add new target(s)")
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
    elif res.lower() == "a":
        target = input("Enter target: ")
        targets.append(target)
    elif res.lower() == "q":
        app.stop()
        break
    if len(targets) > 0:
        reports_count = int(input("Enter reports count: "))
        t_peers = []
        for target in targets:
            t_target = target.replace("\n", "")
            i_start = max(0, t_target.find("t.me/") + 5)
            i_end = -1
            i_end = t_target.find("/", i_start)
            if i_end == -1:
                i_end == len(t_target)
            p_target = t_target[i_start:i_end]
            t_peer = None
            try:
                t_peer = app.resolve_peer(p_target)
            except:
                pass
            time.sleep(1)
            if t_peer is not None:
                print("Target [" + p_target + "] locked.")
                t_peers.append([p_target, t_peer, 0])
            else:
                print("Target [" + p_target + "] not resolved.")
        input("\033[15;0HEnter to continue...")
        os.system("cls")
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
                        random.seed()
                        queue = random.randint(1, 5)
                        if queue > reports_count - t_peers[i_peer][2]:
                            queue = reports_count - t_peers[i_peer][2]
                        for i in range(0, queue):
                            s = app.send(ReportPeer(peer = t_peers[i_peer][1], reason = InputReportReasonOther(), message = msg))
                            time.sleep(1)
                            if s:
                                t_peers[i_peer][2] += 1
                                print("\033[" + str(3 + i_peer) + ";0H" + t_peers[i_peer][0] + "\033[30G" + str(t_peers[i_peer][2]) + "/" + str(reports_count))

                if finish:
                    break
            dt_end = datetime.datetime.now()
            print("\033[" + str(3 + len(t_peers)) + ";0H[" + dt_end.strftime("%d.%m.%Y %H:%M:%S") + "] Done in " + str(dt_end - dt_begin) + ".")
        else:
            pass
        input("\033[16;0HEnter to continue...")

        # for i in range(0, len(targets)):
        #     p_target = targets[i].replace("\n", "")
        #     t_peer = app.resolve_peer(p_target)
        #     if t_peer is not None:
        #         print("Target [" + p_target + "] locked.")
        #         reports_successful = 0
        #         print("Bombing target...")
        #         s = True
        #         while True:
        #             s = app.send(ReportPeer(peer = t_peer, reason = InputReportReasonOther(), message = msg))
        #             if s:
        #                 reports_successful += 1
        #                 print("Reports: " + str(reports_successful) + "/" + str(reports_count), end="\r")
        #                 if reports_successful >= reports_count:
        #                     print("\nAll reports sent.")
        #                     break
        #             else:
        #                 print("\nSending report failed.")
        #                 break
        #             time.sleep(1)
        #         print("Bombing ended.")
        #     else:
        #         print("Target [" + p_target + "] not resolved.")
        # input("Done.")