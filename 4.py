import psycopg2


conn = psycopg2.connect(database= '', user= '', password= '')
with conn.cursor() as cur:
    def create_tables(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                pk SERIAL PRIMARY KEY,
                name VARCHAR(40),
                soname VARCHAR(40),
                email VARCHAR(40) UNIQUE NOT NULL 
                
            );
                    """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                pk SERIAL PRIMARY KEY,
                phone VARCHAR(15) UNIQUE NOT NULL,
                client_pk INTEGER NULL REFERENCES client(pk) 
            );
                    """)
        conn.commit()
    def insert_client(cur , name, soname, email, number= ''):
        cur.execute("""
            INSERT INTO client(name, soname, email) VALUES(%s, %s, %s);
                    """, (name, soname, email))
        conn.commit()
        if number != '':
            cur.execute("""
                    SELECT pk FROM client WHERE email=%s;
                        """, (email,))
            pk= cur.fetchone()
            cur.execute("""
                INSERT INTO phone(phone, client_pk) VALUES(%s, %s);
                        """, (number, pk))
            conn.commit()       
    def add_phone(cur, number: str, email):


        cur.execute("""
                SELECT pk FROM client WHERE email=%s;
                        """, (email,))
        pk= cur.fetchone()
        cur.execute("""
                INSERT INTO phone(phone, client_pk) VALUES(%s, %s);
                        """, (number, pk))
        conn.commit()
    def change_user(cur, email, name= '', soname= '', email_change= '', ): 
        if name != '':
            cur.execute("""
                UPDATE client
                SET  name=%s WHERE pk = (SELECT pk FROM client WHERE email=%s);
                        """,(name,email ))
            conn.commit()
        if soname != '':
            cur.execute("""
                UPDATE client
                SET  soname=%s WHERE pk = (SELECT pk FROM client WHERE email=%s);
                        """,(soname,email ))
            conn.commit()
        if email_change != '':
            cur.execute("""
                UPDATE client
                SET  email=%s WHERE pk = (SELECT pk FROM client WHERE email=%s);
                        """,(email_change,email ))
            conn.commit()
    def delete_phone(cur, number, email):# mail нужен для проверки пользователя, если юзер захочет удалить не свой номер телефона
        cur.execute("""
                DELETE FROM phone WHERE phone= %s AND client_pk = (SELECT pk FROM client WHERE email= %s);
                    """,(number, email))
    def delete_client(cur, email):
        cur.execute("""
                DELETE FROM phone WHERE client_pk = (SELECT pk FROM client WHERE email= %s);
                    """,(email,))
        conn.commit()
        cur.execute("""
                DELETE FROM client WHERE email= %s;
                    """,(email, ))
        conn.commit()
    def search_client_phone(cur, number): 
        cur.execute("""
                SELECT pk, name, soname, email FROM client WHERE pk= (SELECT client_pk FROM phone WHERE phone= %s)
                    """,(number,))
        client= cur.fetchone()
        return client
    def search_client_all(cur, name, soname, email):#все три обязательных, т.к будут повторы(я бы вообще только по почте делал, но дз требует всего)
        cur.execute("""
                SELECT pk, name, soname, email FROM client WHERE name=%s AND soname= %s AND email= %s
                    """,(name, soname, email))
        client= cur.fetchone()
        return client #вывод вообще почти такой же, какой и ввод, но будь в бд больше данных, было бы полезней 
    #2 последние функции не объединил, потому что должны были быть обязательные параметры для предотвращения повторов, думаю и так сойдет
    
conn.close() 








   #  cur.execute("""SELECT pk FROM phone WHERE phone= %s;""", (number,))
           # phone= cur.fetchone()
           # cur.execute("""SELECT pk FROM client WHERE name= %s;""",(name,))
           # name_client= cur.fetchone()
           # cur.execute("""
           #     INSERT INTO clientphone(client, phone) VALUES(%s, %s);
           #             """,(name_client, phone))
         #   conn.commit()


             #    cur.execute("""
     #       CREATE TABLE IF NOT EXISTS clientphone(
     #           client INTEGER REFERENCES client(pk),
	  #          phone INTEGER REFERENCES phone(pk),
	  #          CONSTRAINT id_cp PRIMARY KEY (phone, client)
      #      );
       #             """)