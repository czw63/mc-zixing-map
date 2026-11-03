#!/usr/bin/env python3
"""查询紫星服务器在线状态与假人，更新 data/bots.json。

用 Minecraft SLP（Server List Ping）协议直连游戏端口，不需要 RCON 或后台权限。
只读操作，不改服务器任何状态。

用法：
    env -u PYTHONPATH /usr/bin/python3 scripts/check_bots.py          # 只更新本地
    env -u PYTHONPATH /usr/bin/python3 scripts/check_bots.py --json   # 打印结果

SLP 的 players.sample 只包含服务器愿意公开的在线玩家，所以：
  - 只能看到"在线"的假人，离线的看不到
  - 服务器设置 sample 隐藏时会是空列表
"""
import json
import socket
import struct
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOST = "mc.zixing.fun"
PORT = 7030
PROTOCOL = 769          # 26.x 握手版本，服务端通常不校验
TIMEOUT = 10
CST = timezone(timedelta(hours=8))
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bots.json"


def _varint(n: int) -> bytes:
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        out += bytes([b | 0x80]) if n else bytes([b])
        if not n:
            return out


def _read_varint(sock) -> int:
    n = shift = 0
    while True:
        b = sock.recv(1)
        if not b:
            raise EOFError("连接被关闭")
        n |= (b[0] & 0x7F) << shift
        shift += 7
        if not b[0] & 0x80:
            return n


def status(host: str = HOST, port: int = PORT, timeout: int = TIMEOUT) -> dict:
    sock = socket.create_connection((host, port), timeout=timeout)
    sock.settimeout(timeout)
    try:
        h = host.encode("utf-8")
        payload = (b"\x00" + _varint(PROTOCOL) + _varint(len(h)) + h
                   + struct.pack(">H", port) + b"\x01")
        sock.sendall(_varint(len(payload)) + payload)
        sock.sendall(_varint(1) + b"\x00")           # status request
        _read_varint(sock)                            # packet length
        _read_varint(sock)                            # packet id
        jlen = _read_varint(sock)
        buf = b""
        while len(buf) < jlen:
            chunk = sock.recv(jlen - len(buf))
            if not chunk:
                break
            buf += chunk
        return json.loads(buf.decode("utf-8"))
    finally:
        sock.close()


def main() -> int:
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    now = datetime.now(CST).isoformat(timespec="seconds")
    try:
        st = status()
    except Exception as exc:                          # 服务器关服或网络不通
        doc["serverOnline"] = False
        doc["lastChecked"] = now
        doc["onlineCount"] = None
        doc["error"] = f"{type(exc).__name__}: {exc}"
        for bot in doc["bots"]:
            bot["status"] = "unknown"
        DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print(f"服务器不可达（{type(exc).__name__}），已记录")
        return 1

    players = st.get("players") or {}
    online = [x.get("name") for x in (players.get("sample") or []) if x.get("name")]
    doc["serverOnline"] = True
    doc["lastChecked"] = now
    doc["onlineCount"] = players.get("online")
    doc["maxPlayers"] = players.get("max")
    doc["version"] = (st.get("version") or {}).get("name")
    doc.pop("error", None)

    known = {b["name"] for b in doc["bots"]}
    for bot in doc["bots"]:
        bot["status"] = "online" if bot["name"] in online else "offline"
    for name in online:                               # 新出现的假人自动补进来
        if name not in known:
            doc["bots"].append({
                "name": name, "purpose": None, "location": None,
                "status": "online",
                "notes": "自动发现在线，用途待补。",
            })

    DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{now}  在线 {players.get('online')}/{players.get('max')}  "
          f"假人 {len(online)}: {', '.join(online) or '无'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
