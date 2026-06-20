# 在 admin.html 的"铸炼预售管理"和"天规税率调整"之间插入开盘设置模块
import re

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 插入点在"终止铸炼会自动将合约内全部BNB与预售代币注入流动仙液池"的 </div> 后面
# 即 <hr class="divider"/> 之前

new_section = """
    <hr class="divider"/>

    <div class="card-header" style="font-size:.95rem;margin-bottom:12px">🔔 开盘设置</div>

    <div style="background:rgba(0,0,0,.25);border-radius:10px;padding:14px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <label style="font-size:.82rem;color:var(--text-muted);cursor:pointer;">
          <input type="checkbox" id="admin-auto-open" onchange="adminSetAutoOpenOnFill(this.checked)" style="margin-right:6px;accent-color:var(--accent1)"/>
          Mint满自动开盘
        </label>
        <span id="admin-auto-open-status" style="font-size:.75rem;color:var(--accent2)"></span>
      </div>

      <div style="margin-bottom:12px;">
        <div style="font-size:.82rem;color:var(--text-muted);margin-bottom:6px;">🕐 定时开盘（北京时间）</div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <input type="datetime-local" id="admin-open-time" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:6px 10px;color:var(--text-body);font-size:.82rem;"/>
          <button onclick="adminSetTradingOpenTime()" style="background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem;font-weight:600;">设定定时开盘</button>
          <button onclick="adminCancelTradingOpenTime()" style="background:rgba(255,255,255,.08);color:var(--text-muted);border:1px solid rgba(255,255,255,.1);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.78rem;" onmouseover="this.style.borderColor='var(--danger)'" onmouseout="this.style.borderColor='rgba(255,255,255,.1)'">取消定时</button>
        </div>
        <div id="admin-open-time-display" style="font-size:.75rem;color:var(--text-muted);margin-top:6px;"></div>
      </div>

      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <button onclick="adminEnableTrading()" style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;border:none;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(22,163,74,.35)">🔓 手动开盘</button>
      </div>
    </div>

    <hr class="divider"/>

"""

# 找到插入点：在"天规税率调整"这个 card-header 之前插入
# 匹配：</div>\n\n    <hr class="divider"/>\n\n    <div class="card-header" ...>⚖️ 天规税率调整
old = '    <div class="card-header" style="font-size:.95rem;margin-bottom:12px">⚖️ 天规税率调整</div>'
new = new_section + '    <div class="card-header" style="font-size:.95rem;margin-bottom:12px">⚖️ 天规税率调整</div>'

if old in content:
    content = content.replace(old, new, 1)
    print('插入成功')
else:
    print('未找到插入点！')
    # 调试：找类似的内容
    idx = content.find('天规税率调整')
    if idx >= 0:
        print('找到上下文：', content[max(0,idx-100):idx+50])

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('完成')
