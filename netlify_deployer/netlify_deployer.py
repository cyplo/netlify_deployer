#!/usr/bin/python3

import json
import os
import requests
import sys
import hashlib
import time

def checkArguments():
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print('usage: ')
        print(sys.argv[0] + " branch_name netlify_site_id directory_to_deploy [deployment_id_to_continue]")
        sys.exit(1)


def getAuthToken():
    token = os.getenv("NETLIFY_TOKEN")
    if not token:
        print('Please set NETLIFY_TOKEN')
        sys.exit(2)

    return token

def getDirectoryToDeploy():
    return os.path.abspath(sys.argv[3])

def getSiteId():
    return sys.argv[2]

def validateDirectoryStructure():
    print('Validating structure...', end="")
    index_filename = "index.html"
    if os.path.isfile(os.path.join(directory_to_deploy, index_filename)):
        print('OK')
    else:
        print('No ' + index_filename)
        sys.exit(3)

def getAllFilePathsForDirectory(directory):
    paths = []
    for root, dirs, filenames in os.walk(directory, topdown=False):
        paths += ((os.path.join(root, name)) for name in filenames)
    return paths

def calculateHashesForPaths(paths):
    print('Hashing...', end="")
    hashes = {}
    for path in paths:
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        sha1 = hashlib.sha1()

        with open(path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)

            file_hash = sha1.hexdigest()
            relative_path = path.replace(directory_to_deploy, '')
            hashes[relative_path] = file_hash
    print('OK')
    return hashes


def getBranchName():
    return sys.argv[1]


def createDeployment(file_hashes):
    print('Creating new deployment...', end="")
    branch_name = getBranchName()
    if branch_name == 'master':
        new_deploy = {'files': file_hashes, 'draft': False}
    else:
        new_deploy = {'files': file_hashes, 'context': 'deploy-preview', 'draft': True}
    new_deploy_json = json.dumps(new_deploy)
    response = requests.post(url=deploys_url, headers=json_headers, data=new_deploy_json)
    if not response.ok:
        print('Failed with error')
        print(response.content)
        sys.exit(4)
    print('OK')
    return response.json()

def getExistingDeployment(deployment_id):
    deploy_url = deploys_url + deployment_id + "/"
    response = requests.get(url=deploy_url, headers=json_headers)
    if not response.ok:
        print('Failed with error')
        print(response.content)
        sys.exit(5)
    return response.json()

def invertDict(dict):
    return {v: k for k, v in dict.items()}

def uploadFilesForHashes(files_for_hashes, required_hashes):
    for required_hash in required_hashes:
        current_file_name = files_for_hashes[required_hash]
        print('Uploading ' + current_file_name + "...", end="")
        with open(os.path.join(directory_to_deploy, "./" + current_file_name), 'rb') as current_file_handle:
            file_upload_url = new_deploy_url + "files/" + current_file_name
            response = requests.put(url=file_upload_url, headers=file_upload_headers, data=current_file_handle)
            if not response.ok:
                print('Failed with error')
                print(response.content)
                sys.exit(6)
            else:
                print('OK')

checkArguments()
auth_token = getAuthToken()
site_id = getSiteId()
json_headers = {"Authorization": "Bearer " + auth_token, 'content-type': "application/json"}
base_url = 'https://api.netlify.com/api/v1/'
site_url = base_url + "sites/" + site_id + "/"
deploys_url = site_url + "deploys/"

directory_to_deploy = getDirectoryToDeploy()

print("Deploying " + directory_to_deploy + " to Netlify as " + site_id)
validateDirectoryStructure()

paths_to_hash = getAllFilePathsForDirectory(directory_to_deploy)
file_hashes = calculateHashesForPaths(paths_to_hash)

if not len(sys.argv) == 5:
    deployment = createDeployment(file_hashes)
else:
    deployment_id = sys.argv[4]
    deployment = getExistingDeployment(deployment_id)

deployment_id = deployment['id']

files_for_hashes = invertDict(file_hashes)

new_deploy_url = base_url + "deploys/" + deployment_id + "/"
file_upload_headers = {"Authorization": "Bearer " + auth_token, 'content-type': "application/octet-stream"}
uploadFilesForHashes(files_for_hashes, deployment['required'])

print('Done uploading, waiting for the confirmation...')
while deployment['state'] != 'ready':
    time.sleep(1)
    deployment = getExistingDeployment(deployment_id)

print('Fully deployed at ' + deployment['deploy_ssl_url'])
