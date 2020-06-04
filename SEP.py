#!/usr/local/bin/python3
# -*- coding: utf8 -*-
import requests
import hashlib
from datetime import datetime, timedelta
import os
#import win32api
#import win32net


class UpdateAPI():
    def __init__(self, product_type):
        today = datetime.now().strftime("%Y-%m-%d")
        self.api = f"https://www.broadcom.com/api/getjsonbyurl?vanityurl=support/security-center/definitions/download/detail&locale=avg_en&updateddate={today}-12:18:16&gid={product_type}"
        self.suitable_day = "{}/{}/{}".format((datetime.now() - timedelta(days=1)).month, (datetime.now() - timedelta(days=1)).day, (datetime.now() - timedelta(days=1)).year)
        self.download_folder = " " # Folder path

    def checkHash(self, file_name):
        md5_hash = hashlib.md5()
        a_file = open(file_name, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return digest.upper()

    def check(self):
        resp = requests.get(self.api).json()
        resp_with_type = resp.get('groups')[0].get('packages')
        for i in resp_with_type:
            file_download_link = i.get('file').get('ftp_url_')
            if file_download_link.endswith('.jdb'):
                allowed = ['_14_0.jdb', '15sds.jdb', 'IU_SEP.jdb']
                is_correct = False
                for correction in allowed:
                    if file_download_link.endswith(correction):
                        is_correct = True
                        break
                if not is_correct:
                    continue
                file_md5 = i.get('file').get('md5')
                released = i.get('file').get('release_date')
                file_name = file_download_link.split('/')[-1]
                print("File Download Path: " + file_download_link)
                print('-'*100)
                print("File Hash on Web: " + file_md5)
                print("File Release Date: " + released)
                print("Only downloads when date is: " + self.suitable_day)
                if released == self.suitable_day:
                    # this is a perfect day to download the update
                    print("Download initiated due to perfect date match!")
                    with open(self.download_folder + file_name, 'wb+') as downloaded_file:
                        downloaded_file.write(requests.get(file_download_link, stream=True).content)
                    print(f"{file_name} has been downloaded and hash checking is being processed ...")
                    if self.checkHash(self.download_folder + file_name) == file_md5:
                        print("File hash is healthy!")
                    else:
                        print("Hash mismatch!")
                break


if __name__ == "__main__":
    updateDownloader = UpdateAPI("sep14")
    updateDownloader.check()
    updateDownloader = UpdateAPI("ips14")
    updateDownloader.check()
    updateDownloader = UpdateAPI("sonar")
    updateDownloader.check()
    ip = '192.168.1.18' #remote ip
    username = 'ram' # change to input("Username: ")
    password = 'ram@123' # change to input("Password: ")
    '''use_dict={}
    use_dict['remote']=unicode('\\\\{}\C$'.format(ip))
    use_dict['password']=unicode(password)
    use_dict['username']=unicode(username)
    win32net.NetUseAdd(None, 2, use_dict)'''
