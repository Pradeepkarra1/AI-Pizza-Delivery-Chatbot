import json
import subprocess
import sys
import os


def run_cmd(args, env=None):
    envp = os.environ.copy()
    if env:
        envp.update(env)
    proc = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=envp)
    assert proc.returncode == 0, f"Command failed: {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_create_with_windows_style_address():
    data = run_cmd([
        "scripts/simulate_agent.py",
        "create",
        "--pizza_type",
        "Margherita",
        "--size",
        "Medium",
        "--quantity",
        "1",
        "--delivery_address",
        "C:\\Users\\Alice\\Order",
    ])
    payload = data.get("json") or data.get("data")
    assert payload is not None
    assert payload.get("delivery_address") == "C:\\Users\\Alice\\Order"


def test_create_with_unix_style_address():
    data = run_cmd([
        "scripts/simulate_agent.py",
        "create",
        "--pizza_type",
        "Margherita",
        "--size",
        "Small",
        "--quantity",
        "1",
        "--delivery_address",
        "/home/alice/order",
    ])
    payload = data.get("json") or data.get("data")
    assert payload is not None
    assert payload.get("delivery_address") == "/home/alice/order"
