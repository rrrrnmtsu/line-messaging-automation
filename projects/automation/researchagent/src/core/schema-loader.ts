/**
 * スキーマ駆動型リサーチシステム - SchemaLoader
 *
 * YAMLファイルからリサーチスキーマを読み込み、検証・TypeScript型に変換する
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

/**
 * フィールド定義
 */
export interface FieldDefinition {
  name: string;
  type: 'string' | 'select' | 'url' | 'date';
  required: boolean;
  extraction_priority: 'high' | 'medium' | 'low';
  description: string;
  notion_type: 'title' | 'rich_text' | 'select' | 'url';
  options?: string[]; // selectの場合の選択肢
  allowed_values?: string[]; // 許可される値のリスト
  max_length?: number; // 最大文字数
  format?: string; // date等のフォーマット
}

/**
 * 検索設定
 */
export interface SearchConfig {
  base_keywords: string[];
  languages: string[];
  result_limit: number;

  // 実行パラメータ
  per_query?: number;
  concurrency?: number;
  timeout?: number;

  // ドメイン設定
  priority_domains?: string[];
  blocked_domains?: string[];
  primary_info_domains?: string[];
}

/**
 * LLM抽出設定
 */
export interface ExtractionConfig {
  model: string;
  temperature: number;
  max_tokens: number;
  prompt_template_path: string;
  retry_attempts: number;
  timeout_seconds: number;
}

/**
 * Notion連携設定
 */
export interface NotionConfig {
  database_id?: string;
  parent_page_id?: string | null;
  database_title?: string;
}

/**
 * リサーチスキーマ全体
 */
export interface ResearchSchema {
  domain: string;
  version: string;
  description: string;
  search: SearchConfig;
  schema: FieldDefinition[];
  extraction: ExtractionConfig;
  notion?: NotionConfig;
}

/**
 * スキーマローダー
 */
export class SchemaLoader {
  private schemasDir: string;
  private cachedSchemas: Map<string, ResearchSchema>;

  constructor(schemasDir: string = './schemas') {
    this.schemasDir = path.resolve(schemasDir);
    this.cachedSchemas = new Map();
  }

  /**
   * スキーマファイルを読み込む
   *
   * @param schemaName - スキーマ名（例: "n8n-case-study"）
   * @returns ResearchSchema
   */
  loadSchema(schemaName: string): ResearchSchema {
    // キャッシュチェック
    if (this.cachedSchemas.has(schemaName)) {
      return this.cachedSchemas.get(schemaName)!;
    }

    const schemaPath = path.join(this.schemasDir, `${schemaName}.yaml`);

    // ファイル存在確認
    if (!fs.existsSync(schemaPath)) {
      throw new Error(`Schema file not found: ${schemaPath}`);
    }

    // YAML読み込み
    const fileContent = fs.readFileSync(schemaPath, 'utf8');
    const schema = yaml.load(fileContent) as ResearchSchema;

    // バリデーション
    this.validateSchema(schema);

    // キャッシュに保存
    this.cachedSchemas.set(schemaName, schema);

    return schema;
  }

  /**
   * スキーマの妥当性検証
   *
   * @param schema - ResearchSchema
   */
  validateSchema(schema: ResearchSchema): void {
    // 必須フィールドチェック
    if (!schema.domain || !schema.version || !schema.description) {
      throw new Error('Schema must have domain, version, and description');
    }

    if (!schema.search || !schema.schema || !schema.extraction) {
      throw new Error('Schema must have search, schema, and extraction config');
    }

    // フィールド定義の検証
    if (!Array.isArray(schema.schema) || schema.schema.length === 0) {
      throw new Error('Schema must have at least one field definition');
    }

    // 各フィールドの検証
    for (const field of schema.schema) {
      if (!field.name || !field.type || field.required === undefined) {
        throw new Error(`Invalid field definition: ${JSON.stringify(field)}`);
      }

      // select型の場合、optionsが必要
      if (field.type === 'select' && (!field.options || field.options.length === 0)) {
        throw new Error(`Select field "${field.name}" must have options`);
      }
    }

    // 検索設定の検証
    if (!schema.search.base_keywords || schema.search.base_keywords.length === 0) {
      throw new Error('Search config must have at least one base keyword');
    }

    // 抽出設定の検証
    if (!schema.extraction.model || !schema.extraction.prompt_template_path) {
      throw new Error('Extraction config must have model and prompt_template_path');
    }
  }

  /**
   * 利用可能なスキーマ一覧を取得
   *
   * @returns スキーマ名の配列
   */
  listAvailableSchemas(): string[] {
    if (!fs.existsSync(this.schemasDir)) {
      return [];
    }

    const files = fs.readdirSync(this.schemasDir);
    return files
      .filter(file => file.endsWith('.yaml') || file.endsWith('.yml'))
      .map(file => file.replace(/\.(yaml|yml)$/, ''));
  }

