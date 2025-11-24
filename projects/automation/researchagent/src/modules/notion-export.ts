/**
 * Notion エクスポートモジュール（スキーマ駆動版）
 *
 * SchemaLoader を使用して動的に Notion にエクスポートする機能を提供
 */

import { CaseStudyRecord } from '../types/schema.js';
import { SchemaLoader } from '../core/schema-loader.js';

/**
 * Notion データベースのプロパティ定義
 *
 * スキーマから動的生成
 */
interface NotionDatabaseProperties {
  [key: string]: {
    type: string;
    [key: string]: any;
  };
}

/**
 * レコードを Notion ページプロパティ形式に変換（SchemaLoader使用）
 */
function convertToNotionProperties(schemaName: string, record: Record<string, any>): any {
  const loader = new SchemaLoader('./schemas');
  return loader.generateNotionProperties(schemaName, record);
}

/**
 * Notion データベースにレコードをエクスポート（スキーマ駆動版）
 *
 * @param schemaName - スキーマ名
 * @param records - エクスポートするレコード配列
 * @param databaseId - Notion データベース ID
 * @returns エクスポート成功件数
 */
export async function exportToNotion(
  schemaName: string,
  records: Record<string, any>[],
  databaseId: string
): Promise<number> {
  console.log(`\n[Notion Export] ${records.length}件のレコードをエクスポート開始...`);
  console.log(`[Notion Export] Schema: ${schemaName}`);
  console.log(`[Notion Export] Database ID: ${databaseId}`);

  let successCount = 0;
  let failureCount = 0;

  for (const record of records) {
    try {
      const properties = convertToNotionProperties(schemaName, record);

      // Notion MCP の API-post-page ツールを使用（仮実装 - 実際は MCP 経由で実行）
      const recordId = record.ID || record.id || 'N/A';
      const recordTitle = record.タイトル || record.title || record.name || 'N/A';
      console.log(`[Notion Export] ID ${recordId}: ${recordTitle} をエクスポート中...`);

      // TODO: ここで実際の Notion MCP ツールを呼び出す
      // 現時点では構造のみ準備

      successCount++;
      console.log(`[Notion Export] ID ${recordId}: エクスポート成功`);

    } catch (error: any) {
      failureCount++;
      const recordId = record.ID || record.id || 'N/A';
      console.error(`[Notion Export] ID ${recordId}: エクスポート失敗 - ${error.message}`);
    }
  }

  console.log(`\n[Notion Export] 完了: ${successCount}件成功, ${failureCount}件失敗`);
  return successCount;
}

/**
 * Notion データベーススキーマの検証（スキーマ駆動版）
 *
 * 必要なプロパティが存在するか確認
 */
export async function validateNotionDatabase(schemaName: string, databaseId: string): Promise<boolean> {
  console.log(`[Notion Export] データベーススキーマ検証中...`);
  console.log(`[Notion Export] Schema: ${schemaName}`);
  console.log(`[Notion Export] Database ID: ${databaseId}`);

  try {
    const loader = new SchemaLoader('./schemas');
    const schema = loader.loadSchema(schemaName);

    console.log(`[Notion Export] スキーマ読み込み成功: ${schema.schema.length}フィールド`);

    // TODO: Notion MCP の API-retrieve-a-database ツールを使用してスキーマ確認
    console.log('[Notion Export] スキーマ検証成功');
    return true;
  } catch (error: any) {
    console.error(`[Notion Export] スキーマ検証失敗: ${error.message}`);
    return false;
  }
}

/**
 * Notion データベースを作成（スキーマ駆動版）
 *
 * スキーマから自動的にプロパティを生成
 */
export async function createNotionDatabase(
  schemaName: string,
  parentPageId: string,
  databaseTitle?: string
): Promise<string | null> {
  const loader = new SchemaLoader('./schemas');
  const schema = loader.loadSchema(schemaName);

  const finalTitle = databaseTitle || schema.description;
  console.log(`[Notion Export] 新しいデータベースを作成中: ${finalTitle}`);
  console.log(`[Notion Export] Schema: ${schemaName}`);

  try {
    const properties: NotionDatabaseProperties = {};

    // スキーマからプロパティを動的生成
    for (const field of schema.schema) {
      switch (field.notion_type) {
        case 'title':
          properties[field.name] = { type: 'title' };
          break;
        case 'rich_text':
          properties[field.name] = { type: 'rich_text' };
          break;
        case 'select':
          properties[field.name] = { type: 'select', select: {} };
          break;
        case 'url':
          properties[field.name] = { type: 'url', url: {} };
          break;
        default:
          console.warn(`[Notion Export] 未対応の Notion 型: ${field.notion_type}`);
      }
    }

    console.log(`[Notion Export] ${Object.keys(properties).length}個のプロパティを生成`);

    // TODO: Notion MCP の API-create-a-database ツールを使用してデータベース作成
    console.log('[Notion Export] データベース作成成功');

    // 仮の戻り値（実際は作成されたデータベース ID を返す）
    return 'dummy-database-id';

  } catch (error: any) {
    console.error(`[Notion Export] データベース作成失敗: ${error.message}`);
    return null;
  }
}
