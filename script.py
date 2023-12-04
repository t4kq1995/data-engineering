#!/usr/bin/env python
# coding: utf-8
import requests

# response = requests.post(
#     url='http://localhost:8081',
#     json={'date': '2022-08-10', 'raw_dir': '/file_storage/raw/sales/2022-08-10'},
# )
# print("Response status code:", response.status_code)
# print("Response JSON", response.json())


response = requests.post(
    url='http://localhost:8082',
    json={'stg_dir': '/file_storage/stg/sales/2022-08-10', 'raw_dir': '/file_storage/raw/sales/2022-08-10'},
)
print("Response status code:", response.status_code)
print("Response JSON", response.json())