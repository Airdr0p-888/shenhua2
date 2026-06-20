import json, urllib.request

rpc = 'https://bsc-dataseed.binance.org/'
contract = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'

def eth_call(data):
    payload = {'jsonrpc':'2.0','method':'eth_call','params':[{'to':contract,'data':data},'latest'],'id':1}
    r = urllib.request.urlopen(urllib.request.Request(rpc,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}),timeout=10)
    return json.loads(r.read())['result']

# balanceOf(contract) - selector: 70a08231
# padded address: 0000000000000000000000006fe41178284f5651d09d56cc6a6d3d87c60ac555
contract_padded = '0000000000000000000000006fe41178284f5651d09d56cc6a6d3d87c60ac555'
bal = eth_call('0x70a08231000000000000000000000000' + contract_padded)
print(f"balanceOf(contract) raw: {bal}")
bal_int = int(bal, 16)
print(f"balanceOf(contract) human: {bal_int / 10**18}")

# totalSupply() - selector: 18160ddd
ts = eth_call('0x18160ddd')
print(f"totalSupply raw: {ts}")
ts_int = int(ts, 16)
print(f"totalSupply human: {ts_int / 10**18}")

# balanceOf(pair) - pair address from earlier: 0x9d07220A46225A590D7a887E0E9f3Eb377c9aEa4
pair = '0x9d07220A46225A590D7a887E0E9f3Eb377c9aEa4'.lower()
pair_padded = '0'*24 + pair[2:]
bal_pair = eth_call('0x70a08231' + pair_padded)
print(f"balanceOf(pair) raw: {bal_pair}")
bal_pair_int = int(bal_pair, 16)
print(f"balanceOf(pair) human: {bal_pair_int / 10**18}")

# Add up: contract + pair + check vs totalSupply
print(f"\nSum check: contract({bal_int}) + pair({bal_pair_int}) = {bal_int + bal_pair_int}")
print(f"TotalSupply: {ts_int}")
print(f"Difference (unaccounted): {ts_int - bal_int - bal_pair_int}")
print(f"Difference / 10^18: {(ts_int - bal_int - bal_pair_int) / 10**18}")
