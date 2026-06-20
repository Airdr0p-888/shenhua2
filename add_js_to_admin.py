# 给 admin_new.html 添加 JS 函数（开盘设置相关）
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

TEMP = os.environ.get('TEMP', r'C:\Users\ADMINI~1\AppData\Local\Temp')
path = os.path.join(TEMP, 'admin_new.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 </script> 前插入新的 JS 函数
new_js = r"""
async function adminSetAutoOpenOnFill(v) {
  try {
    const tx = await targetContract.setAutoOpenOnFill(v);
    await tx.wait();
    showModal('✅', '自动开盘设置已保存', '', 'done');
    adminRefreshStatus();
  } catch(e) { showModal('⚠️', '设置失败', e.reason||e.message, 'error'); }
}
async function adminSetTradingOpenTime() {
  const dtStr = document.getElementById('admin-open-time').value;
  if (!dtStr) { alert('请选择开盘时间'); return; }
  // dtStr 格式 "2026-06-21T10:00"，视为北京时间（UTC+8）
  const d = new Date(dtStr + '+08:00');
  const ts = Math.floor(d.getTime() / 1000);
  if (!ts || ts < Date.now()/1000) { alert('时间必须晚于当前时间'); return; }
  try {
    const tx = await targetContract.setTradingOpenTime(ts);
    await tx.wait();
    showModal('✅', '定时开盘已设定', '', 'done');
    adminRefreshStatus();
  } catch(e) { showModal('⚠️', '设定失败', e.reason||e.message, 'error'); }
}
async function adminCancelTradingOpenTime() {
  try {
    const tx = await targetContract.setTradingOpenTime(0);
    await tx.wait();
    showModal('✅', '定时开盘已取消', '', 'done');
    adminRefreshStatus();
  } catch(e) { showModal('⚠️', '操作失败', e.reason||e.message, 'error'); }
}
"""

# 在 </script> 前插入（</script> 之前）
script_end = '</script>'
if script_end in content:
    idx = content.index(script_end)
    content = content[:idx] + new_js + '\n' + content[idx:]
    print('JS 函数插入成功')
else:
    print('未找到 </script>')

# 2. 修改 adminRefreshStatus()：在读取列表里加 autoOpenOnFill 和 tradingOpenTime
# 找到 Promise.all([ 的位置，在里面加读操作
old_promise = "const [presaleActive, fillBNB, collectedBNB, tradeOpen, buyTax, sellTax,"
new_promise = "const [presaleActive, fillBNB, collectedBNB, tradeOpen, autoOpen, openTime, buyTax, sellTax,"
if old_promise in content:
    content = content.replace(old_promise, new_promise, 1)
    print('Promise.all 已更新')
else:
    print('未找到 Promise.all 旧字符串')

# 对应的读取列表也要加
old_calls = """      c.presaleActive(), c.fillAmountBNB(), c.totalBNBCollected(), c.tradingActive(),
      c.buyTaxBps(), c.sellTaxBps(),"""
new_calls = """      c.presaleActive(), c.fillAmountBNB(), c.totalBNBCollected(), c.tradingActive(),
      c.autoOpenOnFill(), c.tradingOpenTime(),
      c.buyTaxBps(), c.sellTaxBps(),"""
if old_calls in content:
    content = content.replace(old_calls, new_calls, 1)
    print('读取列表已更新')
else:
    print('未找到读取列表旧字符串，尝试搜索...')
    # 模糊找
    idx = content.find('c.presaleActive()')
    if idx >= 0:
        print('找到上下文:', repr(content[idx:idx+100]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('完成，文件已写入:', path)
