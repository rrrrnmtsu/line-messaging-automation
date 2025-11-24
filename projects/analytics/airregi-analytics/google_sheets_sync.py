#!/usr/bin/env python3
"""
Google Sheets¹¯ê×È

Airì¸Çü¿’Google Sheetsk¨¯¹İüÈW~Y

(‹:
    # µŞêüìİüÈ’¨¯¹İüÈ
    python google_sheets_sync.py --summary data/processed/summary_report_20251014.json

    # ÖÇü¿’¨¯¹İüÈ
    python google_sheets_sync.py --transactions data/raw/imported_transactions_20251014.json

    # ¹×ìÃÉ·üÈ’š
    python google_sheets_sync.py --summary data/processed/summary_report_20251014.json --title "—A_10"

    # q	-š
    python google_sheets_sync.py --summary data/processed/summary_report_20251014.json --share example@gmail.com
"""
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from src.integrations.google_sheets import (
    export_summary_to_sheets,
    export_transactions_to_sheets,
    GoogleSheetsClient
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """á¤óæ"""
    parser = argparse.ArgumentParser(
        description='Airì¸Çü¿’Google Sheetsk¨¯¹İüÈ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Çü¿½ü¹ia‰KÅ	
    parser.add_argument(
        '--summary',
        type=str,
        help='µŞêüìİüÈJSONÕ¡¤ënÑ¹'
    )
    parser.add_argument(
        '--transactions',
        type=str,
        help='ÖÇü¿JSONÕ¡¤ënÑ¹'
    )

    # ª×·çó
    parser.add_argument(
        '--title',
        type=str,
        help='¹×ìÃÉ·üÈšWjD4oêÕ	'
    )
    parser.add_argument(
        '--credentials',
        type=str,
        default='config/google_credentials.json',
        help='Google<Å1Õ¡¤ënÑ¹ÇÕ©ëÈ: config/google_credentials.json	'
    )
    parser.add_argument(
        '--share',
        type=str,
        help='q	Hnáüë¢Éì¹pn4o«óŞ:Š	'
    )
    parser.add_argument(
        '--share-role',
        type=str,
        choices=['reader', 'writer', 'owner'],
        default='writer',
        help='q	)PÇÕ©ëÈ: writer	'
    )

    args = parser.parse_args()

    # ĞêÇü·çó
    if not args.summary and not args.transactions:
        parser.error("--summary ~_o --transactions nDZŒK’šWfO`UD")

    if args.summary and args.transactions:
        parser.error("--summary h --transactions oBkšgM~[“")

    # <Å1Õ¡¤ënº
    creds_path = Path(args.credentials)
    if not creds_path.exists():
        logger.error(f"L Google<Å1Õ¡¤ëL‹dKŠ~[“: {args.credentials}")
        logger.info("\nGoogle Sheets API -šK")
        logger.info("1. Google Cloud Console (https://console.cloud.google.com/) k¢¯»¹")
        logger.info("2. °WD×í¸§¯È’\~_oâXn×í¸§¯È’x")
        logger.info("3. APIhµüÓ¹’é¤ÖéêK‰å’	¹:")
        logger.info("   - Google Sheets API")
        logger.info("   - Google Drive API")
        logger.info("4. <Å1’<Å1’\’µüÓ¹¢«¦óÈ’x")
        logger.info("5. µüÓ¹¢«¦óÈ’\W­ü’ı ’JSON’x")
        logger.info("6. À¦óíüÉW_JSONÕ¡¤ë’åkİX:")
        logger.info(f"   {args.credentials}")
        sys.exit(1)

    try:
        # µŞêüìİüÈn¨¯¹İüÈ
        if args.summary:
            summary_path = Path(args.summary)
            if not summary_path.exists():
                logger.error(f"L Õ¡¤ëL‹dKŠ~[“: {args.summary}")
                sys.exit(1)

            logger.info(f"=Ê µŞêüìİüÈ’¨¯¹İüÈ-...")
            logger.info(f"   Õ¡¤ë: {args.summary}")

            url = export_summary_to_sheets(
                summary_file=str(summary_path),
                spreadsheet_title=args.title,
                credentials_path=args.credentials
            )

            logger.info(f" ¨¯¹İüÈŒ†!")
            logger.info(f"   ¹×ìÃÉ·üÈURL: {url}")

        # ÖÇü¿n¨¯¹İüÈ
        elif args.transactions:
            tx_path = Path(args.transactions)
            if not tx_path.exists():
                logger.error(f"L Õ¡¤ëL‹dKŠ~[“: {args.transactions}")
                sys.exit(1)

            logger.info(f"=Ê ÖÇü¿’¨¯¹İüÈ-...")
            logger.info(f"   Õ¡¤ë: {args.transactions}")

            url = export_transactions_to_sheets(
                transactions_file=str(tx_path),
                spreadsheet_title=args.title,
                credentials_path=args.credentials
            )

            logger.info(f" ¨¯¹İüÈŒ†!")
            logger.info(f"   ¹×ìÃÉ·üÈURL: {url}")

        # q	-š
        if args.share:
            title = args.title
            if not title:
                # ¿¤ÈëLšUŒfDjD4êÕUŒ_¿¤Èë’¨,
                if args.summary:
                    import json
                    with open(args.summary, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        target_date = data.get('şaå', datetime.now().strftime('%Y-%m-%d'))
                        title = f"Airì¸ò
_{target_date}"
                elif args.transactions:
                    title = f"Airì¸ÖÇü¿_{datetime.now().strftime('%Y%m%d')}"

            emails = [email.strip() for email in args.share.split(',')]
            client = GoogleSheetsClient(args.credentials)

            logger.info(f"\n=ä ¹×ìÃÉ·üÈ’q	-...")
            for email in emails:
                client.share_spreadsheet(title, email, args.share_role)
                logger.info(f"   q	Œ†: {email} ({args.share_role})")

        logger.info("\n<‰ YyfnæLŒ†W~W_!")

    except FileNotFoundError as e:
        logger.error(f"L Õ¡¤ë¨éü: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"L ¨éüLzW~W_: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
