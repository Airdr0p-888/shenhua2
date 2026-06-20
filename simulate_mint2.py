import json, re
from web3 import Web3, HTTPProvider
from eth_account.account import Account

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
abi_match = re.search(r'"ABI":\s*(\[.*?\])\s*,\s*"BYTECODE"', content, re.DOTALL)
abi = json.loads(abi_match.group(1))

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))
contract = w3.eth.contract(address=contract_address, abi=abi)

mint_cost = contract.functions.mintCostBNB().call()
print(f"mintCostBNB: {mint_cost}")

acct = Account.create()
print(f"Simulating mint from: {acct.address}")

# Encode mint() call data
mint_data = contract.encodeABI('mint', [])
print(f"mint() data: {mint_data}")

try:
    gas = w3.eth.estimate_gas({
        'from': acct.address,
        'to': contract_address,
        'value': mint_cost,
        'data': mint_data,
    })
    print(f"Gas estimate: {gas} - mint should work!")
except Exception as e:
    err_str = str(e)
    print(f"\n=== Revert ===")
    print(err_str)
    # Try to extract revert reason from the error
    if 'revert' in err_str.lower() or 'execution reverted' in err_str.lower():
        # Look for the revert reason string in the error
        import re as re2
        # The revert reason is usually in the error message
        print(f"\nFull error: {err_str}")
