#!/usr/bin/env bash
# 每天跑一次：查询服务器在线状态，仅在数据有变化时提交推送。
# 无变化不推送，避免白白消耗 Cloudflare Pages 的构建次数（免费版 500 次/月）。
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG_PREFIX="[$(date '+%F %T')]"
echo "$LOG_PREFIX 开始检查"

env -u PYTHONPATH /usr/bin/python3 scripts/check_bots.py || {
    echo "$LOG_PREFIX 查询失败，不提交"
    exit 0
}

if git diff --quiet -- data/bots.json; then
    echo "$LOG_PREFIX 数据无变化，跳过推送"
    exit 0
fi

export HTTPS_PROXY=http://192.168.1.156:7897
export HTTP_PROXY=http://192.168.1.156:7897
git add data/bots.json
git commit -q -m "chore: 更新假人在线状态 $(date +%F)"
if git push -q origin master; then
    echo "$LOG_PREFIX 已推送，触发部署"
else
    echo "$LOG_PREFIX 推送失败"
fi
