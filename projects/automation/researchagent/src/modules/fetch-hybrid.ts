/**
 * ハイブリッド取得モジュール
 * axios（高速）→ Puppeteer（確実）のフォールバック
 */

import axios from 'axios';
import * as cheerio from 'cheerio';
import { retry, withTimeout } from '../utils/retry.js';
import { ExtractedData } from '../types/schema.js';

/**
 * ハイブリッド取得：axiosで試行 → 失敗時はPuppeteerでリトライ
 */
export async function fetchAndExtractHybrid(url: string): Promise<ExtractedData | null> {
  console.log(`[FetchHybrid] Fetching: ${url}`);

  // まずaxiosで高速取得を試行
  try {
    const result = await fetchWithAxios(url);
    if (result && result.content.length >= 400) {
      console.log(`  ✓ Axios取得成功 (${result.content.length}文字)`);
      return result;
    }
  } catch (error: any) {
    console.warn(`  ⚠ Axios失敗: ${error.message}`);
  }

  // axiosで失敗 → Puppeteerでリトライ
  console.log(`  → Puppeteerでリトライ...`);
  try {
    const result = await fetchWithPuppeteer(url);
    if (result && result.content.length >= 400) {
      console.log(`  ✓ Puppeteer取得成功 (${result.content.length}文字)`);
      return result;
    }
  } catch (error: any) {
    console.error(`  ✗ Puppeteer失敗: ${error.message}`);
  }

  console.error(`[FetchHybrid] 取得失敗: ${url}`);
  return null;
}

/**
 * axiosでの取得（既存ロジック）
 */
async function fetchWithAxios(url: string): Promise<ExtractedData | null> {
  const response = await retry(() =>
    withTimeout(
      axios.get(url, {
        headers: {
          'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          Accept:
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        },
        timeout: 30000,
      }),
      30000
    )
  );

  const html = response.data;
  const $ = cheerio.load(html);

  const host = new URL(url).host;
  const title = extractTitle($);
  const publishedDate = extractPublishedDate($);
  const content = extractMainContent($);
  const { lang, region } = detectLangRegion($, url);

  if (content.length < 400) {
    return null;
  }

  return {
    url,
    host,
    title,
    content: content.substring(0, 6000),
    publishedDate: publishedDate || undefined,
    detectedLang: lang,
    detectedRegion: region,
  };
}

/**
 * Puppeteerでの取得
 * Note: MCPのPuppeteerツールを使用
 */
async function fetchWithPuppeteer(url: string): Promise<ExtractedData | null> {
  try {
    // MCPツールを動的にimport
    // 注: 実際の環境では、MCPツールが利用可能である必要があります

    // ページナビゲーション
    // await mcp__puppeteer__puppeteer_navigate({ url });

    // JavaScript実行でコンテンツ抽出
    // const content = await mcp__puppeteer__puppeteer_evaluate({
    //   script: `
    //     // メインコンテンツを抽出
    //     const article = document.querySelector('article')
    //       || document.querySelector('main')
    //       || document.querySelector('.content')
    //       || document.body;
    //
    //     // テキスト抽出
    //     return article.innerText || '';
    //   `
    // });

    // タイトル取得
    // const title = await mcp__puppeteer__puppeteer_evaluate({
    //   script: `document.title || ''`
    // });

    // TODO: 実際のMCP Puppeteer統合
    // 現時点ではプレースホルダー
    console.warn(`[FetchPuppeteer] Not implemented yet for: ${url}`);
    return null;

    // const host = new URL(url).host;
    // return {
    //   url,
    //   host,
    //   title: title as string,
    //   content: (content as string).substring(0, 6000),
    //   publishedDate: null,
    // };
  } catch (error: any) {
    throw new Error(`Puppeteer fetch failed: ${error.message}`);
  }
}

/**
 * タイトル抽出
 */
function extractTitle($: cheerio.CheerioAPI): string {
  return (
    $('meta[property="og:title"]').attr('content') ||
    $('meta[name="twitter:title"]').attr('content') ||
    $('title').text() ||
    $('h1').first().text() ||
    'No Title'
  ).trim();
}

/**
 * 公開日抽出
 */
function extractPublishedDate($: cheerio.CheerioAPI): string | null {
  const dateStr =
    $('meta[property="article:published_time"]').attr('content') ||
    $('meta[name="pubdate"]').attr('content') ||
    $('time[datetime]').attr('datetime') ||
    $('time').text();

  if (!dateStr) return null;

  // ISO形式に変換を試みる
  try {
    const date = new Date(dateStr);
    if (!isNaN(date.getTime())) {
      return date.toISOString().split('T')[0];
    }
  } catch {
    // パース失敗
  }

  return dateStr.trim();
}

/**
 * メインコンテンツ抽出
 */
function extractMainContent($: cheerio.CheerioAPI): string {
  // 不要な要素を削除
  $('script, style, nav, header, footer, aside, iframe, noscript').remove();

  // メインコンテンツを抽出
  const selectors = [
    'article',
    'main',
    '[role="main"]',
    '.article-body',
    '.post-content',
    '.entry-content',
    '.content',
    '#content',
    'body',
  ];

  for (const selector of selectors) {
    const element = $(selector).first();
    if (element.length > 0) {
      const text = element.text().replace(/\s+/g, ' ').trim();
      if (text.length >= 400) {
        return text;
      }
    }
  }

  // フォールバック: body全体
  return $('body').text().replace(/\s+/g, ' ').trim();
}

/**
 * 言語・地域検出
 */
function detectLangRegion(
  $: cheerio.CheerioAPI,
  url: string
): { lang: string; region: string } {
  // HTMLのlang属性
  const htmlLang = $('html').attr('lang');

  // meta[og:locale]
  const ogLocale = $('meta[property="og:locale"]').attr('content');

  // TLDベースの推定
  const urlObj = new URL(url);
  const tld = urlObj.hostname.split('.').pop();

  let lang = '英語';
  let region = 'US';

  // 日本語判定
  if (htmlLang?.includes('ja') || ogLocale?.includes('ja') || tld === 'jp') {
    lang = '日本語';
    region = 'JP';
  }

  return { lang, region };
}
