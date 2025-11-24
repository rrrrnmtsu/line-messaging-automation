#!/usr/bin/env node

import dotenv from 'dotenv';
import { fetchAndExtract } from './src/modules/fetch.js';
import { extractWithLLM } from './src/modules/llm-extract-ollama.js';

dotenv.config();

async function testOllama() {
  console.log('=== Ollama + Qwen3:30b テスト ===\n');

  // テストURL: QiitaのN8n記事
  const testUrl = 'https://qiita.com/YushiYamamoto/items/1c6fa7d52a0186f58165';

  console.log(`[1] コンテンツ取得: ${testUrl}`);
  const data = await fetchAndExtract(testUrl);

  if (!data) {
    console.error('コンテンツ取得失敗');
    return;
  }

  console.log(`✓ 取得成功 (${data.content.length}文字)`);
  console.log(`タイトル: ${data.title}`);
  console.log(`ホスト: ${data.host}`);
  console.log('\n[2] LLM抽出開始...');

  const record = await extractWithLLM(data, '一次情報');

  if (!record) {
    console.error('LLM抽出失敗');
    return;
  }

  console.log('\n✓ 抽出成功！\n');
  console.log('=== 抽出結果 ===');
  console.log(`タイトル: ${record.タイトル}`);
  console.log(`業種: ${record.業種}`);
  console.log(`目的/KPI: ${record['目的/KPI']}`);
  console.log(`主要n8nノード: ${record.主要n8nノード}`);
  console.log(`情報の種類: ${record.情報の種類}`);
  console.log('\n=== 完了 ===');
}

testOllama().catch(console.error);
