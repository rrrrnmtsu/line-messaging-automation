#!/usr/bin/env python3
"""
FC2動画スクレイピングツール

指定ワードでFC2サイト内を検索し、動画URLとサムネイル画像をCSVに出力
"""

import os
import csv
import time
from datetime import datetime
from urllib.parse import urljoin, quote
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


class FC2VideoScraper:
    """FC2動画スクレイピングクラス"""

    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        初期化

        Args:
            headless: ヘッドレスモードで実行するか
            timeout: ページ読み込みタイムアウト（秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None

    def setup_driver(self):
        """Seleniumドライバーのセットアップ"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('accept-language=ja-JP,ja;q=0.9')
        chrome_options.add_argument('--disable-extensions')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)

    def close_driver(self):
        """ドライバーを閉じる"""
        if self.driver:
            self.driver.quit()

    def search_videos(self, keyword: str, max_pages: int = 1) -> List[Dict[str, str]]:
        """
        FC2で動画を検索

        Args:
            keyword: 検索キーワード
            max_pages: 取得する最大ページ数

        Returns:
            動画情報のリスト [{url, thumbnail, title}, ...]
        """
        if not self.driver:
            self.setup_driver()

        videos = []
        base_url = "https://video.fc2.com"

        for page in range(1, max_pages + 1):
            print(f"ページ {page}/{max_pages} を処理中...")

            # 検索URLを構築（FC2のアダルト検索エンドポイント）
            search_url = f"{base_url}/a/search/videos/?keyword={quote(keyword)}&page={page}"

            try:
                self.driver.get(search_url)
                time.sleep(3)  # ページ読み込み待機

                # ページソースをデバッグ出力（初回のみ）
                if page == 1:
                    print("ページ構造を確認中...")
                    # 可能な複数のセレクタパターンを試す

                # 動画要素を取得（複数のセレクタパターンを試行）
                selectors = [
                    'article.items_article_link',
                    'div.items_video',
                    'li.items_video',
                    'a[href*="/a/content/"]',
                    'div[class*="video"]',
                    'li[class*="item"]'
                ]

                video_items = []
                for selector in selectors:
                    video_items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if video_items:
                        print(f"セレクタ '{selector}' で {len(video_items)} 件の要素を発見")
                        break

                if not video_items:
                    # スクリーンショットを保存してデバッグ
                    screenshot_path = f"debug_page_{page}.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"ページ {page} に動画が見つかりませんでした（スクリーンショット: {screenshot_path}）")
                    print(f"ページタイトル: {self.driver.title}")
                    break

                for item in video_items:
                    try:
                        video_data = self._extract_video_data(item)
                        if video_data:
                            videos.append(video_data)
                    except Exception as e:
                        print(f"動画データ抽出エラー: {e}")
                        continue

                print(f"ページ {page} から {len(video_items)} 件取得")
                time.sleep(2)  # リクエスト間隔

            except Exception as e:
                print(f"ページ {page} の取得エラー: {e}")
                import traceback
                traceback.print_exc()
                break

        return videos

    def _extract_video_data(self, element) -> Optional[Dict[str, str]]:
        """
        動画要素からデータを抽出

        Args:
            element: Selenium WebElement

        Returns:
            動画データ辞書 or None
        """
        try:
            # タイトルとURLを取得
            link_elem = element.find_element(By.CSS_SELECTOR, 'a')
            video_url = link_elem.get_attribute('href')
            title = link_elem.get_attribute('title') or link_elem.text

            # サムネイル画像を取得
            try:
                img_elem = element.find_element(By.CSS_SELECTOR, 'img')
                thumbnail = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
            except:
                thumbnail = ""

            if video_url:
                return {
                    'url': video_url,
                    'thumbnail': thumbnail,
                    'title': title.strip()
                }
        except Exception as e:
            print(f"要素解析エラー: {e}")

        return None

    def save_to_csv(self, videos: List[Dict[str, str]], output_path: str):
        """
        動画データをCSVに保存

        Args:
            videos: 動画データリスト
            output_path: 出力ファイルパス
        """
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['No', 'Title', 'URL', 'Thumbnail', 'Scraped_At']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for idx, video in enumerate(videos, 1):
                writer.writerow({
                    'No': idx,
                    'Title': video.get('title', ''),
                    'URL': video.get('url', ''),
                    'Thumbnail': video.get('thumbnail', ''),
                    'Scraped_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

        print(f"\n{len(videos)} 件のデータを {output_path} に保存しました")


def main():
    """メイン処理"""
    load_dotenv()

    # 環境変数から設定を取得
    keyword = os.getenv('SEARCH_KEYWORD', 'サンプル')
    max_pages = int(os.getenv('MAX_PAGES', '1'))
    output_dir = os.getenv('OUTPUT_DIR', 'output')
    headless = os.getenv('HEADLESS', 'True').lower() == 'true'
    timeout = int(os.getenv('BROWSER_TIMEOUT', '30'))

    print(f"=== FC2動画スクレイピング開始 ===")
    print(f"検索ワード: {keyword}")
    print(f"取得ページ数: {max_pages}")
    print(f"ヘッドレスモード: {headless}\n")

    scraper = FC2VideoScraper(headless=headless, timeout=timeout)

    try:
        # 動画を検索
        videos = scraper.search_videos(keyword, max_pages)

        if videos:
            # CSVに保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f'fc2_videos_{keyword}_{timestamp}.csv')
            scraper.save_to_csv(videos, output_path)
        else:
            print("動画が見つかりませんでした")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        scraper.close_driver()

    print("\n=== スクレイピング完了 ===")


if __name__ == "__main__":
    main()
