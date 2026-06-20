import json, re
from web3 import Web3, HTTPProvider

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
abi_match = re.search(r'"ABI":\s*(\[.*?\])\s*,\s*"BYTECODE"', content, re.DOTALL)
abi = json.loads(abi_match.group(1))

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))
contract = w3.eth.contract(address=contract_address, abi=abi)

# Read all relevant state
ts = contract.functions.totalSupply().call()
ptg = contract.functions.presaleTokensGiven().call()
lu = contract.functions.lpTokensUsed().call()
cb = contract.functions.balanceOf(contract_address).call()
tpt = contract.functions.totalPresaleTokens().call()
tlp = contract.functions.totalLPTokens().call()

print(f"totalSupply:         {ts}  = {ts / 10**18}")
print(f"presaleTokensGiven:  {ptg}  = {ptg / 10**18}")
print(f"lpTokensUsed:        {lu}  = {lu / 10**18}")
print(f"contract balance:     {cb}  = {cb / 10**18}")
print(f"totalPresaleTokens:  {tpt}  = {tpt / 10**18}")
print(f"totalLPTokens:       {tlp}  = {tlp / 10**18}")
print()
print(f"数学检查:")
print(f"  totalSupply - presaleTokensGiven - lpTokensUsed = {ts - ptg - lu}  = {(ts - ptg - lu) / 10**18}")
print(f"  contract balance (actual)                        = {cb}  = {cb / 10**18}")
print(f"  差额 (missing tokens)                            = {cb - (ts - ptg - lu)}  = {(cb - (ts - ptg - lu)) / 10**18}")
print()
# Check: does the contract have UNCLAIMED LP tokens (in the pair but not accounted for)?
# Try to find the pair address
try:
    pair = contract.functions.uniswapV2Pair().call()
    print(f"LP Pair address: {pair}")
    pair_bal = contract.functions.balanceOf(pair).call()
    print(f"Pair token balance: {pair_bal} = {pair_bal / 10**18}")
except Exception as e:
    print(f"Could not get pair: {e}")
