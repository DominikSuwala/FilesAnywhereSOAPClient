"""
    Author:     Dominik Suwala <dxs9411@rit.edu>
    Date:       2017-02-05
    Purpose:    FilesAnywhere SOAP client implementation for Konica Minolta
"""

import urllib2
import httplib
import requests
import sys
import os

"""
    Gets value of XML attribute
"""

def getXMLAttribute( msg, keyName ):
    if( keyName in msg ):
        # print msg.split( keyName + '>' )[ 1 ].split( '</' )[ 0 ]
        return msg.split( keyName + '>' )[ 1 ].split( '</' )[ 0 ]
    else:
        return None

"""
    Generic web call for a SOAP service, SOAP1.2
"""
def callSOAPService( SOAPmessage, SOAPAction ):
    headers = {
        'Content-Type' : 'application/soap+xml; charset=utf-8'
        #'SOAPAction' : 'http://api.filesanywhere.com/' + SOAPAction
    }
    endpoint = 'https://api.filesanywhere.com/v2/fawapi.asmx'

    postData = SOAPmessage
    r = requests.post( endpoint, data=postData, headers=headers )
    # print r.status_code, r.content
    return r.content

def validateResponse( SOAPmessage ):
    if( '<ErrorMessage>' in SOAPmessage ):
        return False
    return True

"""
    Login by organization ID, username, and password
"""
def AccountLogin( argsDict ):
    soapTemplate = open( 'SOAP_Templates/AccountLogin.txt' ).read()
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_1}', argsDict[ '--apikey' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_2}', argsDict[ '--orgid' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_3}', argsDict[ '-u' ] )
    if( argsDict[ 'encpass' ] ):
        soapTemplate = soapTemplate.replace( '{REPLACE_ME_6}', 'ENCRYPTEDYES' )
    else:
        soapTemplate = soapTemplate.replace( '{REPLACE_ME_6}', 'ENCRYPTEDNO' )

    soapTemplate = soapTemplate.replace( '{REPLACE_ME_4}', argsDict[ '-p' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_5}', argsDict[ '--iplist' ] )

    # print soapTemplate

    response = callSOAPService( soapTemplate, 'AccountLogin' )
    # print response

    if( not validateResponse( response ) ):
        print( 'Invalid login or password' )
        sys.exit( 1 )

    if( '<Token>' in response ):
        argsDict[ 'token' ] = getXMLAttribute( response, 'Token' )
    if( '<ClientEncryptedPassword>' in response ):
        argsDict[ 'encpass' ] = True
        argsDict[ '-p' ] = getXMLAttribute( response, 'ClientEncryptedPassword' )

    print( 'Successfully logged in as ' + argsDict[ '-u' ] + '.' )


"""
    List files and folders within a user's volume
"""
def ListItems2( argsDict ):
    soapTemplate = open( 'SOAP_Templates/ListItems2.txt' ).read()
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_1}', argsDict[ 'token' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_2}', '\\' + argsDict[ '-u' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_3}', '50' )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_4}', '0' )

    response = callSOAPService( soapTemplate, 'ListItems' )
    # print soapTemplate
    # print response

    if( not validateResponse( response ) ):
        print( 'Invalid response' )

    # Name, Size, Path, DateLastModified
    print response.count( '<Item>' ), 'files + folders'
    for tempStr in response.split( '<Item>' )[1:]:
        print 'Name', getXMLAttribute( tempStr, 'Name' )
        print 'Size', getXMLAttribute( tempStr, 'Size' ), 'bytes'
        print 'Path', getXMLAttribute( tempStr, 'Path' )
        print 'Date', getXMLAttribute( tempStr, 'DateLastModified' )
        print '-------'

"""
    Create a folder
"""
def CreateFolderRecursive( argsDict, folderName ):
    soapTemplate = open( 'SOAP_Templates/CreateFolderRecursive.txt' ).read()
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_1}', argsDict[ 'token' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_2}', '\\' + argsDict[ '-u' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_3}', folderName )

    response = callSOAPService( soapTemplate, 'CreateFolderRecursive' )
    # print soapTemplate
    # print response

    if( not validateResponse( response ) ):
        print( 'Invalid. Could not create folder ' + folderName )
    else:
        print( 'Successfully created folder "' + folderName + '"' )


"""
    Upload a file piece-by-piece in chunks
"""
def AppendChunk( argsDict, folderName, filename ):

    uploadPath = ''
    filename = ''
    # chunkdata
    # Offset
    # bytesread
    # islastchunk

    soapTemplate = open( 'SOAP_Templates/CreateFolderRecursive.txt' ).read()
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_1}', argsDict[ 'token' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_2}', '\\' + argsDict[ '-u' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_3}', folderName )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_4}', argsDict[ 'token' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_5}', '\\' + argsDict[ '-u' ] )
    soapTemplate = soapTemplate.replace( '{REPLACE_ME_6}', folderName )

"""
    Delete a file or folder
"""
def DeleteItems():
    pass

"""
    Search files and folders
"""
def SearchFiles():
    pass

"""
    Send link used to access files
"""
def SendItemsELink2():
    pass

def printHelp():
    print 'Usage: python FAClient.py'
    print 'Command-Line Options:'
    print '\t-u <username>'
    print '\t-p <password>'
    print '\t[--orgid] <orgID>'
    print '\t[--iplist] <commaSeparatedListOfAllowedIPs>'
    print '\t[--apikey] <APIkey>'
    print ''

def main():
    if( sys.argv[ 1 ] == '--help' or sys.argv[ 1 ] == '-h' ):
        printHelp()
        sys.exit( 0 )
    APIkey = '0FDEF414-DB8C-4321-9FCA-A6B66A75EC55'
    loggedIn = False
    argsDict = {}
    i = 1
    sysargs = sys.argv[ 1: ]
    argsDict[ 'encpass' ] = False
    argsDict[ '--orgid' ] = '0'
    argsDict[ '--apikey' ] = APIkey
    argsDict[ '--iplist' ] = ''

    i = 0
    while( len( sysargs ) > 0 ):
        try:
            argsDict[ sysargs[ i ].lower() ] = sysargs[ i + 1 ]
        except:
            argsDict[ sysargs[ i ].lower() ] = ''
        sysargs = sysargs[ 2: ]
    for d in argsDict.keys():
        pass #print d, argsDict[ d ]

    response = AccountLogin( argsDict )
    # print argsDict

    actions = {
        'login' : 'Login',
        'ls' : 'List files',
        'mkdir' : 'Create a folder',
        'upload' : 'Upload a file',
        'delete' : 'Delete a file or folder',
        'search' : 'Search files and folers',
        'link' : 'Get link used to access files'
    }
    while( True ):
        print 'Select action:'
        for action in actions:
            print action, '-', actions[ action ]
        choice = raw_input()
        if( choice not in actions.keys() ):
            if( choice == 'debug' ):
                print argsDict
            continue
        elif( choice == 'login' ):
            print 'Enter username:'
            username = raw_input()
            print 'Enter password:'
            password = raw_input()
            argsDict[ '-u' ] = username
            argsDict[ '-p' ] = password
            argsDict[ 'encpass' ] = False
            AccountLogin( argsDict )

        elif( choice == 'ls' ):
            ListItems2( argsDict )
        elif( choice == 'mkdir' ):
            print 'Enter new folder name, including path'
            folderName = raw_input()
            CreateFolderRecursive( argsDict, folderName )

if __name__ == '__main__':
    main()
