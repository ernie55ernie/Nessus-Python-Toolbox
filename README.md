# Nessus Python Toolbox

A toolbox that implements the extended functionalities of [Nessus](https://www.tenable.com/products/nessus), the #1 vulnerability assessment solution.

[![Python v3.8.5](https://img.shields.io/badge/python-v3.8.5-blue)](https://www.python.org/downloads/release/python-385/)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/ernie55ernie/Nessus-Python-Toolbox/blob/main/LICENSE)

## Table of Contents

- [Environments](#environments)
- [Usage](#usage)
- [Nessus Scan Bulk Downloader](#nessus-bulk-downloader)
- [To-Dos](#todos)

## Environments

1. Nessus Professional Version 10
2. Nessus API Documentation v. 10.0.2
3. [python 3.8.5](https://www.python.org/downloads/release/python-385/)
4. pip 20.2.4

## Usage

- Install dependency
```
pip install -r requirements.txt
```

## Nessus Scan Bulk Downloader

- Modify the output directory, Nessus endpoint, username, password, and Nessus db password in nessus-scan-bulk-downloader.py.
```python
output_dir = 'exports'
base_url = 'https://localhost:8834/'
# login infomation for local Nessus
username = ''
password = ''

export_format = 'db'
# password for nessus db
db_password = ''
```

- Run Nessus Scan Bulk Downloader.
```
python nessus-scan-bulk-downloader.py
100%|█████████████████████████████████████████| 107/107 [06:56<00:00,  3.89s/it]
```

This tool will execute the following functions.

1. Create a Session -> get token
2. List all Scans -> get folders and scans
3. Request for Export -> get file id
4. Check Export Status -> get status
5. Download Export file -> get file binary

This tool was inspired by this discussion, [Bulk Download Entire Scan History - Tenable Community](https://community.tenable.com/s/question/0D53a00006TAN76/bulk-download-entire-scan-history).

## To-Dos
- [ ] Export Scan Config to Scan Policy for other scans, [Can I export scan configuration and import them in SecurityCenter?](https://community.tenable.com/s/question/0D5f200005rdVSP/can-i-export-scan-configuration-and-import-them-in-securitycenter).

## License
Nessus Python Toolbox is licensed under the [MIT](https://github.com/ernie55ernie/Nessus-Python-Toolbox/blob/main/LICENSE) license.
Copyright (c) 2022 Yu-Wei Chang
