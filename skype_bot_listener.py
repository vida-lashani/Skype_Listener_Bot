import pandas as pd
import pymysql.cursors
from skpy import Skype, SkypeEventLoop, SkypeNewMessageEvent, SkypeAuthException

from datetime import date
# enter your skype credentials
username = str('')
password = str('')
sk = Skype(username, password)
date_today = str(date.today())
ch = sk.chats["19:@thread"] # enter your skype group's id

class SkypeListener(SkypeEventLoop):
    def __init__(self):
        try:
            super(SkypeListener, self).__init__(username, password)
        except SkypeAuthException as e:
            print("Failed to authenticate with Skype:", e)
            raise Exception

    def Convert_to_list(self, string):
        return list(string.split(","))

    def get_pass_id(self, cell_phones):

        text_list = self.Convert_to_list(str(cell_phones))

        if len(text_list) == 1:
            pass_cellphone = "('" + str(cell_phones) + "')"
        elif len(text_list) > 1:
            pass_cellphone = tuple(set(text_list))
        print(pass_cellphone)
        connection = pymysql.connect(
            # enter your mysql db credentials
            host='',
            user='',
            password='',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cur:
                cur.execute("""
                select u.id,u.cellphone
                from users as u
                where u.cellphone IN {0}
                """.format(pass_cellphone))
                pass_Info = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
                print(pass_Info)
        finally:
            connection.close()

        return pass_Info

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and event.msg.chat.id == ch.id:
            default = "Skype listener: Investigate if you see this."
            message = {"user_id": event.msg.userId,
                       "chat_id": event.msg.chatId,
                       "msg": event.msg.content}
            print(message)
            text = str(event.msg.content.replace(" ", ""))
            list_phones = self.Convert_to_list(text)
            print(list_phones)
            if len(list_phones) == 1:
                if not list_phones[0].startswith("+98"):
                    event.msg.chat.sendMsg("Wrong cellphone format")

                else:
                    event.msg.chat.sendMsg("The message has a correct cellphone number")
                    pass_id = self.get_pass_id(text)
                    print(2)
                    event.msg.chat.sendMsg(str(pass_id['id'][0]))
                    print(1)
            elif len(list_phones) > 1:
                for j in range(len(list_phones)):
                    if not list_phones[j].startswith("+98"):
                        event.msg.chat.sendMsg("Wrong cellphone format")

                    else:
                        event.msg.chat.sendMsg("The message has correct cellphone numbers")
                        pass_id = self.get_pass_id(text)
                        for i in range(len(pass_id)):
                            event.msg.chat.sendMsg(str(pass_id['id'][i]))


if __name__ == "__main__":
    response = SkypeListener()
    response.loop()
