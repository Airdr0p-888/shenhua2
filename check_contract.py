import json, re, urllib.request

# Read contract_data.js and extract ABI
with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\contract_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract ABI json
abi_match = re.search(r'"ABI":\s*(\[.*?\])\s*,\s*"BYTECODE"', content, re.DOTALL)
if not abi_match:
    print("Could not extract ABI")
    exit(1)
abi = json.loads(abi_match.group(1))

contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'
rpc_url = 'https://bsc-dataseed.binance.org/'

def call_view(func_name):
    # Find function in ABI
    func = None
    for item in abi:
        if item.get('name') == func_name and item.get('type') == 'function':
            func = item
            break
    if not func:
        return 'NOT_FOUND'
    # Build function selector
    inputs = func.get('inputs', [])
    if inputs:
        return 'HAS_INPUTS'
    # Encode function call (just selector)
    import hashlib
    sig = func_name + '()'
    selector = '0x' + hashlib.sha3_256(sig.encode()).hexdigest()[:8]
    # Make RPC call
    payload = {
        'jsonrpc': '2.0',
        'method': 'eth_call',
        'params': [{'to': contract_address, 'data': selector}, 'latest'],
        'id': 1
    }
    req = urllib.request.Request(rpc_url, 
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get('result', 'ERROR')
    except Exception as e:
        return str(e)

# Call all zero-arg view functions
view_funcs = ['presaleTokenPct','lpTokenPct','totalPresaleTokens','totalLPTokens',
    'presaleTokensGiven','lpTokensUsed','mintCostBNB','tokensPerMint',
    'fillAmountBNB','totalBNBCollected','presaleActive','mintLiquidityBps',
    'totalSupply','name','symbol','decimals']

for fn in view_funcs:
    result = call_view(fn)
    print(f'{fn}: {result}')
