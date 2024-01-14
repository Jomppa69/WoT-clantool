from api_handler import ApiHandler
from db_handler import DbHandler, DB_CONN

class getMembers():
    def __init__(self, container) -> None:
        APIhandler = ApiHandler()
        DBhandler = DbHandler()

        DBhandler.init_member_database()

        clanMembers = APIhandler.pull_members()
        tankIds = DBhandler.get_tank_ids()

        DBhandler.add_clan_members(clanMembers)
        clanMembers = APIhandler.get_members_tanks(clanMembers, tankIds)

        DBhandler.write_member_tanks(clanMembers)
        DBhandler.print_tanks()

        DB_CONN.close()
        return None
