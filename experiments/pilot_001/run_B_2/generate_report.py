#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Generates placeholder statistical reporting data.")
    parser.add_argument("--size", type=int, required=True, help="Size of output in KB")
    args = parser.parse_args()

    chunk = "MOCK_STATISTICAL_DATA: {" + "A"*900 + "} \n"
    # 1 KB is roughly 1 chunk
    for _ in range(args.size):
        sys.stdout.write(chunk)

if __name__ == "__main__":
    main()
