#!/usr/bin/env python3
"""
FC2動画HTMLパーサー

手動でダウンロードしたHTMLファイルから動画情報を抽出してCSVに出力
"""

import os
import csv
import sys
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup


class FC2HTMLParser:
    """FC2動画HTMLパーサー"""

    def parse_html_file(self, html_path: str) -> List[Dict[str, str]]:
        """
        HTMLファイルから動画情報を抽出

        Args:
            html_path: HTMLファイルのパス

        Returns:
            動画情報のリスト
        """
        videos = []

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'lxml')

            # 複数のセレクタパターンを試行
            selectors = [
                ('article.items_article_link', 'a', 'img'),
                ('div.items_video_hor_big', 'a', 'img'),
                ('div.items_video_hor_mini', 'a', 'img'),
                ('li.items_video', 'a', 'img'),
            ]

            for article_selector, link_selector, img_selector in selectors:
                items = soup.select(article_selector)

                if items:
                    print(f"セレクタ '{article_selector}' で {len(items)} 件発見")

                    for item in items:
                        video_data = self._extract_video_from_element(item, link_selector, img_selector)
                        if video_data:
                            videos.append(video_data)

                    if videos:
                        break

            # 汎用的なリンク抽出（フォールバック）
            if not videos:
                print("特定のセレクタで見つからなかったため、汎用抽出を試行...")
                videos = self._extract_generic_videos(soup)

        except Exception as e:
            print(f"HTMLパースエラー: {e}")
            import traceback
            traceback.print_exc()

        return videos

    def _extract_video_from_element(self, element, link_selector: str, img_selector: str) -> Dict[str, str]:
        """要素から動画データを抽出"""
        try:
            link = element.select_one(link_selector)
            if not link:
                return None

            url = link.get('href', '')
            if not url or 'fc2.com' not in url:
                return None

            # 相対URLを絶対URLに変換
            if url.startswith('/'):
                url = f"https://video.fc2.com{url}"

            # タイトル取得
            title = link.get('title', '') or link.get_text(strip=True)

            # サムネイル取得
            thumbnail = ""
            img = element.select_one(img_selector)
            if img:
                thumbnail = img.get('src') or img.get('data-src') or img.get('data-lazy-src') or ""

            return {
                'url': url,
                'thumbnail': thumbnail,
                'title': title or 'タイトルなし'
            }

        except Exception as e:
            return None

    def _extract_generic_videos(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """汎用的な動画リンク抽出"""
        videos = []

        # FC2動画へのリンクをすべて抽出
        links = soup.find_all('a', href=lambda x: x and '/a/content/' in x)

        for link in links:
            url = link.get('href', '')
            if url.startswith('/'):
                url = f"https://video.fc2.com{url}"

            title = link.get('title', '') or link.get_text(strip=True)

            # 親要素からサムネイルを探す
            thumbnail = ""
            parent = link.find_parent()
            if parent:
                img = parent.find('img')
                if img:
                    thumbnail = img.get('src') or img.get('data-src') or ""

            videos.append({
                'url': url,
                'thumbnail': thumbnail,
                'title': title or 'タイトルなし'
            })

        # 重複削除
        unique_videos = []
        seen_urls = set()
        for video in videos:
            if video['url'] not in seen_urls:
                seen_urls.add(video['url'])
                unique_videos.append(video)

        return unique_videos

    def save_to_csv(self, videos: List[Dict[str, str]], output_path: str):
        """動画データをCSVに保存"""
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['No', 'Title', 'URL', 'Thumbnail', 'Parsed_At']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for idx, video in enumerate(videos, 1):
                writer.writerow({
                    'No': idx,
                    'Title': video.get('title', ''),
                    'URL': video.get('url', ''),
                    'Thumbnail': video.get('thumbnail', ''),
                    'Parsed_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

        print(f"\n{len(videos)} 件のデータを {output_path} に保存しました")


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python {sys.argv[0]} <HTMLファイルパス> [出力CSVパス]")
        print("\n例:")
        print(f"  python {sys.argv[0]} fc2_search_result.html")
        print(f"  python {sys.argv[0]} fc2_search_result.html output/result.csv")
        sys.exit(1)

    html_path = sys.argv[1]

    if not os.path.exists(html_path):
        print(f"エラー: ファイルが見つかりません: {html_path}")
        sys.exit(1)

    # 出力パスの決定
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"output/fc2_videos_{timestamp}.csv"

    print(f"=== FC2動画HTMLパース開始 ===")
    print(f"入力ファイル: {html_path}")
    print(f"出力ファイル: {output_path}\n")

    parser = FC2HTMLParser()

    # HTMLをパース
    videos = parser.parse_html_file(html_path)

    if videos:
        # CSVに保存
        parser.save_to_csv(videos, output_path)
        print(f"\n取得した動画数: {len(videos)}")
    else:
        print("動画が見つかりませんでした")
        print("\nヒント:")
        print("- HTMLファイルが正しく保存されているか確認してください")
        print("- ブラウザで「完全に保存」オプションを使用してください")

    print("\n=== パース完了 ===")


if __name__ == "__main__":
    main()
