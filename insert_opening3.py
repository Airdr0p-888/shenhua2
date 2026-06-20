# 读取 admin.html，在"天规税率调整"前插入开盘设置模块，输出到临时目录
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import os

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('文件长度:', len(content))

new_section = (
    '    <hr class="divider"/>\n'
    '\n'
    '    <div class="card-header" style="font-size:.95rem;margin-bottom:12px">🔔 开盘设置</div>\n'
    '\n'
    '    <div style="background:rgba(0,0,0,.25);border-radius:10px;padding:14px;margin-bottom:14px;">\n'
    '      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">\n'
    '        <label style="font-size:.82rem;color:var(--text-muted);cursor:pointer;">\n'
    '          <input type="checkbox" id="admin-auto-open" onchange="adminSetAutoOpenOnFill(this.checked)" style="margin-right:6px;accent-color:var(--accent1)"/>\n'
    '          Mint满自动开盘\n'
    '        </label>\n'
    '        <span id="admin-auto-open-status" style="font-size:.75rem;color:var(--accent2)"></span>\n'
    '      </div>\n'
    '\n'
    '      <div style="margin-bottom:12px;">\n'
    '        <div style="font-size:.82rem;color:var(--text-muted);margin-bottom:6px;">🕐 定时开盘（北京时间）</div>\n'
    '        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">\n'
    '          <input type="datetime-local" id="admin-open-time" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:6px 10px;color:var(--text-body);font-size:.82rem;"/>\n'
    '          <button onclick="adminSetTradingOpenTime()" style="background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem;font-weight:600;">设定定时开盘</button>\n'
    '          <button onclick="adminCancelTradingOpenTime()" style="background:rgba(255,255,255,.08);color:var(--text-muted);border:1px solid rgba(255,255,255,.1);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.78rem;">取消定时</button>\n'
    '        </div>\n'
    '        <div id="admin-open-time-display" style="font-size:.75rem;color:var(--text-muted);margin-top:6px;"></div>\n'
    '      </div>\n'
    '\n'
    '      <div style="display:flex;gap:10px;flex-wrap:wrap;">\n'
    '        <button onclick="adminEnableTrading()" style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;border:none;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(22,163,74,.35)">🔓 手动开盘</button>\n'
    '      </div>\n'
    '    </div>\n'
    '\n'
    '    <hr class="divider"/>\n'
    '\n'
)

marker = '<div class="card-header" style="font-size:.95rem;margin-bottom:12px">⚠️ 天规税率调整</div>'
idx = content.find(marker)
print('marker index:', idx)

if idx >= 0:
    new_content = content[:idx] + new_section + content[idx:]
    out_path = os.path.join(os.environ.get('TEMP', r'C:\Users\ADMINI~1\AppData\Local\Temp'), 'admin_new.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('成功写入:', out_path)
    print('文件长度:', len(new_content))
else:
    print('未找到 marker')
