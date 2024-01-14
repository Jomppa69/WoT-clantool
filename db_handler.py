from db_conn import DB_CONN

class DbHandler:
    def __init__(self) -> None:
            return None


    # ----------HANDLING clan_wars_tanks TABLE----------
    def init_tank_database(self) -> None:
        cursor = DB_CONN.cursor()
        statement = self.__tanks_statement()
        print(statement)
        cursor.execute(statement)
        DB_CONN.commit()
        cursor.close()
        return None


    def __tanks_statement(self) -> str:
        statement =("""
            CREATE TABLE IF NOT EXISTS clan_wars_tanks(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tank_id NUMBER NOT NULL UNIQUE,
                type TEXT NOT NULL,
                is_premium BOOLEAN
            );
            """)
        
        return statement
    

    def add_tanks(self, cwTanks) -> None:
        cursor = DB_CONN.cursor()
        sql_statement = f"INSERT OR IGNORE INTO clan_wars_tanks(name, tank_id, type, is_premium) VALUES(?, ?, ?, ?)"
        for tank in cwTanks:
            cursor.execute(sql_statement, (cwTanks[tank]["name"], cwTanks[tank]["tank_id"], cwTanks[tank]["type"], cwTanks[tank]["is_premium"]))
        DB_CONN.commit()
        cursor.close()
        return None
    # ----------END OF HANDLING clan_wars_tanks TABLE----------
    
    #----------HANDLING clan_members & members_tanks TABLES----------

    def init_member_database(self) -> None:
        statements = self.__member_statement()
        cursor = DB_CONN.cursor()
        cursor.execute(statements[0])
        cursor.execute(statements[1])
        DB_CONN.commit()
        cursor.close()
        return None
    

    def __member_statement(self) -> str:
        statements = []
        statements.append("""
        CREATE TABLE IF NOT EXISTS clan_members(
        id INTEGER PRIMARY KEY,
        account_name TEXT NOT NULL,
        account_id NUMBER NOT NULL UNIQUE
        );
        """)

        statements.append("""
        CREATE TABLE IF NOT EXISTS members_tanks(
        id INTEGER PRIMARY KEY,
        account_id INTEGER NOT NULL,
        tank_id NUMBER NOT NULL,
        FOREIGN KEY(tank_id) REFERENCES clan_wars_tanks(tank_id)
        FOREIGN KEY(account_id) REFERENCES clan_members(id)
        );
        """)
        
        return statements


    def get_tank_ids(self): #-> List[int,int....]:
        tankIds = []
        cursor = DB_CONN.cursor()
        sql_query = "SELECT tank_id FROM clan_wars_tanks ORDER BY type ASC"
        cursor.execute(sql_query)
        ids = cursor.fetchall()
        for id in ids:
                tankIds.append(int(id[0]))
        DB_CONN.commit()
        cursor.close()
        return tankIds
    

    def add_clan_members(self, clanMembers) -> None:
        cursor = DB_CONN.cursor()
        cursor.execute("DELETE FROM clan_members")
        sql_statement = "INSERT OR IGNORE INTO clan_members(account_name, account_id) VALUES(?, ?)"
        for member in clanMembers:
                cursor.execute(sql_statement, (member["account_name"], member["account_id"]))
                member["rowId"] = cursor.lastrowid
        DB_CONN.commit()
        cursor.close()
        return None
    

    def write_member_tanks(self, clanMembers) -> None:
        cursor = DB_CONN.cursor()
        cursor.execute("DELETE FROM members_tanks")
        for member in clanMembers:
            sql_statement = """
            INSERT INTO members_tanks(account_id, tank_id)
                VALUES(?, ?)
            ;"""

            if len(member["tanks"]) != 0:
                for tank in member["tanks"]:
                    cursor.execute(sql_statement, (member["rowId"], int(tank)))
        DB_CONN.commit()
        cursor.close()
        return None
    

    def print_tanks(self) -> None:
        cursor = DB_CONN.cursor()
        sql_query = """
            SELECT 
                n.account_name, GROUP_CONCAT(DISTINCT t.name)
            FROM 
                ((members_tanks m
                    INNER JOIN clan_members n ON m.account_id = n.id)
                    INNER JOIN clan_wars_tanks t ON t.tank_id = m.tank_id)
            GROUP BY
                n.account_name
            ;
            """
        cursor.execute(sql_query)
        result = cursor.fetchall()
        for row in result:
             print(row)
        DB_CONN.commit()
        cursor.close()
    # ----------END OF HANDLING clan_members & members_tanks TABLES----------