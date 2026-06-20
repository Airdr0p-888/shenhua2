from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider('https://bsc-dataseed.binance.org/'))
contract_address = '0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555'

# 手动构造 ABI（只需要读税率的两个函数）
abi = [
    {
        "inputs": [],
        "name": "buyTaxBps",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
        "stateMutability": "view"
    },
    {
        "inputs": [],
        "name": "sellTaxBps", 
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
        "stateMutability": "view"
    },
    {
        "inputs": [],
        "name": "MAX_TAX",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
        "stateMutability": "view"
    }
]

c = w3.eth.contract(address=contract_address, abi=abi)

for fn_name in ['buyTaxBps', 'sellTaxBps', 'MAX_TAX']:
    try:
        val = c.functions[fn_name]().call()
        if 'Tax' in fn_name or 'MAX' in fn_name:
            print(f'{fn_name} = {val}  → 实际税率 = {val/10000*100:.2f}%')
        else:
            print(f'{fn_name} = {val}')
    except Exception as e:
        print(f'{fn_name}: 读取失败 - {e}')
