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

# Try to simulate a mint from a fresh address
mint_cost = contract.functions.mintCostBNB().call()
print(f"mintCostBNB: {mint_cost}")

# Use a random private key to simulate
acct = Account.create()
print(f"Simulating mint from: {acct.address}")

# Build the transaction
tx = contract.functions.mint().build_transaction({
    'from': acct.address,
    'value': mint_cost,
    'gas': 500000,
    'gasPrice': w3.eth.gas_price,
    'nonce': 0,
})

# Use eth_call to simulate (doesn't send)
# But eth_call needs a real tx... let's use estimate_gas which will revert with reason
try:
    gas = w3.eth.estimate_gas({
        'from': acct.address,
        'to': contract_address,
        'value': mint_cost,
        'data': contract.encodeABI('mint', []),
    })
    print(f"Gas estimate: {gas} - should work!")
except Exception as e:
    err_str = str(e)
    print(f"Revert reason: {err_str}")
    # Try to extract revert reason from error message
    if 'revert' in err_str.lower():
        # Try to decode the revert reason
        import re as re2
        # Look for "Already minted" or other string
        matches = re2.findall(r'[A-Za-z\s]+', err_str)
        print(f"Error details: {matches}")
