#!/usr/bin/env python3
"""Minimal local simulator for the Pizza Chatbot's tool endpoints.

Usage examples:
  python scripts/simulate_agent.py menu
  python scripts/simulate_agent.py create --pizza_type Margherita --size Large --quantity 2
  python scripts/simulate_agent.py status --order_id 12345
"""
import json
import os
import sys
import requests
import click

MENU_URL = os.environ.get(
    "SIM_MENU_URL",
    "https://gist.githubusercontent.com/Pradeepkarra1/770ee94f47281b8c952b744d3889ea00/raw/a6bdb41b0c7e1bda15c63ab8e7eb73dc9213b441/pizza_menu.json",
)
CREATE_ORDER_URL = os.environ.get("SIM_CREATE_URL", "https://httpbin.org/post")
CHECK_STATUS_URL = os.environ.get("SIM_STATUS_URL", "https://httpbin.org/get")
FALLBACK_CREATE = os.environ.get("SIM_FALLBACK_CREATE", "https://postman-echo.com/post")
FALLBACK_STATUS = os.environ.get("SIM_FALLBACK_STATUS", "https://postman-echo.com/get")


@click.group()
def cli():
    """Simulator CLI"""


@cli.command()
def menu():
    """Fetch and pretty-print the menu JSON"""
    try:
        resp = requests.get(MENU_URL, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching menu: {e}")
        sys.exit(2)
    data = resp.json()
    print(json.dumps(data.get("menu", data), indent=2))


@cli.command()
@click.option("--pizza_type", required=True)
@click.option("--size", required=True)
@click.option("--quantity", required=True, type=int)
@click.option("--customer_name", default="Test User")
@click.option("--delivery_address", default="123 Main St")
@click.option("--phone_number", default="555-0123")
def create(pizza_type, size, quantity, customer_name, delivery_address, phone_number):
    """Simulate creating an order (POST)"""
    payload = {
        "pizza_type": pizza_type,
        "size": size,
        "quantity": quantity,
        "customer_name": customer_name,
        "delivery_address": delivery_address,
        "phone_number": phone_number,
    }
    try:
        resp = requests.post(CREATE_ORDER_URL, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        # Try fallback for transient server errors
        resp_obj = getattr(e, 'response', None)
        status = getattr(resp_obj, 'status_code', None)
        if not status or status >= 500:
            try:
                print(f"Primary endpoint returned {status}, retrying with fallback: {FALLBACK_CREATE}", file=sys.stderr)
                resp = requests.post(FALLBACK_CREATE, json=payload, timeout=10)
                resp.raise_for_status()
            except Exception as e2:
                print(f"Fallback also failed: {e2}", file=sys.stderr)
                sys.exit(2)
        else:
            # Print response body if available for easier debugging
            body = resp_obj
            if body is not None:
                try:
                    print(json.dumps(body.json(), indent=2))
                except Exception:
                    print(body.text)
            print(f"Error creating order: {e}")
            sys.exit(2)
    print(json.dumps(resp.json(), indent=2))


@cli.command()
@click.option("--order_id", required=True)
def status(order_id):
    """Simulate checking order status (GET)"""
    try:
        resp = requests.get(CHECK_STATUS_URL, params={"order_id": order_id}, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        resp_obj = getattr(e, 'response', None)
        status = getattr(resp_obj, 'status_code', None)
        if not status or status >= 500:
            try:
                print(f"Primary endpoint returned {status}, retrying with fallback: {FALLBACK_STATUS}", file=sys.stderr)
                resp = requests.get(FALLBACK_STATUS, params={"order_id": order_id}, timeout=10)
                resp.raise_for_status()
            except Exception as e2:
                print(f"Fallback also failed: {e2}", file=sys.stderr)
                sys.exit(2)
        else:
            print(f"Error checking status: {e}", file=sys.stderr)
            sys.exit(2)
    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    cli()
