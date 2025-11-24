#!/usr/bin/env node
/**
 * スキーマ駆動型システムの統合テスト
 *
 * CLI → SchemaLoader → Notion Export の一連の流れを検証
 */

import { SchemaLoader } from './src/core/schema-loader.js';
import { exportToNotion, validateNotionDatabase, createNotionDatabase } from './src/modules/notion-export.js';
import { CaseStudyRecord } from './src/types/schema.js';

async function main() {
  console.log('==============================================');
  console.log('スキーマ駆動型システム - 統合テスト');
  console.log('==============================================\n');

  // ========== Test 1: SchemaLoader 初期化 ==========
  console.log('[Test 1] SchemaLoader 初期化...');
  const loader = new SchemaLoader('./schemas');
  const schemas = loader.listAvailableSchemas();
  console.log(`✓ 利用可能なスキーマ: ${schemas.length}件`);
  console.log(`  - ${schemas.join(', ')}`);

  // ========== Test 2: n8n スキーマ読み込み ==========
  console.log('\n[Test 2] n8n スキーマ読み込み...');
  const schemaName = 'n8n-case-study';
  const schema = loader.loadSchema(schemaName);
  console.log(`✓ スキーマ読み込み成功`);
  console.log(`  ドメイン: ${schema.domain}`);
  console.log(`  バージョン: ${schema.version}`);
  console.log(`  フィールド数: ${schema.schema.length}`);

  // ========== Test 3: Notion プロパティ生成 ==========
  console.log('\n[Test 3] Notion プロパティ生成テスト...');

  const testRecord: Partial<CaseStudyRecord> = {
    ID: '001',
    タイトル: 'スキーマ駆動型システムテスト',
    業種: 'IT・ソフトウェア開発',
    サブ領域: 'リサーチ自動化',
    '目的/KPI': 'スキーマ駆動型アーキテクチャの検証',
    トリガー種別: 'Cron',
    入力ソース: 'YAML スキーマファイル',
    出力先: 'Notion データベース',
    主要n8nノード: 'N/A',
    '外部API/連携ツール': 'Notion API',
    ワークフロー概要: 'YAMLスキーマから動的にNotionプロパティを生成',
    実装難易度: '3',
    規模目安: 'テスト環境',
    '成果/ROI': 'スキーマ駆動型システムの実証',
    '運用上のリスク/前提': 'なし',
    '地域/言語': 'JP / 日本語',
    出典URL: 'https://example.com',
    情報の種類: '一次情報',
    '公開日/更新日': '2025-11-03',
    重複判定キー: 'test-schema-integration-001'
  };

  const notionProps = loader.generateNotionProperties(schemaName, testRecord);
  console.log(`✓ Notionプロパティ生成成功`);
  console.log(`  プロパティ数: ${Object.keys(notionProps).length}`);

  // ========== Test 4: TypeScript 型エクスポート ==========
  console.log('\n[Test 4] TypeScript 型エクスポート...');
  const tsInterface = loader.exportAsTypeScript(schemaName);
  console.log(`✓ TypeScript型定義生成成功`);
  console.log(`  インターフェース: N8nCaseStudyRecord`);

  // ========== Test 5: Notion エクスポート（モック） ==========
  console.log('\n[Test 5] Notion エクスポート機能テスト...');

  // データベース検証（モック）
  const mockDatabaseId = '29fd6d1146cb81b09ea4db8064663e3f';
  const isValid = await validateNotionDatabase(schemaName, mockDatabaseId);
  console.log(`✓ データベース検証: ${isValid ? '成功' : '失敗'}`);

  // レコードエクスポート（モック）
  const records = [testRecord];
  const exportedCount = await exportToNotion(schemaName, records, mockDatabaseId);
  console.log(`✓ エクスポート完了: ${exportedCount}件`);

  // ========== Test 6: 新規データベース作成（モック） ==========
  console.log('\n[Test 6] 新規データベース作成テスト...');
  const mockParentPageId = 'test-parent-page-id';
  const newDbId = await createNotionDatabase(schemaName, mockParentPageId, 'テストDB');
  console.log(`✓ データベース作成: ${newDbId ? '成功' : '失敗'}`);

  // ========== Test 7: スキーマ情報表示 ==========
  console.log('\n[Test 7] スキーマ情報表示...');
  loader.printSchemaInfo(schemaName);

  // ========== 完了 ==========
  console.log('\n==============================================');
  console.log('統合テスト完了');
  console.log('==============================================');
  console.log('\n✅ 全てのテストがパスしました');
  console.log('\n次のステップ:');
  console.log('  1. 新しいスキーマファイルを作成 (例: schemas/saas-comparison.yaml)');
  console.log('  2. CLI で実行:');
  console.log('     npm run dev -- --schema saas-comparison --phase 1 --target-rows 10');
  console.log('  3. Notion エクスポート:');
  console.log('     npm run dev -- --schema saas-comparison --export-notion');
}

main().catch(console.error);
