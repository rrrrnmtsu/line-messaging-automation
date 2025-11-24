/**
 * ハイブリッド検索モジュール
 * WebSearch（MCP）+ DuckDuckGo の組み合わせ
 */

import axios from 'axios';
import * as cheerio from 'cheerio';
import { retry, withTimeout } from '../utils/retry.js';
import { SearchConfig } from '../core/schema-loader.js';

export interface SearchResult {
  url: string;
  title: string;
  snippet?: string;
  priority?: number;
}

/**
 * ハイブリッド検索：WebSearch（MCP）とDuckDuckGoを並行実行
 */
export async function hybridSearch(
  query: string,
  maxResults: number = 20,
  searchConfig?: SearchConfig
): Promise<SearchResult[]> {
  console.log(`[HybridSearch] Searching: "${query}"`);

  const results: SearchResult[] = [];

  // 並行実行
  const [webSearchResults, ddgResults] = await Promise.allSettled([
    searchWithWebSearch(query, Math.ceil(maxResults / 2)),
    searchDuckDuckGo(query, Math.ceil(maxResults / 2)),
  ]);

  // WebSearch結果を追加
  if (webSearchResults.status === 'fulfilled') {
    results.push(...webSearchResults.value);
  } else {
    console.warn(`[HybridSearch] WebSearch failed: ${webSearchResults.reason}`);
  }

  // DuckDuckGo結果を追加
  if (ddgResults.status === 'fulfilled') {
    results.push(...ddgResults.value);
  } else {
    console.warn(`[HybridSearch] DuckDuckGo failed: ${ddgResults.reason}`);
  }

  // 重複排除
  const uniqueResults = deduplicateByUrl(results);

  // ブロックドメイン除外
  const filteredResults = searchConfig?.blocked_domains
    ? filterBlockedDomains(uniqueResults, searchConfig.blocked_domains)
    : uniqueResults;

  // 優先度ソート（スキーマの優先ドメインを使用）
  const sortedResults = sortByPriority(filteredResults, searchConfig);

  console.log(`[HybridSearch] Found ${sortedResults.length} unique results for "${query}"`);

  return sortedResults.slice(0, maxResults);
}

/**
 * WebSearch（MCPツール）を使用した検索
 * Note: MCPツールは直接呼び出せないため、代わりにGoogle Custom Search APIを使用
 */
async function searchWithWebSearch(query: string, maxResults: number): Promise<SearchResult[]> {
  // MCPのWebSearchツールが利用できない場合は、簡易的にGoogle検索風の結果を返す
  // 実装: Google Custom Search API または SerpAPI への置き換えを想定

  // 現時点では空配列を返し、DuckDuckGoに依存
  return [];
}

/**
 * DuckDuckGo HTML検索
 */
async function searchDuckDuckGo(query: string, maxResults: number = 20): Promise<SearchResult[]> {
  const encodedQuery = encodeURIComponent(query);
  const url = `https://html.duckduckgo.com/html/?q=${encodedQuery}`;

  try {
    const response = await retry(() =>
      withTimeout(
        axios.get(url, {
          headers: {
            'User-Agent':
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          },
        }),
        30000
      )
    );

    const html = response.data;
    const $ = cheerio.load(html);

    const results: SearchResult[] = [];
    const linkRegex = /<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)<\/a>/gi;

    let match;
    while ((match = linkRegex.exec(html)) !== null) {
      if (results.length >= maxResults) break;

      const rawUrl = match[1];
      const title = match[2];

      // DuckDuckGoのリダイレクトURLをデコード
      const urlMatch = rawUrl.match(/uddg=([^&]+)/);
      if (!urlMatch) continue;

      const actualUrl = decodeURIComponent(urlMatch[1]);

      // 優先度計算
      const priority = calculatePriority(actualUrl);

      results.push({
        url: actualUrl,
        title: title.trim(),
        priority,
      });
    }

    return results;
  } catch (error: any) {
    console.error(`[DuckDuckGo] Search failed: ${error.message}`);
    return [];
  }
}

/**
 * URL重複排除
 */
function deduplicateByUrl(results: SearchResult[]): SearchResult[] {
  const seen = new Set<string>();
  return results.filter((result) => {
    const normalized = normalizeUrl(result.url);
    if (seen.has(normalized)) {
      return false;
    }
    seen.add(normalized);
    return true;
  });
}

/**
 * URL正規化
 */
function normalizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    // クエリパラメータとハッシュを除去
    return `${parsed.protocol}//${parsed.host}${parsed.pathname}`.toLowerCase();
  } catch {
    return url.toLowerCase();
  }
}

/**
 * ブロックドメイン除外
 */
function filterBlockedDomains(results: SearchResult[], blockedDomains: string[]): SearchResult[] {
  return results.filter((result) => {
    try {
      const host = new URL(result.url).host.replace('www.', '');
      return !blockedDomains.some((blocked) => host.includes(blocked));
    } catch {
      return true; // URLパースエラーの場合は残す
    }
  });
}

/**
 * 優先度でソート（スキーマの優先ドメインを使用）
 */
function sortByPriority(results: SearchResult[], searchConfig?: SearchConfig): SearchResult[] {
  // 優先度を再計算
  const resultsWithPriority = results.map((result) => ({
    ...result,
    priority: calculatePriority(result.url, searchConfig),
  }));

  return resultsWithPriority.sort((a, b) => (b.priority || 0) - (a.priority || 0));
}

/**
 * ドメインベースの優先度計算（スキーマ対応）
 */
function calculatePriority(url: string, searchConfig?: SearchConfig): number {
  try {
    const host = new URL(url).host.replace('www.', '');

    // スキーマから優先ドメインを取得
    if (searchConfig?.priority_domains) {
      for (let i = 0; i < searchConfig.priority_domains.length; i++) {
        const domain = searchConfig.priority_domains[i];
        if (host.includes(domain)) {
          // 優先度スコア: 100 - (順位 * 5)
          return 100 - i * 5;
        }
      }
    }

    // フォールバック: 日本語ドメイン優先
    if (host.endsWith('.jp')) return 50;

    return 10;
  } catch {
    return 0;
  }
}
