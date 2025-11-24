"""
ログ管理モジュール
"""
import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """ロガークラス"""

    def __init__(self, name: str, log_dir: str = "./logs", level: str = "INFO"):
        """
        初期化

        Args:
            name: ロガー名
            log_dir: ログディレクトリ
            level: ログレベル
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))

        # ログディレクトリ作成
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        # ファイルハンドラー
        log_file = os.path.join(
            log_dir,
            f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level))

        # コンソールハンドラー
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))

        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # ハンドラー追加
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        """DEBUGログ"""
        self.logger.debug(message)

    def info(self, message: str):
        """INFOログ"""
        self.logger.info(message)

    def warning(self, message: str):
        """WARNINGログ"""
        self.logger.warning(message)

    def error(self, message: str):
        """ERRORログ"""
        self.logger.error(message)

    def critical(self, message: str):
        """CRITICALログ"""
        self.logger.critical(message)
