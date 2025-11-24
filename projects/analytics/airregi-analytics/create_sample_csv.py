"""
サンプルCSVデータ生成スクリプト

Airレジから出力されると想定されるCSV形式のサンプルデータを生成します。
"""
import os
import csv
from datetime import datetime, timedelta
import random
from pathlib import Path


def create_sample_transactions_csv():
    """取引データのサンプルCSV生成"""

    output_dir = Path("data/import")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_file = output_dir / "sample_transactions.csv"

    # サンプル商品
    products = [
        {"name": "ランチセットA", "price": 1200},
        {"name": "ランチセットB", "price": 1500},
        {"name": "カレーライス", "price": 900},
        {"name": "パスタセット", "price": 1300},
        {"name": "ハンバーグ定食", "price": 1100},
        {"name": "コーヒー", "price": 400},
        {"name": "ケーキセット", "price": 800},
        {"name": "ビール", "price": 600},
        {"name": "日替わり定食", "price": 950},
        {"name": "デザート盛り合わせ", "price": 700},
    ]

    payment_methods = ["現金", "クレジットカード", "電子マネー", "QRコード決済"]
    staff_names = ["田中", "佐藤", "鈴木", "高橋", "渡辺"]

    # CSVヘッダー
    headers = [
        "日付", "時刻", "伝票番号", "商品名", "数量",
        "単価", "金額", "支払方法", "スタッフ"
    ]

    # データ生成
    rows = []
    today = datetime.now()

    for i in range(50):  # 50件の取引
        # ランダムな時刻（11:00-21:00）
        hour = random.randint(11, 20)
        minute = random.randint(0, 59)

        tx_time = today.replace(hour=hour, minute=minute)

        # 商品選択
        product = random.choice(products)
        quantity = random.randint(1, 2)
        subtotal = product["price"] * quantity
        amount = int(subtotal * 1.1)  # 税込

        row = [
            tx_time.strftime("%Y-%m-%d"),
            tx_time.strftime("%H:%M:%S"),
            f"T{i+1:04d}",
            product["name"],
            quantity,
            product["price"],
            amount,
            random.choice(payment_methods),
            random.choice(staff_names)
        ]

        rows.append(row)

    # CSV書き込み
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ サンプルCSV作成完了: {csv_file}")
    print(f"   データ件数: {len(rows)}件")

    return str(csv_file)


def create_sample_settlement_csv():
    """精算データのサンプルCSV生成"""

    output_dir = Path("data/import")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_file = output_dir / "sample_settlement.csv"

    # CSVヘッダー
    headers = [
        "日付", "総売上", "現金", "クレジットカード",
        "電子マネー", "QRコード", "取引件数"
    ]

    # データ生成（過去7日分）
    rows = []
    today = datetime.now()

    for i in range(7):
        date = today - timedelta(days=i)
        total_sales = random.randint(150000, 250000)

        # 支払方法別内訳（ランダム）
        cash = int(total_sales * random.uniform(0.25, 0.40))
        card = int(total_sales * random.uniform(0.20, 0.30))
        emoney = int(total_sales * random.uniform(0.20, 0.30))
        qr = total_sales - (cash + card + emoney)

        transactions = random.randint(40, 80)

        row = [
            date.strftime("%Y-%m-%d"),
            total_sales,
            cash,
            card,
            emoney,
            qr,
            transactions
        ]

        rows.append(row)

    # CSV書き込み
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ 精算CSV作成完了: {csv_file}")
    print(f"   データ件数: {len(rows)}日分")

    return str(csv_file)


if __name__ == "__main__":
    print("=" * 60)
    print("Airレジサンプルデータ（CSV）生成")
    print("=" * 60)
    print()

    # 取引データCSV
    tx_file = create_sample_transactions_csv()

    # 精算データCSV
    settlement_file = create_sample_settlement_csv()

    print()
    print("=" * 60)
    print("生成完了")
    print("=" * 60)
    print()
    print("次のステップ:")
    print(f"1. CSVをインポート:")
    print(f"   python import_csv.py --file {tx_file} --analyze")
    print()
    print(f"2. 精算データをインポート:")
    print(f"   python import_csv.py --file {settlement_file} --type settlement")
