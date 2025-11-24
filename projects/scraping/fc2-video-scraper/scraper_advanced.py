#!/usr/bin/env python3
"""
FC2動画スクレイピングツール（高度版）

ボット対策を回避するための高度な手法を実装
"""

import os
import csv
import time
import random
from datetime import datetime
from urllib.parse import quote
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


class FC2VideoScraperAdvanced:
    """FC2動画スクレイピングクラス（ボット対策回避版）"""

    def __init__(self, headless: bool = False, timeout: int = 30):
        """
        初期化

        Args:
            headless: ヘッドレスモードで実行するか（False推奨）
            timeout: ページ読み込みタイムアウト（秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Seleniumドライバーのセットアップ（ボット検出回避）"""
        chrome_options = Options()

        # ボット検出回避のための設定
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        if self.headless:
            chrome_options.add_argument('--headless=new')

        # 基本設定
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')

        # より本物らしいUser-Agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('accept-language=ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7')

        # その他の設定
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--profile-directory=Default')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # WebDriverの検出を回避するJavaScriptを実行
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });

                Object.defineProperty(navigator, 'languages', {
                    get: () => ['ja-JP', 'ja', 'en-US', 'en']
                });

                window.chrome = {
                    runtime: {}
                };
            '''
        })

        self.driver.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.driver, 20)

    def human_like_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """人間らしいランダムな遅延"""
        time.sleep(random.uniform(min_sec, max_sec))

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

        try:
            # まずトップページにアクセスして人間らしい動作を模倣
            print("FC2動画サイトにアクセス中...")
            self.driver.get("https://video.fc2.com/")
            self.human_like_delay(2, 4)

            # アダルトセクションに移動
            print("アダルトセクションに移動中...")
            self.driver.get("https://video.fc2.com/a/")
            self.human_like_delay(2, 4)

            # 検索ボックスを探して入力
            print(f"キーワード '{keyword}' で検索中...")
            try:
                # 検索ボックスのセレクタ候補
                search_selectors = [
                    'input[name="keyword"]',
                    'input[type="search"]',
                    'input[placeholder*="検索"]',
                    '#search_keyword',
                    '.search_input'
                ]

                search_box = None
                for selector in search_selectors:
                    try:
                        search_box = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if search_box:
                            print(f"検索ボックス発見: {selector}")
                            break
                    except:
                        continue

                if not search_box:
                    print("検索ボックスが見つかりませんでした。直接URLでアクセスします。")
                    # 直接検索URLにアクセス
                    search_url = f"https://video.fc2.com/a/search/videos/?keyword={quote(keyword)}"
                    self.driver.get(search_url)
                else:
                    # 人間らしくタイピング
                    search_box.click()
                    self.human_like_delay(0.5, 1)
                    for char in keyword:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.3))

                    self.human_like_delay(0.5, 1)
                    search_box.send_keys(Keys.RETURN)

                self.human_like_delay(3, 5)

            except Exception as e:
                print(f"検索エラー: {e}")
                # フォールバック: 直接URLアクセス
                search_url = f"https://video.fc2.com/a/search/videos/?keyword={quote(keyword)}"
                self.driver.get(search_url)
                self.human_like_delay(3, 5)

            # 各ページの動画を取得
            for page in range(1, max_pages + 1):
                print(f"\nページ {page}/{max_pages} を処理中...")

                if page > 1:
                    # ページネーションをクリック
                    try:
                        next_page_url = f"https://video.fc2.com/a/search/videos/?keyword={quote(keyword)}&page={page}"
                        self.driver.get(next_page_url)
                        self.human_like_delay(3, 5)
                    except Exception as e:
                        print(f"ページ {page} への移動エラー: {e}")
                        break

                # ページのスクリーンショットを保存
                screenshot_path = f"page_{page}_screenshot.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"スクリーンショット保存: {screenshot_path}")

                # スクロールして全コンテンツを読み込み
                self._scroll_page()

                # 動画要素を取得
                page_videos = self._extract_videos_from_page()

                if not page_videos:
                    print(f"ページ {page} に動画が見つかりませんでした")
                    print(f"現在のURL: {self.driver.current_url}")
                    print(f"ページタイトル: {self.driver.title}")
                    break

                videos.extend(page_videos)
                print(f"ページ {page} から {len(page_videos)} 件取得（合計: {len(videos)} 件）")

                self.human_like_delay(2, 4)

        except Exception as e:
            print(f"検索処理エラー: {e}")
            import traceback
            traceback.print_exc()

        return videos

    def _scroll_page(self):
        """ページを人間らしくスクロール"""
        try:
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")

            current_position = 0
            scroll_step = viewport_height // 2

            while current_position < total_height:
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.3, 0.7))

                # 新しいコンテンツが読み込まれた場合に対応
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height > total_height:
                    total_height = new_height

            # トップに戻る
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

        except Exception as e:
            print(f"スクロールエラー: {e}")

    def _extract_videos_from_page(self) -> List[Dict[str, str]]:
        """現在のページから動画情報を抽出"""
        videos = []

        # 複数のセレクタパターンを試行
        selectors = [
            'article.items_article_link',
            'div.items_video_hor_big',
            'div.items_video_hor_mini',
            'li.items_video',
            'a[href*="/a/content/"]',
            'div[class*="video-item"]',
            'div[class*="videoItem"]'
        ]

        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"セレクタ '{selector}' で {len(elements)} 件発見")

                    for element in elements:
                        try:
                            video_data = self._extract_video_data(element)
                            if video_data and video_data not in videos:
                                videos.append(video_data)
                        except Exception as e:
                            continue

                    if videos:
                        break

            except Exception as e:
                continue

        return videos

    def _extract_video_data(self, element) -> Optional[Dict[str, str]]:
        """動画要素からデータを抽出"""
        try:
            # リンク要素を探す
            link_elem = None
            try:
                link_elem = element if element.tag_name == 'a' else element.find_element(By.CSS_SELECTOR, 'a')
            except:
                return None

            video_url = link_elem.get_attribute('href')
            if not video_url or 'fc2.com' not in video_url:
                return None

            # タイトルを取得
            title = ""
            try:
                title = link_elem.get_attribute('title') or link_elem.text.strip()
                if not title:
                    title_elem = element.find_element(By.CSS_SELECTOR, 'h3, h4, .title, [class*="title"]')
                    title = title_elem.text.strip()
            except:
                pass

            # サムネイル画像を取得
            thumbnail = ""
            try:
                img_elem = element.find_element(By.CSS_SELECTOR, 'img')
                thumbnail = img_elem.get_attribute('src') or img_elem.get_attribute('data-src') or img_elem.get_attribute('data-lazy-src')
            except:
                pass

            if video_url:
                return {
                    'url': video_url,
                    'thumbnail': thumbnail,
                    'title': title or 'タイトルなし'
                }

        except Exception as e:
            pass

        return None

    def save_to_csv(self, videos: List[Dict[str, str]], output_path: str):
        """動画データをCSVに保存"""
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
    headless = os.getenv('HEADLESS', 'False').lower() == 'true'
    timeout = int(os.getenv('BROWSER_TIMEOUT', '30'))

    print(f"=== FC2動画スクレイピング開始（高度版） ===")
    print(f"検索ワード: {keyword}")
    print(f"取得ページ数: {max_pages}")
    print(f"ヘッドレスモード: {headless}")
    print(f"注意: ボット検出回避のため、処理に時間がかかります\n")

    scraper = FC2VideoScraperAdvanced(headless=headless, timeout=timeout)

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
            print("\n対処法:")
            print("1. ヘッドレスモードを無効にして実行 (HEADLESS=False)")
            print("2. 手動でブラウザを確認し、CAPTCHA等がないか確認")
            print("3. FC2のサイト構造が変更されている可能性")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nブラウザを閉じています...")
        scraper.close_driver()

    print("\n=== スクレイピング完了 ===")


if __name__ == "__main__":
    main()
