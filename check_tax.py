from web3 import Web3, HTTPProvider
from json import loads

w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))

# 读取 contract_data.js 里的 ABI
with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    src = f.read()
# 提取 ABI
abi_start = src.find('"ABI":') + 6
abi_end = src.find('],', abi_start) + 1
ABI = loads(src[abi_start:abi_end+1])

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
c = w3.eth.contract(address=contract_address, abi=ABI)

for fn in ['buyTaxBps', 'sellTaxBps', 'MAX_TAX']:
    try:
        v = c.functions[fn]().call()
        print(f'{fn} = {v}  (={v/100}%)' if 'Tax' in fn or 'MAX' in fn else f'{fn} = {v}')
    except Exception as e:
        print(f'{fn}: ERROR - {e}')
