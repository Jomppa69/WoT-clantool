import requests
import json

class ApiHandler:
    def __init__(self) -> None:
          return None

    # ----------selectCwTanks.py FUNCTIONS----------
    def pull_tanks(self, classChoice) -> dict:
        response = requests.get(f"https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=f0caf677f57a195024f047e27c2913dd&fields=name%2C+tank_id%2C+type%2C+is_premium&type={classChoice}&tier=10")
        responseDict = json.loads(response.text)
        tanks = responseDict["data"]
        return tanks
    

    def get_keys(self, tanks) -> list:
        keys = list(tanks.keys())
        return keys
    # ----------END OF selectCwTanks.py functions----------

    # ----------getMembers.py FUNCTIONS----------
    def pull_members(self) -> dict:
        response = requests.get("https://api.worldoftanks.eu/wot/clans/info/?application_id=f0caf677f57a195024f047e27c2913dd&clan_id=500161363&fields=members.account_name%2C+members.account_id")
        responseDict = json.loads(response.text)
        clanMembers = responseDict["data"]["500161363"]["members"]
        return clanMembers


    def get_members_tanks(self, clanMembers, tankIds) -> dict:
        comparsions = 0
        members = 0
        for member in clanMembers:
            ownedTanks = []
            account_id = member["account_id"]
            response = requests.get(f"https://api.worldoftanks.eu/wot/account/tanks/?fields=tank_id&application_id=f0caf677f57a195024f047e27c2913dd&account_id={account_id}")
            responseDict = json.loads(response.text)
            memberTanks = responseDict["data"][str(account_id)]
            members += 1
            print(f"members {members}")
            
            for id in memberTanks:
                if id["tank_id"] in tankIds:
                    ownedTanks.append(id["tank_id"])
                    comparsions += 1
            member["tanks"] = ownedTanks
        print(comparsions)
        return clanMembers
    # ----------END OF getMembers.py functions----------