import json
import os
import subprocess
import sys


def run_cmd(args):
    proc = subprocess.run([sys.executable] + args, capture_output=True, text=True)
    assert proc.returncode == 0, f"Command failed: {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    return proc.stdout


def run_cmd_env(args, env=None):
    envp = os.environ.copy()
    if env:
        envp.update(env)
    proc = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=envp)
    return proc


def test_create_missing_args_shows_usage_error():
    proc = run_cmd_env([
        "scripts/simulate_agent.py",
        "create",
        "--pizza_type",
        "Margherita",
    ])
    assert proc.returncode != 0
    stderr = (proc.stderr or "").lower()
    assert "usage" in stderr or "error" in stderr


def test_help_output():
    proc = run_cmd_env(["scripts/simulate_agent.py", "--help"]) 
    assert proc.returncode == 0
    assert "Usage" in proc.stdout


def test_menu():
    out = run_cmd(["scripts/simulate_agent.py", "menu"])
    data = json.loads(out)
    assert isinstance(data, list)
    assert "category" in data[0]


def test_create():
    out = run_cmd([
        "scripts/simulate_agent.py",
        "create",
        "--pizza_type",
        "Margherita",
        "--size",
        "Large",
        "--quantity",
        "1",
        "--customer_name",
        "CI Test",
    ])
    data = json.loads(out)
    # Response should include an echo of the JSON payload under either 'json' or 'data'
    assert any(k in data for k in ("json", "data"))


def test_status():
    out = run_cmd(["scripts/simulate_agent.py", "status", "--order_id", "ci-123"])
    data = json.loads(out)
    # Response contains args with order_id
    args = data.get("args")
    assert args and args.get("order_id") == "ci-123"


def test_create_fallback_on_primary_failure():
    # Point primary to an unroutable port to force a failure and trigger fallback
    env = {"SIM_CREATE_URL": "http://127.0.0.1:9"}
    proc = run_cmd_env([
        "scripts/simulate_agent.py",
        "create",
        "--pizza_type",
        "Margherita",
        "--size",
        "Large",
        "--quantity",
        "1",
        "--customer_name",
        "Fallback Test",
    ], env=env)
    # Should succeed using fallback endpoint
    assert proc.returncode == 0, f"STDERR: {proc.stderr}"
    assert "retrying with fallback" in proc.stderr.lower()
    data = json.loads(proc.stdout)
    assert any(k in data for k in ("json", "data"))


def test_menu_failure_exits_nonzero():
    env = {"SIM_MENU_URL": "http://127.0.0.1:9"}
    proc = run_cmd_env(["scripts/simulate_agent.py", "menu"], env=env)
    assert proc.returncode != 0
