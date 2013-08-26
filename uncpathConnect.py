import os
from win_unc import UncCredentials, UncDirectory, UncDirectoryConnection
import ConfigParser
import base64

def UncConnect(uncPath, username=None, password=None):
    # Or provide credentials if you need them:
    if username != None and password != None:
        creds = UncCredentials(username, password)
        authz_unc = UncDirectory(uncPath, creds)
    else:
        authz_unc = UncDirectory(uncPath)
    
    # Setup a connection handler:
    conn = UncDirectoryConnection(authz_unc, persistent = True)
    conn.connect()
    conn.disconnect()

    os.system('cmd.exe /c start "" "{path}"'.format(path=uncPath))

