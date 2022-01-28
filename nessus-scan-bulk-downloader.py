# https://community.tenable.com/s/question/0D53a00006TAN76/bulk-download-entire-scan-history
import os
import re
import time
import json
import requests
import unicodedata
from tqdm import tqdm
from urllib.parse import urljoin
# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

output_dir = 'exports'
base_url = 'https://localhost:8834/'
# login info for local Nessus
username = ''
password = ''

export_format = 'db'
# password for nessus db
db_password = ''


if not os.path.exists(output_dir):
	os.mkdir(output_dir)

def slugify(value, allow_unicode = False):
	"""
	Modified from https://github.com/django/django/blob/master/django/utils/text.py
	Replace dot(.) with underscore(_) first to keep IP address formatting
	"""
	value = str(value).replace('.', '_')
	if allow_unicode:
		value = unicodedata.normalize('NFKC', value)
	else:
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub(r'[^\w\s-]', '', value.lower())
	return re.sub(r'[-\s]+', '-', value).strip('-_')

url = urljoin(base_url, 'session')

payload = {'username' : username, 'password' : password}

response = requests.request('POST', url, data = payload, verify = False)

token = json.loads(response.text)['token']

url = urljoin(base_url, 'scans')

headers = {'X-Cookie': 'token=' + token}

response = requests.request('GET', url, headers = headers, verify = False)

obj = json.loads(response.text)

id2foldername = {}
for folder_dict in obj['folders']:
	directory = folder_dict['name']
	id2foldername[folder_dict['id']] = directory
	dir_path = os.path.join(output_dir, directory)
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)

for scan_dict in tqdm(obj['scans']):
	scan_id = scan_dict['id']

	url = 'https://localhost:8834/scans/' + str(scan_id) + '/export'

	payload = {'scan_id' : scan_id, 'format' : export_format, 'password' : db_password, 'template_id' : 'false'}

	response = requests.request('POST', url, headers = headers, data = payload, verify = False)

	file_id = json.loads(response.text)['file']

	status = None
	while status != 'ready':
		time.sleep(1)

		url = 'https://localhost:8834/scans/' + str(scan_id) + '/export/' + str(file_id) + '/status'

		response = requests.request('GET', url, headers = headers, verify = False)

		res_json = json.loads(response.text)
		
		if 'status' in res_json:
			status = res_json['status']

	url = 'https://localhost:8834/scans/' + str(scan_id) + '/export/' + str(file_id) + '/download'

	response = requests.request('GET', url, headers = headers, verify = False)

	file_bin = response.content

	folder_name = id2foldername[scan_dict['folder_id']]
	scan_name = slugify(scan_dict['name']) + '.db'

	output_file_name = os.path.join(output_dir, folder_name, scan_name)
	with open(output_file_name, 'wb') as file:
		file.write(file_bin)
