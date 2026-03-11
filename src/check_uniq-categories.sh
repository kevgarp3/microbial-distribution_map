#!/bin/bash
f=$1
echo ""
echo "Unique categories:"
tail -n +2 "$f" | awk -F "\t" '$2 != "None" {print $2}' | sort | uniq -c
echo ""