const { ethers } = require('ethers');
const fs = require('fs');
const src = fs.readFileSync('./contract_data.js', 'utf8');
eval(src.replace('const CONTRACT_DATA', 'var CONTRACT_DATA'));
const ABI = CONTRACT_DATA.ABI;

const provider = new ethers.JsonRpcProvider('https://bsc-dataseed.binance.org/');
const c = new ethers.Contract('0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555', ABI, provider);

async function main() {
  const [buyTax, sellTax, maxTax] = await Promise.all([
    c.buyTaxBps(), c.sellTaxBps(), c.MAX_TAX()
  ]);
  console.log('链上实际税率：');
  console.log('  buyTaxBps  =', buyTax.toString(), '→', (buyTax / 10000 * 100).toFixed(2) + '%');
  console.log('  sellTaxBps =', sellTax.toString(), '→', (sellTax / 10000 * 100).toFixed(2) + '%');
  console.log('  MAX_TAX    =', maxTax.toString());
}
main().catch(console.error);