  /**
   * 必須フィールドの一覧を取得
   *
   * @param schemaName - スキーマ名
   * @returns 必須フィールド名の配列
   */
  getRequiredFields(schemaName: string): string[] {
    const schema = this.loadSchema(schemaName);
    return schema.schema
      .filter(field => field.required)
      .map(field => field.name);
  }

  /**
   * Notionプロパティマッピングを生成
   *
   * @param schemaName - スキーマ名
   * @param record - データレコード（key-valueオブジェクト）
   * @returns Notion APIに渡すプロパティオブジェクト
   */
  generateNotionProperties(schemaName: string, record: Record<string, any>): any {
    const schema = this.loadSchema(schemaName);
    const properties: any = {};

    for (const field of schema.schema) {
      const value = record[field.name];

      // 値が無い場合はスキップ（required=falseの場合）
      if (value === undefined || value === null || value === '') {
        if (field.required) {
          throw new Error(`Required field "${field.name}" is missing`);
        }
        continue;
      }

      // Notion型に応じて変換
      switch (field.notion_type) {
        case 'title':
          properties[field.name] = {
            title: [{ text: { content: String(value) }}]
          };
          break;

        case 'rich_text':
          properties[field.name] = {
            rich_text: [{ text: { content: String(value) }}]
          };
          break;

        case 'select':
          properties[field.name] = {
            select: { name: String(value) }
          };
          break;

        case 'url':
          properties[field.name] = {
            url: value || null
          };
          break;

        default:
          throw new Error(`Unknown notion_type: ${field.notion_type}`);
      }
    }

    return properties;
  }

  /**
   * LLM抽出用のプロンプトを生成
   *
   * @param schemaName - スキーマ名
   * @param extractedContent - 抽出されたコンテンツ
   * @returns LLMに送信するプロンプト
   */
  generateExtractionPrompt(schemaName: string, extractedContent: string): string {
    const schema = this.loadSchema(schemaName);

    // プロンプトテンプレートを読み込み
    const templatePath = path.resolve(schema.extraction.prompt_template_path);

    if (!fs.existsSync(templatePath)) {
      throw new Error(`Prompt template not found: ${templatePath}`);
    }

    let promptTemplate = fs.readFileSync(templatePath, 'utf8');

    // フィールド定義を動的に挿入
    const fieldDescriptions = schema.schema
      .map(field => {
        const required = field.required ? '（必須）' : '（任意）';
        const options = field.options ? `\n  選択肢: ${field.options.join(', ')}` : '';
        return `- ${field.name} ${required}: ${field.description}${options}`;
      })
      .join('\n');

    // プレースホルダーを置換
    promptTemplate = promptTemplate.replace('{{FIELD_DEFINITIONS}}', fieldDescriptions);
    promptTemplate = promptTemplate.replace('{{CONTENT}}', extractedContent);

    return promptTemplate;
  }

  /**
   * TypeScriptインターフェースとしてエクスポート（型チェック用）
   *
   * @param schemaName - スキーマ名
   * @returns TypeScriptインターフェース文字列
   */
  exportAsTypeScript(schemaName: string): string {
    const schema = this.loadSchema(schemaName);
    const interfaceName = schema.domain
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join('');

    const fields = schema.schema.map(field => {
      let tsType: string;

      switch (field.type) {
        case 'string':
        case 'url':
        case 'date':
          tsType = 'string';
          break;
        case 'select':
          if (field.options && field.options.length > 0) {
            tsType = field.options.map(opt => `"${opt}"`).join(' | ');
          } else {
            tsType = 'string';
          }
          break;
        default:
          tsType = 'any';
      }

      const required = field.required ? '' : '?';
      return `  "${field.name}"${required}: ${tsType};`;
    }).join('\n');

    return `export interface ${interfaceName}Record {\n${fields}\n}`;
  }

  /**
   * スキーマ情報を表示
   *
   * @param schemaName - スキーマ名
   */
  printSchemaInfo(schemaName: string): void {
    const schema = this.loadSchema(schemaName);

    console.log(`\n========================================`);
    console.log(`スキーマ情報: ${schemaName}`);
    console.log(`========================================`);
    console.log(`ドメイン: ${schema.domain}`);
    console.log(`バージョン: ${schema.version}`);
    console.log(`説明: ${schema.description}`);
    console.log(`\nフィールド数: ${schema.schema.length}`);
    console.log(`必須フィールド: ${this.getRequiredFields(schemaName).length}/${schema.schema.length}`);
    console.log(`\n検索キーワード: ${schema.search.base_keywords.join(', ')}`);
    console.log(`対応言語: ${schema.search.languages.join(', ')}`);
    console.log(`\nLLMモデル: ${schema.extraction.model}`);
    console.log(`プロンプト: ${schema.extraction.prompt_template_path}`);

    if (schema.notion?.database_id) {
      console.log(`\nNotion DB: ${schema.notion.database_id}`);
    }

    console.log(`========================================\n`);
  }
}

/**
 * デフォルトエクスポート
 */
export default SchemaLoader;
