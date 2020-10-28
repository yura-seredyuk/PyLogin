import mysql.connector

if __name__ == "__main__":
    db_manager


class db_manager:
    def __init__(self, host, user, password):
        self.__db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS pylogin")
        self.__cursor.execute("USE pylogin")
        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64), email VARCHAR(128), password VARCHAR(2048))")

    def menu(self):
        exit = False
        while not exit:
            choice = int(input(
                "1. Register\n2. Login\n3. Edit\n4. Delete\n5. Show all users\n6. Search by email\n0. Exit\n==> "))
            if choice == 1:
                answer = self.__register()
                print(answer)
            elif choice == 2:
                answer = self.__login()
                print(answer)
            elif choice == 3:
                answer = self.__edit()
                print(answer)
            elif choice == 4:
                answer = self.__delete()
                print(answer)
            elif choice == 5:
                answer = self.__show_all()
                print(answer)
            elif choice == 6:
                answer = self.__show_email()
                print(answer)
            elif choice == 0:
                exit = True
                print("Bye!")
            else:
                print("Wrong choise")

    def __register(self):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            return "Password do not match!"

        self.__cursor.execute(
            f"SELECT email FROM users WHERE email = '{email}'")
        result = self.__cursor.fetchone()
        if result != None:
            return "User exists"
        else:
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            val = (username, email, password)
            self.__cursor.execute(sql, val)
            self.__db.commit()
            return "User successfully created!"

    def __login(self):
        email = input("Email: ")
        password = input("Password: ")

        self.__cursor.execute(
            f"SELECT username FROM users WHERE email = '{email}' AND password = '{password}'")
        result = self.__cursor.fetchone()
        if result != None:
            return f"Hello {''.join(result)}!"
        else:
            return "Wrong email or password! Please try again."

    def __edit(self):
        email = input("Email: ")
        password = input("Password: ")

        self.__cursor.execute(
            f"SELECT username, email, password FROM users WHERE email = '{email}' AND password = '{password}'")
        result = self.__cursor.fetchone()
        if result != None:
            username, *result = result
            print(f"Hello {username}! Plese enter new data to your account:")
            username = input("Username: ")
            new_email = input("Email: ")
            password = input("Password: ")
            self.__cursor.execute(
                f"UPDATE users SET username = '{username}', email = '{new_email}', password = '{password}' WHERE email = '{email}'")
            self.__db.commit()
            return f"{username}, your data is updated!"
        else:
            return "Wrong email or password! Please try again."

    def __delete(self):
        email = input("Email: ")
        password = input("Password: ")

        self.__cursor.execute(
            f"SELECT username FROM users WHERE email = '{email}' AND password = '{password}'")
        result = self.__cursor.fetchone()
        if result != None:
            self.__cursor.execute(f"DELETE FROM users WHERE email = '{email}'")
            self.__db.commit()
            return f"Hello {''.join(result)}! Your data has been deleted."
        else:
            return "Wrong email or password! Please try again."

    def __show_all(self):
        self.__cursor.execute(
            f"SELECT username, email FROM users")
        result = self.__cursor.fetchall()
        if result != []:
            print('Username'.center(20, '='), 'Email'.center(20, '='), sep='|')
            for username, email in result:
                print("%20s%20s" % (username, email))

            return f"All users!"
        else:
            return "No data!"

    def __show_email(self):
        email = input("Enter email: ")

        self.__cursor.execute(
            f"SELECT username, email FROM users WHERE email = '{email}'")
        result = self.__cursor.fetchall()
        if result != []:
            print('Username'.center(20, '='), 'Email'.center(20, '='), sep='|')
            for username, email in result:
                print("%20s%20s" % (username, email))
            return f"User with email: {email}!"
        else:
            return "No data."
