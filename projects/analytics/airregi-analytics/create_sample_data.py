"""
サンプルデータ生成スクリプト

API仕様が判明するまでの間、システムの動作確認用にサンプルデータを生成します。
"""
import os
import json
import sys
from datetime import datetime, timedelta
import random
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.utils.logger import Logger


def generate_sample_transactions(date: datetime, num_transactions: int = 50) -> dict:
    """
    サンプル取引データ生成

    Args:
        date: 対象日付
        num_transactions: 取引件数

    Returns:
        取引データ
    """
    transactions = []

    # サンプル商品マスタ
    products = [
        {"id": "P001", "name": "ランチセットA", "price": 1200},
        {"id": "P002", "name": "ランチセットB", "price": 1500},
        {"id": "P003", "name": "カレーライス", "price": 900},
        {"id": "P004", "name": "パスタセット", "price": 1300},
        {"id": "P005", "name": "ハンバーグ定食", "price": 1100},
        {"id": "P006", "name": "コーヒー", "price": 400},
        {"id": "P007", "name": "ケーキセット", "price": 800},
        {"id": "P008", "name": "ビール", "price": 600},
        {"id": "P009", "name": "日替わり定食", "price": 950},
        {"id": "P010", "name": "デザート盛り合わせ", "price": 700},
    ]

    payment_methods = ["現金", "クレジットカード", "電子マネー", "QRコード決済"]

    for i in range(num_transactions):
        # 営業時間内のランダムな時刻生成（11:00-21:00）
        hour = random.randint(11, 20)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        transaction_time = date.replace(
            hour=hour,
            minute=minute,
            second=second
        )

        # ランダムに1-3商品を選択
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, num_items)

        items = []
        subtotal = 0

        for product in selected_products:
            quantity = random.randint(1, 2)
            item_total = product["price"] * quantity
            subtotal += item_total

            items.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "subtotal": item_total
            })

        # 税込金額計算（10%）
        tax = int(subtotal * 0.1)
        total_amount = subtotal + tax

        transaction = {
            "transaction_id": f"TXN{date.strftime('%Y%m%d')}{i+1:04d}",
            "transaction_datetime": transaction_time.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
            "amount": total_amount,
            "subtotal": subtotal,
            "tax": tax,
            "payment_method": random.choice(payment_methods),
            "items": items,
            "customer_id": None,
            "staff_id": f"S{random.randint(1, 5):03d}",
            "store_id": "STORE001"
        }

        transactions.append(transaction)

    return {
        "transactions": transactions,
        "total_count": len(transactions),
        "date": date.strftime("%Y-%m-%d")
    }


def generate_sample_settlement(date: datetime, transactions_data: dict) -> dict:
    """
    サンプル精算データ生成

    Args:
        date: 対象日付
        transactions_data: 取引データ

    Returns:
        精算データ
    """
    # 支払方法別集計
    payment_totals = {
        "現金": 0,
        "クレジットカード": 0,
        "電子マネー": 0,
        "QRコード決済": 0
    }

    for transaction in transactions_data["transactions"]:
        method = transaction["payment_method"]
        amount = transaction["amount"]
        payment_totals[method] += amount

    total_sales = sum(payment_totals.values())
    opening_cash = 50000  # 始業時現金
    closing_cash = opening_cash + payment_totals["現金"]

    settlement = {
        "settlement_id": f"SET{date.strftime('%Y%m%d')}001",
        "date": date.strftime("%Y-%m-%d"),
        "cash_sales": payment_totals["現金"],
        "card_sales": payment_totals["クレジットカード"],
        "emoney_sales": payment_totals["電子マネー"],
        "qr_sales": payment_totals["QRコード決済"],
        "total_sales": total_sales,
        "opening_cash": opening_cash,
        "closing_cash": closing_cash,
        "expected_cash": closing_cash,
        "difference": 0,
        "status": "completed"
    }

    return {"settlement": settlement}


def main():
    """メイン処理"""
    logger = Logger('SampleDataGenerator', os.getenv('LOG_DIR', './logs'))

    logger.info("=" * 60)
    logger.info("サンプルデータ生成開始")
    logger.info("=" * 60)

    # データディレクトリ確認
    raw_data_dir = os.getenv('RAW_DATA_DIR', './data/raw')
    Path(raw_data_dir).mkdir(parents=True, exist_ok=True)

    # 過去7日分のサンプルデータ生成
    today = datetime.now()

    for i in range(7):
        target_date = today - timedelta(days=i+1)
        date_str = target_date.strftime('%Y%m%d')

        logger.info(f"\n対象日: {target_date.strftime('%Y-%m-%d')}")

        # 取引データ生成
        num_transactions = random.randint(40, 80)  # 40-80件のランダム
        transactions_data = generate_sample_transactions(target_date, num_transactions)

        # 取引データ保存
        transactions_file = os.path.join(raw_data_dir, f"transactions_{date_str}.json")
        with open(transactions_file, 'w', encoding='utf-8') as f:
            json.dump(transactions_data, f, ensure_ascii=False, indent=2)

        logger.info(f"  取引データ生成: {num_transactions}件")
        logger.info(f"  保存先: {transactions_file}")

        # 精算データ生成
        settlement_data = generate_sample_settlement(target_date, transactions_data)

        # 精算データ保存
        settlement_file = os.path.join(raw_data_dir, f"settlement_{date_str}.json")
        with open(settlement_file, 'w', encoding='utf-8') as f:
            json.dump(settlement_data, f, ensure_ascii=False, indent=2)

        logger.info(f"  精算データ生成完了")
        logger.info(f"  保存先: {settlement_file}")

        # サマリー表示
        total_sales = settlement_data["settlement"]["total_sales"]
        logger.info(f"  総売上: ¥{total_sales:,}")

    logger.info("\n" + "=" * 60)
    logger.info("サンプルデータ生成完了")
    logger.info("=" * 60)
    logger.info("\n次のステップ:")
    logger.info("1. 生成されたサンプルデータを確認")
    logger.info("   ls -la data/raw/")
    logger.info("\n2. サンプルデータで分析を実行")
    logger.info("   python analyze_sample_data.py")


if __name__ == "__main__":
    main()
