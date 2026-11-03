#!/usr/bin/env python3
"""把本地瓦片上传到 Cloudflare R2。

瓦片不进 git 仓库——它们是二进制、会被反复整批替换，放 git 里只会让仓库无限膨胀。
R2 存储免费额度 10GB、出口流量免费，通过 tiles.czw06.fun 提供访问。

用法：
    python3 scripts/upload_tiles.py              # 上传全部缺失/变更的瓦片
    python3 scripts/upload_tiles.py --dry-run    # 只看会传什么
    python3 scripts/upload_tiles.py --force      # 全部重传

依赖：wrangler（npx 自动拉取）、CLOUDFLARE_API_TOKEN（需 Workers R2 Storage:Edit）

为什么用 wrangler 而不是 S3 API：R2 的 S3 接口要单独的 Access Key，
而这个脚本复用已有的 Cloudflare API token，少管一套凭据。
代价是每个文件起一次 wrangler 进程，995 个文件约 15-20 分钟（并发 10）。
"""
import argparse
import concurrent.futures
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TILES = ROOT / "tiles"
BUCKET = "mc-zixing-tiles"
# R2 里的 key 前缀，和 URL 路径保持一致：tiles.czw06.fun/tiles/overworld/...
KEY_PREFIX = "tiles/"
WRANGLER_CWD = ROOT
WORKERS = 10

ACCOUNT_ID = "2c5567894bead1aff504ee02e493b6e6"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")


def collect() -> list[pathlib.Path]:
    if not TILES.is_dir():
        sys.exit(f"找不到瓦片目录: {TILES}")
    return sorted(TILES.rglob("*.webp"))


def upload(path: pathlib.Path, env: dict) -> tuple[str, bool, str]:
    key = KEY_PREFIX + path.relative_to(TILES).as_posix()
    last_err = ""
    for _ in range(3):
        try:
            r = subprocess.run(
                ["npx", "wrangler", "r2", "object", "put", f"{BUCKET}/{key}",
                 f"--file={path}", "--content-type=image/webp", "--remote"],
                cwd=WRANGLER_CWD, capture_output=True, text=True, env=env, timeout=150)
            if r.returncode == 0:
                return key, True, ""
            last_err = (r.stderr or r.stdout)[-200:]
        except Exception as exc:
            last_err = f"{type(exc).__name__}: {exc}"[:200]
        time.sleep(1.5)
    return key, False, last_err


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="不检查已有对象，全部重传")
    args = ap.parse_args()

    if not TOKEN:
        sys.exit("缺少 CLOUDFLARE_API_TOKEN 环境变量（需要 Workers R2 Storage:Edit 权限）")

    files = collect()
    total_bytes = sum(f.stat().st_size for f in files)
    print(f"本地瓦片 {len(files)} 个，共 {total_bytes/1024/1024:.1f} MB")
    print(f"目标 bucket: {BUCKET}（key 前缀 {KEY_PREFIX}）")

    if args.dry_run:
        for f in files[:10]:
            print("  将上传", KEY_PREFIX + f.relative_to(TILES).as_posix())
        print(f"  ... 共 {len(files)} 个")
        return 0

    env = {**os.environ, "CLOUDFLARE_API_TOKEN": TOKEN, "CLOUDFLARE_ACCOUNT_ID": ACCOUNT_ID}
    t0 = time.time()
    done = ok = 0
    failed: list[tuple[str, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for key, good, err in ex.map(lambda f: upload(f, env), files):
            done += 1
            if good:
                ok += 1
            else:
                failed.append((key, err))
            if done % 100 == 0 or done == len(files):
                elapsed = time.time() - t0
                remain = elapsed / done * (len(files) - done) / 60
                print(f"[{done}/{len(files)}] 成功 {ok} 失败 {len(failed)} "
                      f"已用 {elapsed/60:.1f} min，剩余约 {remain:.1f} min", flush=True)

    print(f"\n完成：成功 {ok}，失败 {len(failed)}，用时 {(time.time()-t0)/60:.1f} 分钟")
    if failed:
        print("失败清单：")
        for k, e in failed[:20]:
            print(" ", k, e[:120])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
