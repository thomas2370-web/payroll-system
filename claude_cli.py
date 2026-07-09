#!/usr/bin/env python3
"""
Simple CLI to call Anthropic Claude via REST API.

Usage examples:
  # PowerShell (temporary env var)
  $env:ANTHROPIC_API_KEY = "sk-..."
  python claude_cli.py --prompt "Hello Claude!"

  # Read prompt from a file
  python claude_cli.py --model claude-2.1 < myprompt.txt

Requires the `ANTHROPIC_API_KEY` environment variable to be set.
"""

import os
import sys
import argparse
import json
import requests


def main():
    parser = argparse.ArgumentParser(description="Simple Claude CLI using Anthropic REST API")
    parser.add_argument("--model", default="claude-2.1", help="Claude model to call (default: claude-2.1)")
    parser.add_argument("--prompt", help="Prompt text. If omitted, reads from stdin")
    parser.add_argument("--max-tokens", type=int, default=300, dest="max_tokens",
                        help="Maximum tokens to sample (default: 300)")
    parser.add_argument("--endpoint", help="Override Claude API endpoint (for advanced use)")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: set ANTHROPIC_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if args.prompt:
        prompt = args.prompt
    else:
        prompt = sys.stdin.read()
        if not prompt or not prompt.strip():
            print("Error: no prompt provided via --prompt or stdin", file=sys.stderr)
            sys.exit(1)

    payload = {
        "model": args.model,
        "prompt": prompt,
        "max_tokens_to_sample": args.max_tokens,
    }

    url = args.endpoint or "https://api.anthropic.com/v1/complete"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except Exception as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except Exception:
        print("Non-JSON response:\n", resp.text, file=sys.stderr)
        sys.exit(1)

    # Extract plausible completion fields used by different API versions
    completion = data.get("completion") or data.get("text") or data.get("output") or data.get("response")
    if completion is None:
        print(json.dumps(data, indent=2))
    else:
        print(completion)


if __name__ == "__main__":
    main()
