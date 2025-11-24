#!/usr/bin/env npx tsx
/**
 * SchemaLoaderの動作確認テスト
 *
 * 実行方法:
 * npx tsx test-schema-loader.ts
 */

import { SchemaLoader } from './src/core/schema-loader.js';
import { CaseStudyRecord } from './src/types/schema.js';

async function main() {
  console.log('==============================================');
  console.log('SchemaLoader 動作確認テスト');
  console.log('==============================================\n');

  // SchemaLoaderインスタンス作成
  const loader = new SchemaLoader('./schemas');

  // 1. 利用可能なスキーマ一覧
  console.log('[Test 1] 利用可能なスキーマ一覧');
  const schemas = loader.listAvailableSchemas();
  console.log(`  見つかったスキーマ: ${schemas.length}件`);
  schemas.forEach(name => console.log(`    - ${name}`));
  console.log();

  // 2. n8nスキーマの読み込み
  console.log('[Test 2] n8nスキーマの読み込み');
  try {
    const schema = loader.loadSchema('n8n-case-study');
    console.log(`  ✓ スキーマ読み込み成功`);
    console.log(`    ドメイン: ${schema.domain}`);
    console.log(`    バージョン: ${schema.version}`);
    console.log(`    フィールド数: ${schema.schema.length}`);
    console.log();
  } catch (error: any) {
    console.error(`  ✗ エラー: ${error.message}`);
    return;
  }

  // 3. 必須フィールドの取得
  console.log('[Test 3] 必須フィールドの取得');
  const requiredFields = loader.getRequiredFields('n8n-case-study');
  console.log(`  必須フィールド: ${requiredFields.length}件`);
  requiredFields.slice(0, 5).forEach(field => console.log(`    - ${field}`));
  if (requiredFields.length > 5) {
    console.log(`    ... 他 ${requiredFields.length - 5}件`);
  }
  console.log();

  // 4. Notionプロパティ生成テスト
  console.log('[Test 4] Notionプロパティ生成テスト');
  const testRecord: Partial<CaseStudyRecord> = {
    ID: '001',
    タイトル: 'テスト事例',
    業種: 'IT・ソフトウェア開発',
    サブ領域: 'プロジェクト管理',
    '目的/KPI': '業務効率化30%',
    トリガー種別: 'Webhook',
    入力ソース: 'GitHub',
    出力先: 'Slack',
    主要n8nノード: 'Webhook, HTTP Request, Slack',
    '外部API/連携ツール': 'GitHub API, Slack API',
    ワークフロー概要: 'GitHubイベントをSlackに通知',
    実装難易度: '2',
    '成果/ROI': '月20時間削減',
    '地域/言語': 'JP / 日本語',
    出典URL: 'https://example.com',
    情報の種類: '推定',
    重複判定キー: 'test_github_slack'
  };

  try {
    const notionProps = loader.generateNotionProperties('n8n-case-study', testRecord);
    console.log(`  ✓ Notionプロパティ生成成功`);
    console.log(`    プロパティ数: ${Object.keys(notionProps).length}`);
    console.log(`    例（ID）: ${JSON.stringify(notionProps.ID)}`);
    console.log();
  } catch (error: any) {
    console.error(`  ✗ エラー: ${error.message}`);
  }

  // 5. TypeScriptインターフェースエクスポート
  console.log('[Test 5] TypeScriptインターフェースエクスポート');
  try {
    const tsInterface = loader.exportAsTypeScript('n8n-case-study');
    console.log(`  ✓ TypeScript型定義生成成功`);
    console.log(`    型定義の最初の3行:`);
    tsInterface.split('\n').slice(0, 3).forEach(line => console.log(`      ${line}`));
    console.log('      ...');
    console.log();
  } catch (error: any) {
    console.error(`  ✗ エラー: ${error.message}`);
  }

  // 6. スキーマ情報の表示
  console.log('[Test 6] スキーマ情報の表示');
  loader.printSchemaInfo('n8n-case-study');

  console.log('==============================================');
  console.log('全てのテスト完了');
  console.log('==============================================');
}

main().catch(console.error);
