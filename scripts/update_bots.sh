#!/usr/bin/env bash
# 每天跑一次：查询服务器在线状态。只有实质变化（在线人数、假人状态）才提交推送，
# 单纯的时间戳刷新不算变化，避免白白消耗 Cloudflare Pages 构建次数（免费版 500 次/月）。
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG_PREFIX="[$(date '+%F %T')]"
echo "$LOG_PREFIX 开始检查"

env -u PYTHONPATH /usr/bin/python3 scripts/check_bots.py || {
    echo "$LOG_PREFIX 查询失败，不提交"
    exit 0
}

# 比较时忽略 lastChecked，只比真正有意义的数据
if env -u PYTHONPATH /usr/bin/python3 -c "
import json, subprocess, sys
cur = json.load(open('data/bots.json'))
old = json.loads(subprocess.run(['git', 'show', 'HEAD:data/bots.json'],
                                capture_output=True, text=True).stdout or '{}')
for d in (cur, old):
    d.pop('lastChecked', None)
sys.exit(1 if cur == old else 0)
"; then
    :
else
    git checkout -- data/bots.json
    echo "$LOG_PREFIX 状态无变化，跳过推送"
    exit 0
fi

export HTTPS_PROXY=http://192.168.1.156:7897
export HTTP_PROXY=http://192.168.1.156:7897
git add data/bots.json
git commit -q -m "chore: 更新假人在线状态 $(date +%F)"
if git push -q origin master; then
    echo "$LOG_PREFIX 状态有变化，已推送并触发部署"
else
    echo "$LOG_PREFIX 推送失败"
fi
