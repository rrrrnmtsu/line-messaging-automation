#!/usr/bin/env node

import dotenv from 'dotenv';
import { fetchAndExtract } from './src/modules/fetch.js';
import { extractWithLLM } from './src/modules/llm-extract-ollama.js';
import { normalizeRecord } from './src/modules/normalize.js';
import { outputCSV, outputMarkdownWithCSV, ensureOutputDir } from './src/modules/output.js';

dotenv.config();

async function testDirectUrls() {
  console.log('=== 直接URL指定テスト（10件） ===\n');

  // 確実に取得できるURL
  const testUrls = [
    'https://qiita.com/YushiYamamoto/items/1c6fa7d52a0186f58165',
    'https://qiita.com/YushiYamamoto/items/022e2eb80dd11ca051ea',
    'https://zenn.dev/ugongone/articles/c4dceb7bd7c7fd',
    'https://note.com/ryota_mt84/n/n513ad368b995',
    'https://note.com/55clotho/n/n0b87e1be7ba2',
    'https://note.com/gappon_inc/n/n32b29af648b3',
    'https://note.com/th1980/n/n5bca74449ca1',
    'https://aitaroblog.com/n8n-automation-usecase',
    'https://clmagic.net/2025/08/10/n8n-use-cases-automation-guide',
    'https://yoshikazu-komatsu.com/n8n-use-cases-5-examples',
  ];

  const records = [];
  let successCount = 0;
  let failCount = 0;

  for (const url of testUrls) {
    console.log(`\n[${successCount + failCount + 1}/${testUrls.length}] 処理中: ${url}`);

    try {
      // コンテンツ取得
      const data = await fetchAndExtract(url);
      if (!data) {
        console.log(`  ❌ コンテンツ取得失敗`);
        failCount++;
        continue;
      }

      console.log(`  ✓ コンテンツ取得成功 (${data.content.length}文字)`);

      // LLM抽出
      const record = await extractWithLLM(data, '一次情報');
      if (!record) {
        console.log(`  ❌ LLM抽出失敗`);
        failCount++;
        continue;
      }

      // 正規化
      const normalized = normalizeRecord(record);
      records.push(normalized);

      console.log(`  ✅ 抽出成功: ${normalized.タイトル}`);
      successCount++;

      // 10件達成したら終了
      if (successCount >= 10) {
        break;
      }
    } catch (error: any) {
      console.error(`  ❌ エラー: ${error.message}`);
      failCount++;
    }
  }

  console.log(`\n=== 結果サマリー ===`);
  console.log(`成功: ${successCount}件`);
  console.log(`失敗: ${failCount}件`);

  if (records.length === 0) {
    console.error('抽出されたレコードがありません');
    return;
  }

  // 出力
  const outDir = 'output';
  ensureOutputDir(outDir);

  const prefix = 'test_gptoss_direct_10';
  outputCSV(records, `${outDir}/${prefix}_full.csv`);
  outputMarkdownWithCSV(records, `${outDir}/${prefix}_main.md`);

  console.log(`\n=== 出力完了 ===`);
  console.log(`- ${outDir}/${prefix}_main.md`);
  console.log(`- ${outDir}/${prefix}_full.csv`);
}

testDirectUrls().catch(console.error);
