#!/usr/bin/env node

import { hybridSearch } from './src/modules/search-hybrid.js';

async function testHybridSearch() {
  console.log('=== ハイブリッド検索テスト ===\n');

  const testQueries = [
    'n8n 事例',
    'n8n 導入事例',
    'n8n 自動化 ワークフロー'
  ];

  for (const query of testQueries) {
    console.log(`\n[テスト] クエリ: "${query}"`);

    const results = await hybridSearch(query, 10);

    console.log(`結果: ${results.length}件\n`);

    results.slice(0, 5).forEach((result, i) => {
      console.log(`${i + 1}. [優先度: ${result.priority}] ${result.title}`);
      console.log(`   ${result.url}`);
    });
  }

  console.log('\n=== テスト完了 ===');
}

testHybridSearch().catch(console.error);
