import json, re, sys
from web3 import Web3, HTTPProvider

# Read ABI from contract_data.js
with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

abi_match = re.search(r'"ABI":\s*(\[.*?\])\s*,\s*"BYTECODE"', content, re.DOTALL)
if not abi_match:
    print("Could not extract ABI")
    sys.exit(1)
abi = json.loads(abi_match.group(1))

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))
contract = w3.eth.contract(address=contract_address, abi=abi)

keys = [
    'presaleTokenPct','lpTokenPct','totalPresaleTokens','totalLPTokens',
    'presaleTokensGiven','lpTokensUsed','mintCostBNB','tokensPerMint',
    'fillAmountBNB','totalBNBCollected','presaleActive','mintLiquidityBps',
    'totalSupply','name','symbol','decimals'
]

for k in keys:
    try:
        v = contract.functions[k]().call()
        print(f'{k}: {v}')
    except Exception as e:
        print(f'{k}: ERROR - {e}')
