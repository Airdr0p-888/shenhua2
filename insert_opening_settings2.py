# 在 admin.html 的"天规税率调整"之前插入开盘设置模块
import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_section = r"""    <hr class="divider"/>

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
          <button onclick="adminCancelTradingOpenTime()" style="background:rgba(255,255,255,.08);color:var(--text-muted);border:1px solid rgba(255,255,255,.1);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.78rem;">取消定时</button>
        </div>
        <div id="admin-open-time-display" style="font-size:.75rem;color:var(--text-muted);margin-top:6px;"></div>
      </div>

      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <button onclick="adminEnableTrading()" style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;border:none;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(22,163,74,.35)">🔓 手动开盘</button>
      </div>
    </div>

    <hr class="divider"/>

"""

# 找到"天规税率调整"的 card-header，在其前面插入
old_marker = '<div class="card-header" style="font-size:.95rem;margin-bottom:12px">⚖️ 天规税率调整</div>'

if old_marker in content:
    content = content.replace(old_marker, new_section + old_marker, 1)
    print('OK: inserted')
else:
    print('FAIL: marker not found')
    # debug: find near "税率"
    idx = content.find('税率调整')
    if idx >= 0:
        print('found near index', idx)

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')
