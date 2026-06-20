import json, re
from web3 import Web3, HTTPProvider, Account
from eth_utils import to_hex

# Read ABI
with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
abi_match = re.search(r'"ABI":\s*(\[.*?\])\s*,\s*"BYTECODE"', content, re.DOTALL)
abi = json.loads(abi_match.group(1))

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))
contract = w3.eth.contract(address=contract_address, abi=abi)

# Check current state
print("=== 当前链上状态 ===")
print(f"presaleTokensGiven:  {contract.functions.presaleTokensGiven().call()}")
print(f"lpTokensUsed:       {contract.functions.lpTokensUsed().call()}")
print(f"totalBNBCollected:  {contract.functions.totalBNBCollected().call()}")
print(f"fillAmountBNB:      {contract.functions.fillAmountBNB().call()}")
print(f"mintCostBNB:        {contract.functions.mintCostBNB().call()}")
print(f"presaleActive:       {contract.functions.presaleActive().call()}")
print(f"contract BNB balance: {w3.eth.get_balance(contract_address)}")
print()

# Simulate mint for a fresh wallet (mintCount=0)
# We need to call mint() and see if it reverts
# Since we can't send a real tx, let's check the conditions manually

remaining = contract.functions.fillAmountBNB().call() - contract.functions.totalBNBCollected().call()
print(f"remaining BNB to fill: {remaining}")
print(f"mintCostBNB:         {contract.functions.mintCostBNB().call()}")
print(f"Is last mint? remaining < mintCostBNB: {remaining < contract.functions.mintCostBNB().call()}")

# Check if contract has enough balance
contract_bal = contract.functions.balanceOf(contract_address).call()
print(f"contract token balance: {contract_bal}")

# Calculate needed for next mint
tokens_per_mint = contract.functions.tokensPerMint().call()
needed = tokens_per_mint * 2  # user + LP
print(f"tokensPerMint: {tokens_per_mint}")
print(f"contract balance >= tokensPerMint*2: {contract_bal >= tokens_per_mint * 2}")

# Check lpTokensUsed vs totalLPTokens
lp_used = contract.functions.lpTokensUsed().call()
total_lp = contract.functions.totalLPTokens().call()
print(f"lpTokensUsed: {lp_used}, totalLPTokens: {total_lp}, remaining LP: {total_lp - lp_used}")
print(f"Next mint LP need: {tokens_per_mint}, sufficient: {total_lp - lp_used >= tokens_per_mint}")
