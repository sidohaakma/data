#!python

import opal.rest
import opal.file
import opal.import_xml

import click
import constants
import ws.rest

from arguments import Arguments

@click.command()
@click.option(
    '--host',
    '-h', 
    prompt=True,
    default='localhost:8080',
    help='Opal host; only yhe dns name, without protocol and port number.')
@click.option(
    '--admin-username',
    '-u', 
    default='administrator',
    help='Administrator username of Opal host')
@click.option(
    '--admin-password',
    '-p', 
    prompt=True,
    help='Administrator password of Opal host')
@click.option(
    '--version',
    '-v', 
    default='1_0',
    help='Version of data dictionary; can be x_x, for example 1_0.')
def populate(host, admin_username, admin_password, version): 
    '''
    This script will bootstrap the data dictionary version of the LifeCycle variables into Opal.
    '''

    createProject(admin_username, admin_password, host, constants.PROJECT)

    uploadFile(admin_username, admin_password, host, version, constants.DICT_MONTHLY_REPEATED_MEASURES)
    uploadFile(admin_username, admin_password, host, version, constants.DICT_YEARLY_REPEATED_MEASURES)
    uploadFile(admin_username, admin_password, host, version, constants.DICT_NON_REPEATED_MEASURES)

    importDictionary(admin_username, admin_password, host, version, constants.PROJECT, constants.DICT_MONTHLY_REPEATED_MEASURES)
    importDictionary(admin_username, admin_password, host, version, constants.PROJECT, constants.DICT_YEARLY_REPEATED_MEASURES)
    importDictionary(admin_username, admin_password, host, version, constants.PROJECT, constants.DICT_NON_REPEATED_MEASURES)

def createProject(admin_username, admin_password, host, project):
    data = "{\"name\":\"" + constants.PROJECT + "\",\"title\":\"" + constants.PROJECT + "\",\"description\":\"" + constants.PROJECT + "\",\"database\":\"opal_data\",\"vcfStoreService\": null}"

    args_project_bootstrap = Arguments({
        'headers': '',
        'user': admin_username,
        'password': admin_password,
        'content_type': 'application/json',
        'opal': host,
        'accept': 'application/json',
        'method': 'POST',
        'content': data,
        'ws': '/projects',
        'verbose': False,
        'json': False
    })

    ws.rest.do_command(args_project_bootstrap)

    print(u'\u2714' + ' bootstrap project: lifecycle')

def uploadFile(admin_username, admin_password, host, version, dictionary):
    
    opal.file.do_command(Arguments({
        'user': admin_username,
        'password': admin_password,
        'content_type': 'multipart/form-data',
        'opal': host,
        'path': constants.UPLOAD_PATH,
        'upload': constants.UPLOAD_CLIENT_PATH+ '/'  + version + '_' + dictionary + '.zip',
        'verbose': False,
        'download': '',
        'json': False
    }))

    print(u'\u2714' + ' upload metadata-file for table: ' + version + '_'  + dictionary)
    

def importDictionary(admin_username, admin_password, host, version, project, dictionary):
    opal.import_xml.do_command(Arguments({
        'user': admin_username,
        'password': admin_password,
        'opal': host,
        'path': constants.UPLOAD_PATH + '/' + version + '_' + dictionary + '.zip',
        'destination': project,
        'tables': '',
        'separator': ',',
        'type': 'Participant',
        'incremental': False,
        'limit': 0,
        'identifiers': '',
        'policy': '',
        'quote': '"',
        'firstRow': '1',
        'characterSet': 'ISO-8859-1',
        'valueType': '',
        'verbose': False,
        'json': False
    }))

    print(u'\u2714' + ' bootstrap metadata for table: ' + version + '_' + dictionary)