# FilesAnywhereSOAPClient
SOAP Client makes some FilesAnywhere API (FAWAPI) calls. Technical challenge for Konica Minolta

Platform-independent, tested on Python 2.7.10.

## Running

First, resolve Dependencies. Then, run the SOAP client by navigating to the directory containing the file "FAClient.py" and pass the file to python. This will run on any operating system that Python 2.7.10 is supported for.

> python FAClient.py -u {username} -p {password} --apikey {FilesAnywhereAPIKeyString} --orgid {50}

## Usage

Optional parameters are enclosed in brackets. To switch organization IDs you will need to restart with the correct "--orgid" parameter. Switching accounts is supported if the organization ID is unchanged. It is possible to upload multiple files simultaneously.

> -h - Help menu

> -u FilesAnywhere Username

> -p FilesAnywhere Password

> --apikey FilesAnywhere API Key

> [--orgid] Organization ID (Default: 0)

> [--iplist] Comma separated list of allowed IPs

>  Follow prompts to execute any number of API calls

## Dependencies (Python Libraries)
> progress 1.2

https://pypi.python.org/pypi/progress

> requests 2.13.0

http://docs.python-requests.org/en/master/

## Resolve Dependencies
> easy_install pip

> pip install progress

> pip install requests

## Notes

Simultaneous uploading is supported. The progress bar (Progress 1.2) was not designed to handle multiple instances of the progress bar. Therefore, some "flickering" will occur when uploading multiple files simultaneously.

Some naive assumptions were made within the scope of this deliverable. Some errors are ungracefully handled. For instance, if uploading a file and not specifying a proper filepath, 5 attempts will be made before giving up. Reading XML attributes is not robust.
