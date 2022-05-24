import sqlite3


class Database:
    """Класс для работы с БД"""
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def name_user(self, user_id):
        """Метод который выводит имя пользователя из БД"""
        for user in self.cursor.execute("SELECT user_name FROM exlab WHERE user_id = ?", (user_id,)):
            return user[0]

    def read_user(self, user_id, message):
        """Метод который выводит данные о пользователе из БД"""
        for user in self.cursor.execute("SELECT user_name, city FROM exlab WHERE user_id = ?", (user_id,)):
            return message.answer(f"Имя: {user[0]}\nГород: {user[1]}")
        else:
            return message.answer("Нет пользователя")

    def user_del(self, user_id):
        """Метод удаляющий юзера из БД"""
        with self.connection:
            return self.cursor.execute("DELETE FROM exlab WHERE user_id = ?", (user_id,))

    def add_user(self, user_id, teleg_user_name):
        """Метод для добавления нового юзера в таблицу БД и добавление его ника в телеграмм"""
        teleg_user_name = "@" + teleg_user_name
        with self.connection:
            return self.cursor.execute("INSERT INTO exlab (user_id, teleg_user_name) VALUES (?, ?)",
                                       (user_id, teleg_user_name,))

    def user_exists(self, user_id):
        """Метод, проверяет, существует ли такой юзер в таблице БД"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM exlab WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_username(self, user_id, user_name):
        """Метод, который добавляет имя юзера"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET user_name = ? WHERE user_id = ?", (user_name, user_id,))

    def birthday(self, user_id, date):
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET birthday = ? WHERE user_id = ?", (date, user_id,))

    def set_city(self, user_id, city):
        """Метод, который добавляет гоород юзера"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET city = ? WHERE user_id = ?", (city, user_id,))

    def set_speciality(self, user_id, speciality):
        """Метод, который добавляет специальность юзера.
        Специальность: front, back, design, etc."""
        if "speciality" in speciality:
            speciality = speciality[11::]
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET speciality = ? WHERE user_id = ?", (speciality, user_id,))

    def set_specialization(self, user_id, specialization):
        """Метод, который добавляет специализацию юзера.
        Специализация: на чём специализируется в работе, в каких программах работает"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET specialization = ? WHERE user_id = ?",
                                       (specialization, user_id,))

    def set_courses(self, user_id, courses):
        """Метод, который добавляет пройденные курсы или самоучка"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET courses = ? WHERE user_id = ?",
                                       (courses, user_id,))

    def set_eng(self, user_id, english):
        """Метод, который добавляет уровень владения английским"""
        english = english[-2::]
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET english = ? WHERE user_id = ?",
                                       (english, user_id,))

    def set_links(self, user_id, links):
        """Метод, который добавляет ссылки на линкедин или проекты"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET links = ? WHERE user_id = ?",
                                       (links, user_id,))

    def set_sourse(self, user_id, sourses):
        """Метод, который добавляет, откуда юзер узнал про ExLab"""
        if "source" in sourses:
            sourses = sourses[7::]
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET sourses = ? WHERE user_id = ?",
                                       (sourses, user_id,))

    def set_reason(self, user_id, reason):
        """Метод, который добавляет, причину регистрации в ExLab"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET reason = ? WHERE user_id = ?",
                                       (reason, user_id,))

    def set_idea(self,  user_id, idea):
        """Метод, который добавляет, есть ли идея, котоую хочет реализовать юзер"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET idea = ? WHERE user_id = ?",
                                       (idea, user_id,))

    def get_signup(self, user_id):
        """Метод, будет узнавать стадию регистрации пользователя"""
        with self.connection:
            result = self.cursor.execute("SELECT signup from exlab WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        """Метод, который изменяет стадию регистрации юзера"""
        with self.connection:
            return self.cursor.execute("UPDATE exlab SET signup = ? WHERE user_id = ?", (signup, user_id,))

