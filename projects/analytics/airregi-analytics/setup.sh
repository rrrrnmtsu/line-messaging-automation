#!/bin/bash

# Airレジ売上データ分析システム - セットアップスクリプト

echo "======================================"
echo "Airレジ売上データ分析システム"
echo "セットアップ開始"
echo "======================================"

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# Python3のチェック
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません"
    exit 1
fi

echo "Python3: $(python3 --version)"

# 仮想環境作成
echo ""
echo "[1/4] 仮想環境作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 仮想環境作成完了"
else
    echo "✓ 仮想環境は既に存在します"
fi

# 仮想環境有効化
echo ""
echo "[2/4] 仮想環境有効化..."
source venv/bin/activate
echo "✓ 仮想環境有効化完了"

# 依存パッケージインストール
echo ""
echo "[3/4] 依存パッケージインストール中..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ 依存パッケージインストール完了"

# 環境変数確認
echo ""
echo "[4/4] 環境変数確認..."
if [ -f "config/.env" ]; then
    echo "✓ config/.env が存在します"

    # APIキーの確認（先頭10文字のみ表示）
    API_KEY=$(grep "AIRREGI_API_KEY=" config/.env | cut -d'=' -f2 | cut -c1-10)
    if [ -n "$API_KEY" ]; then
        echo "  APIキー: ${API_KEY}..."
    else
        echo "  警告: APIキーが設定されていません"
    fi
else
    echo "警告: config/.env が見つかりません"
    echo "config/.env.example をコピーして設定してください"
fi

echo ""
echo "======================================"
echo "セットアップ完了"
echo "======================================"
echo ""
echo "次のステップ:"
echo "1. API接続テスト:"
echo "   python test_api.py"
echo ""
echo "2. 日次分析実行:"
echo "   python main.py"
echo ""
echo "詳細は USAGE.md を参照してください"
echo ""
