/**
 * Notion エクスポート機能のテストスクリプト
 *
 * test_hybrid_final_10 のデータを Notion にエクスポート
 */

import { readFileSync } from 'fs';
import { join } from 'path';
import { CaseStudyRecord } from './src/types/schema.js';

// CSV を読み込んで CaseStudyRecord に変換
function loadTestData(): CaseStudyRecord[] {
  const csvPath = join(process.cwd(), 'output', 'test_hybrid_final_10_full.csv');
  const csv = readFileSync(csvPath, 'utf-8');

  const lines = csv.split('\n').slice(1); // ヘッダーをスキップ
  const records: CaseStudyRecord[] = [];

  for (const line of lines) {
    if (!line.trim()) continue;

    // CSV パース（簡易版 - ダブルクォートを考慮）
    const values: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];

      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current);
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current); // 最後の値

    if (values.length >= 20) {
      records.push({
        ID: values[0].replace(/"/g, ''),
        タイトル: values[1].replace(/"/g, ''),
        業種: values[2].replace(/"/g, '') as any,
        サブ領域: values[3].replace(/"/g, ''),
        '目的/KPI': values[4].replace(/"/g, ''),
        トリガー種別: values[5].replace(/"/g, ''),
        入力ソース: values[6].replace(/"/g, ''),
        出力先: values[7].replace(/"/g, ''),
        主要n8nノード: values[8].replace(/"/g, ''),
        '外部API/連携ツール': values[9].replace(/"/g, ''),
        ワークフロー概要: values[10].replace(/"/g, ''),
        実装難易度: values[11].replace(/"/g, ''),
        規模目安: values[12].replace(/"/g, ''),
        '成果/ROI': values[13].replace(/"/g, ''),
        '運用上のリスク/前提': values[14].replace(/"/g, ''),
        '地域/言語': values[15].replace(/"/g, ''),
        出典URL: values[16].replace(/"/g, ''),
        情報の種類: values[17].replace(/"/g, '') as any,
        '公開日/更新日': values[18].replace(/"/g, ''),
        重複判定キー: values[19].replace(/"/g, '')
      });
    }
  }

  return records;
}

async function main() {
  console.log('[Test] テストデータ読み込み...');
  const records = loadTestData();
  console.log(`[Test] ${records.length}件のレコードを読み込みました`);

  // データベース ID（環境変数から）
  const databaseId = process.env.NOTION_DATABASE_ID || '29fd6d1146cb81b09ea4db8064663e3f';

  console.log(`\n[Test] Notion にエクスポート開始...`);
  console.log(`[Test] Database ID: ${databaseId}`);

  // 最初の3件のみテスト（ID 002, 003）
  const testRecords = records.slice(1, 3);

  for (const record of testRecords) {
    console.log(`\n[Test] ID ${record.ID}: ${record.タイトル}`);
    console.log('  このレコードを Notion にエクスポートします...');

    // 実際のエクスポート処理は CLI から実行
    // ここでは構造のみ確認
    console.log('  ✓ 準備完了');
  }

  console.log('\n[Test] テスト完了');
  console.log('\n実際のエクスポートは以下のコマンドで実行してください:');
  console.log('npm run dev -- --phase 1 --target-rows 3 --per-query 2 --export-notion --out-prefix test_notion_export_3');
}

main().catch(console.error);
