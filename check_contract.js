const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, 'contract_data.js'), 'utf8');
eval(src.replace('const CONTRACT_DATA', 'var CONTRACT_DATA'));

const ABI = CONTRACT_DATA.ABI;
const provider = new ethers.JsonRpcProvider('https://bsc-dataseed.binance.org/');
const contract = new ethers.Contract('0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555', ABI, provider);

async function main() {
  const keys = [
    'presaleTokenPct','lpTokenPct','totalPresaleTokens','totalLPTokens',
    'presaleTokensGiven','lpTokensUsed','mintCostBNB','tokensPerMint',
    'fillAmountBNB','totalBNBCollected','presaleActive','mintLiquidityBps'
  ];
  for (const k of keys) {
    try {
      const v = await contract[k]();
      console.log(k + ':', v.toString());
    } catch(e) {
      console.log(k + ': N/A');
    }
  }
  // Also check total supply and balance of contract
  try {
    const totalSupply = await contract.totalSupply();
    console.log('totalSupply:', totalSupply.toString());
    const contractBal = await contract.balanceOf('0x6Fe41178284F5651D09d56CC6A6D3D87C60AC555');
    console.log('contractBalance:', contractBal.toString());
  } catch(e) {}
}
main().catch(console.error);
