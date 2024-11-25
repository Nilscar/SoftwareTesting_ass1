import json

################################
# USER DATA MANAGEMENT CLASSES #
################################


class UserDataManager:

    USER_FILE_PATHNAME: str = '../../files/users.json'

    @staticmethod
    def load_users() -> list[dict[str, str | float]]:
        try:
            with open(file=UserDataManager.USER_FILE_PATHNAME, mode='r') as file:
                return json.load(fp=file)
        except FileNotFoundError:
            print('File not found.')
            exit(1)

    @staticmethod
    def save_users(data: list[dict[str, str | float]]) -> None:
        with open(file=UserDataManager.USER_FILE_PATHNAME, mode='w') as file:
            json.dump(obj=data, fp=file, indent=2)
            
    @staticmethod
    def update_wallet(username,new_value):
        with open(file=UserDataManager.USER_FILE_PATHNAME,mode='r') as file:
            data = json.load(fp=file)
            user = {}
            for x in data:
                if x["username"] == username:
                    user = x
                    break
            user["wallet"] = new_value
        
        with open(file=UserDataManager.USER_FILE_PATHNAME,mode='w') as file:
            json.dump(data,file,indent=2)
        
        
        
            
