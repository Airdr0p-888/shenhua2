# 按行号在 admin.html 第339行前插入开盘设置模块
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\WorkBuddy\2026-06-17-21-17-01\admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('总行数:', len(lines))

# 找到包含"天规税率调整"的行（0-based 行号 = grep 行号 - 1）
target = '天规税率调整'
insert_idx = None
for i, line in enumerate(lines):
    if target in line:
        insert_idx = i
        print('找到目标行，行号:', i+1)
        print('内容:', repr(line.strip()))
        break

if insert_idx is None:
    print('未找到目标行！')
    # 模糊搜索
    for i, line in enumerate(lines):
        if '税率' in line and 'card-header' in line:
            print('候选行', i+1, ':', repr(line.strip()))
    sys.exit(1)

new_section = [
    '    <hr class="divider"/>\n',
    '\n',
    '    <div class="card-header" style="font-size:.95rem;margin-bottom:12px">🔔 开盘设置</div>\n',
    '\n',
    '    <div style="background:rgba(0,0,0,.25);border-radius:10px;padding:14px;margin-bottom:14px;">\n',
    '      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">\n',
    '        <label style="font-size:.82rem;color:var(--text-muted);cursor:pointer;">\n',
    '          <input type="checkbox" id="admin-auto-open" onchange="adminSetAutoOpenOnFill(this.checked)" style="margin-right:6px;accent-color:var(--accent1)"/>\n',
    '          Mint满自动开盘\n',
    '        </label>\n',
    '        <span id="admin-auto-open-status" style="font-size:.75rem;color:var(--accent2)"></span>\n',
    '      </div>\n',
    '\n',
    '      <div style="margin-bottom:12px;">\n',
    '        <div style="font-size:.82rem;color:var(--text-muted);margin-bottom:6px;">🕐 定时开盘（北京时间）</div>\n',
    '        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">\n',
    '          <input type="datetime-local" id="admin-open-time" style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:6px 10px;color:var(--text-body);font-size:.82rem;"/>\n',
    '          <button onclick="adminSetTradingOpenTime()" style="background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem;font-weight:600;">设定定时开盘</button>\n',
    '          <button onclick="adminCancelTradingOpenTime()" style="background:rgba(255,255,255,.08);color:var(--text-muted);border:1px solid rgba(255,255,255,.1);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.78rem;">取消定时</button>\n',
    '        </div>\n',
    '        <div id="admin-open-time-display" style="font-size:.75rem;color:var(--text-muted);margin-top:6px;"></div>\n',
    '      </div>\n',
    '\n',
    '      <div style="display:flex;gap:10px;flex-wrap:wrap;">\n',
    '        <button onclick="adminEnableTrading()" style="background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;border:none;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(22,163,74,.35)">🔓 手动开盘</button>\n',
    '      </div>\n',
    '    </div>\n',
    '\n',
    '    <hr class="divider"/>\n',
    '\n',
]

new_lines = lines[:insert_idx] + new_section + lines[insert_idx:]

out_path = os.path.join(os.environ.get('TEMP', r'C:\Users\ADMINI~1\AppData\Local\Temp'), 'admin_new.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('成功！输出文件:', out_path)
print('新行数:', len(new_lines))
