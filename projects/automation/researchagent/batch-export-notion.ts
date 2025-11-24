#!/usr/bin/env node
/**
 * バッチ Notion エクスポートスクリプト
 *
 * 既存の CSV ファイルから Notion にデータをエクスポート
 */

import { readFileSync } from 'fs';
import { join } from 'path';

interface CaseStudyRecord {
  ID: string;
  タイトル: string;
  業種: string;
  サブ領域: string;
  '目的/KPI': string;
  トリガー種別: string;
  入力ソース: string;
  出力先: string;
  主要n8nノード: string;
  '外部API/連携ツール': string;
  ワークフロー概要: string;
  実装難易度: string;
  規模目安: string;
  '成果/ROI': string;
  '運用上のリスク/前提': string;
  '地域/言語': string;
  出典URL: string;
  情報の種類: string;
  '公開日/更新日': string;
  重複判定キー: string;
}

const DATABASE_ID = '29fd6d1146cb81b09ea4db8064663e3f';

// CSV パース関数
function parseCSV(csvPath: string): CaseStudyRecord[] {
  const csv = readFileSync(csvPath, 'utf-8');
  const lines = csv.split('\n').slice(1); // ヘッダースキップ
  const records: CaseStudyRecord[] = [];

  for (const line of lines) {
    if (!line.trim()) continue;

    // CSV パース（ダブルクォート対応）
    const values: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];

      if (char === '"' && (i === 0 || line[i - 1] !== '\\')) {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.replace(/^"|"$/g, ''));
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.replace(/^"|"$/g, ''));

    if (values.length >= 20) {
      records.push({
        ID: values[0],
        タイトル: values[1],
        業種: values[2],
        サブ領域: values[3],
        '目的/KPI': values[4],
        トリガー種別: values[5],
        入力ソース: values[6],
        出力先: values[7],
        主要n8nノード: values[8],
        '外部API/連携ツール': values[9],
        ワークフロー概要: values[10],
        実装難易度: values[11],
        規模目安: values[12],
        '成果/ROI': values[13],
        '運用上のリスク/前提': values[14],
        '地域/言語': values[15],
        出典URL: values[16],
        情報の種類: values[17],
        '公開日/更新日': values[18],
        重複判定キー: values[19]
      });
    }
  }

  return records;
}

// Notion プロパティに変換
function toNotionProperties(record: CaseStudyRecord): any {
  return {
    'ID': {
      title: [{ text: { content: record.ID || '' }}]
    },
    'タイトル': {
      rich_text: [{ text: { content: record.タイトル || '' }}]
    },
    '業種': {
      select: { name: record.業種 || '不明' }
    },
    'サブ領域': {
      rich_text: [{ text: { content: record.サブ領域 || '' }}]
    },
    '目的/KPI': {
      rich_text: [{ text: { content: record['目的/KPI'] || '' }}]
    },
    'トリガー種別': {
      rich_text: [{ text: { content: record.トリガー種別 || '' }}]
    },
    '入力ソース': {
      rich_text: [{ text: { content: record.入力ソース || '' }}]
    },
    '出力先': {
      rich_text: [{ text: { content: record.出力先 || '' }}]
    },
    '主要n8nノード': {
      rich_text: [{ text: { content: record.主要n8nノード || '' }}]
    },
    '外部API/連携ツール': {
      rich_text: [{ text: { content: record['外部API/連携ツール'] || '' }}]
    },
    'ワークフロー概要': {
      rich_text: [{ text: { content: record.ワークフロー概要 || '' }}]
    },
    '実装難易度': {
      select: { name: record.実装難易度 || '不明' }
    },
    '規模目安': {
      rich_text: [{ text: { content: record.規模目安 || '' }}]
    },
    '成果/ROI': {
      rich_text: [{ text: { content: record['成果/ROI'] || '' }}]
    },
    '運用上のリスク/前提': {
      rich_text: [{ text: { content: record['運用上のリスク/前提'] || '' }}]
    },
    '地域/言語': {
      select: { name: record['地域/言語'] || '不明' }
    },
    '出典URL': {
      url: record.出典URL || null
    },
    '情報の種類': {
      select: { name: record.情報の種類 || '推定' }
    },
    '公開日/更新日': {
      rich_text: [{ text: { content: record['公開日/更新日'] || '' }}]
    },
    '重複判定キー': {
      rich_text: [{ text: { content: record.重複判定キー || '' }}]
    }
  };
}

async function main() {
  console.log('==============================================');
  console.log('Notion バッチエクスポート');
  console.log('==============================================\n');

  const csvPath = join(process.cwd(), 'output', 'test_hybrid_final_10_full.csv');
  console.log(`CSV ファイル: ${csvPath}`);
  console.log(`データベース ID: ${DATABASE_ID}\n`);

  console.log('CSV 読み込み中...');
  const records = parseCSV(csvPath);
  console.log(`✓ ${records.length}件のレコードを読み込みました\n`);

  // 最初の3件のみエクスポート（テスト）
  const maxExport = 3;
  const toExport = records.slice(0, maxExport);

  console.log(`最初の${maxExport}件をエクスポートします:\n`);

  for (const record of toExport) {
    console.log(`- ID ${record.ID}: ${record.タイトル.substring(0, 50)}...`);
  }

  console.log('\n注意: このスクリプトは表示のみです。');
  console.log('実際のエクスポートには Notion MCP ツールが必要です。');
  console.log('\n以下のコマンドで各レコードをエクスポートできます:');
  console.log('mcp__notion__API-post-page を使用');
}

main().catch(console.error);
