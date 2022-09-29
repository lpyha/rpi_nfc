import binascii
import datetime
import csv
import json
import nfc
import traceback

NFC_A = nfc.clf.RemoteTarget("106A")
NFC_B = nfc.clf.RemoteTarget("106B")
FELICA = nfc.clf.RemoteTarget("212F")

IDM_LIST_PATH = "./cfg/idm_list.json"
RECORD_PATH = "./record/record.csv"

def get_idm(first_remote_target, second_remote_target):
    with nfc.ContactlessFrontend("usb") as clf:
        print("touch card:")
        while True:
            target = clf.sense(first_remote_target, second_remote_target, iterations=5, interval=0.2)
            if target is not None:
                tag = nfc.tag.activate(clf, target)
                idm = binascii.hexlify(tag.identifier).hex()
                break
    return idm


def get_name_from_idm_list(idm, idm_path):
    with open(f"{idm_path}") as f:
        member = json.load(f)
        for key in member:
            if (idm == key):
                name = member[key]
                break
            else:
                name = "UNKNOWN"
    return name


def record_to_csv(name, idm, record_path):
    dt = datetime.datetime.today()
    with open(f"{record_path}", 'a', encoding="utf-8", newline="") as f:
        record = csv.writer(f)
        record.writerow(name, idm, dt.year, dt.month, dt.day, dt.hour, dt.minute)
    

def main():
    try:
        while True:
            idm = get_idm(first_remote_target=NFC_A, second_remote_target=FELICA)
            name = get_name_from_idm_list(idm=idm, idm_path=IDM_LIST_PATH)
            record_to_csv(name=name, idm=idm, record_path=RECORD_PATH)
    except Exception:
        print(traceback.format_exc())
        
        
if __name__ == '__main__':
    main()