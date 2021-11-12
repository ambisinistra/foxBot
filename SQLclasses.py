import sqlite3
import datetime
import logging

class SQLdb():
    def kwargs_to_str(self, kwargs):
        output = ""
        kw_keys = list(kwargs.keys())
        kw_len = len(kw_keys)
        for i,key in enumerate(kw_keys):
            output += str(kw_keys[i]) + ' '
            if i == (kw_len - 1):
                output += str(kwargs[key])
            else:
                output += str(kwargs[key]) + ', '
        return output

    def __init__(self, database_name="typical_db", **kwargs):
        self.connection = sqlite3.connect(database_name)
        self.name = database_name
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS {} ({});".format(self.name, self.kwargs_to_str(kwargs))
        #logging.debug(query)
        self.cursor.execute(query)
        self.keys = kwargs.keys()

    def record_by_chat_id(self, chat_id: int):
        with self.connection:
            query = "SELECT * FROM {} WHERE  chat_id = '{}';".format(self.name, chat_id)
            #logging.debug(query)
            raw_result = self.cursor.execute(query).fetchall()
            result = []
            #converting (tuple of sql answer) to dict
            for row in raw_result:
                result.append(dict(zip(self.keys, row)))
            return (result)

    def __len__(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM {};".format(self.name)).fetchall()
            return len(result)
    
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
        
class SQLmessages(SQLdb):
    def __init__(self, database_name="messages"):
        super().__init__(database_name=database_name, message_id="integer", chat_id="integer",
                        begin_date="datetime", message_text="text", message_type="text")
    
    def record_by_type(self, chat_id : int, message_type : str):
        with self.connection:
            query = "SELECT * FROM {} WHERE  chat_id = '{}' AND message_type = '{}';".format(self.name, chat_id, message_type)
            #logging.debug(query)
            raw_result = self.cursor.execute(query).fetchall()
            result = []
            #converting (tuple of sql answer) to dict
            for row in raw_result:
                result.append(dict(zip(self.keys, row)))
            return (result)

    def check_old_messages(self, time_diff : str):
        with self.connection:
            raw_result = self.cursor.execute("SELECT * FROM {} WHERE begin_date < '{}'".format(self.name, time_diff)).fetchall()
            result = []
            #converting (tuple of sql answer) to dict
            for row in raw_result:
                result.append(dict(zip(self.keys, row)))
            return (result)

    def insert_record(self, chat_id: int, message_id: int, message_text="", message_type="default"):
        with self.connection:
            current_time = datetime.datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO {}(chat_id, message_id, message_text, begin_date, message_type) VALUES(?,?,?,?,?);".format(self.name),
                                (chat_id, message_id, message_text, current_time, message_type))
        return (0)

    def delete_record(self, chat_id: int, message_id: int):
        """ Удаляем строку с устаревшим сообщением """
        with self.connection:
            result = self.cursor.execute("DELETE FROM {} WHERE chat_id = '{}' AND message_id = '{}';".format(self.name, chat_id, message_id))
        return (result)

class SQLchatsGreatings(SQLdb):
    def __init__(self, database_name="welcome_animations"):
        super().__init__(database_name=database_name, chat_id="integer", animation_link="text", welcome_message="text", capcha="bool", begin_date="datetime")
    
    def delete_record(self, chat_id: int):
        """ Удаляем все строки с таким chat_id"""
        with self.connection:
            result = self.cursor.execute("DELETE FROM {} WHERE chat_id = '{}';".format(self.name, chat_id))
            return (result)

    def update_record(self, chat_id: int, animation_link="", welcome_text="", capcha=None):
        with self.connection:
            current_time = datetime.datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print ("UPDATING record for CHAT", chat_id)
            last_record = self.record_by_chat_id(chat_id)
            #logging.debug(last_record)
            query = "INSERT INTO {} (chat_id, animation_link, welcome_message, capcha, begin_date) VALUES(?,?,?,?,?);".format(self.name)
            if len(last_record) > 0:
                print ("THERE was record for", chat_id)
                self.delete_record(chat_id)
                print ("IT was DELETED")
                if capcha == None:
                    capcha_to_replace = last_record[0]["capcha"]
                else:
                    capcha_to_replace = capcha
                # logging.debug(last_record)
                self.cursor.execute(query, (chat_id, animation_link or last_record[0]["animation_link"], welcome_text or last_record[0]["welcome_message"],
                                    capcha_to_replace, current_time))
            else:
                self.cursor.execute(query, (chat_id, animation_link, welcome_text, capcha, current_time))
        return (last_record)

class SQLmembers(SQLdb):
    def __init__(self, database_name="members"):
        super().__init__(database_name=database_name, chat_id="int", user_id="int", status="text", message_id="int", begin_date="datetime")

    def add_member(self, chat_id:int, user_id:int, status:str, message_id:int):
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        with self.connection:
            self.cursor.execute("INSERT INTO {} (chat_id, message_id, user_id, status, begin_date) VALUES(?,?,?,?,?);".format(self.name), (chat_id, message_id, user_id, status, current_time))

    def delete_record(self, chat_id: int, user_id: int):
        """ Удаляем строку с устаревшим сообщением """
        with self.connection:
            self.cursor.execute("DELETE FROM {} WHERE chat_id = '{}' AND user_id = '{}';".format(self.name, chat_id, user_id))

    def check_old_messages(self, time_diff : str, status="awaiting"):
        with self.connection:
            raw_result = self.cursor.execute("SELECT * FROM {} WHERE begin_date < '{}' AND status ='{}'".format(self.name, time_diff, status)).fetchall()
            result = []
            #converting (tuple of sql answer) to dict
            for row in raw_result:
                result.append(dict(zip(self.keys, row)))
            return (result)