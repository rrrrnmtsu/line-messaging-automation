#!/bin/bash

# Notion エクスポートスクリプト
# test_hybrid_final_10 のデータを Notion データベースにエクスポート

DATABASE_ID="29fd6d1146cb81b09ea4db8064663e3f"
CSV_FILE="output/test_hybrid_final_10_full.csv"

echo "==================================="
echo "Notion エクスポートスクリプト"
echo "==================================="
echo "データベース ID: $DATABASE_ID"
echo "入力ファイル: $CSV_FILE"
echo ""

# CSV から2件目以降を読み込んで Notion にエクスポート
# （1件目は既にエクスポート済み）

echo "エクスポート準備完了"
echo ""
echo "現在の実装では、CLI の --export-notion オプションを使用してください:"
echo "npm run dev -- --phase 1 --target-rows 3 --per-query 2 --export-notion --out-prefix test_notion_3"
echo ""
echo "または、既存データを手動でインポートする場合は、以下のスクリプトを実行:"
echo "node import-csv-to-notion.js"
