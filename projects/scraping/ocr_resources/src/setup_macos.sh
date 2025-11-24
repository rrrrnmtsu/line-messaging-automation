#!/bin/bash
################################################################################
# macOS ARM64 (M1/M2) 用 OCR環境セットアップスクリプト
# 用途: PaddleOCR, EasyOCR, Tesseractの実装環境構築
################################################################################

set -e

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✅ SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠️ WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[❌ ERROR]${NC} $1"
}

# ================================
# 1. システムチェック
# ================================

log_info "=========================================="
log_info "macOS OCR環境セットアップ"
log_info "=========================================="

# macOS バージョン確認
log_info "macOS バージョン確認中..."
if ! sw_vers | grep -q "macOS"; then
    log_error "このスクリプトはmacOSでのみ実行できます"
    exit 1
fi
log_success "macOS 環境確認完了"

# ARM64 確認
log_info "ARM64アーキテクチャ確認中..."
if [[ $(uname -m) != "arm64" ]]; then
    log_warning "このマシンはARM64ではありません ($(uname -m))"
    log_warning "Intel Macの場合はインストールが異なる可能性があります"
fi
log_success "アーキテクチャ: $(uname -m)"

# ================================
# 2. Homebrewの確認
# ================================

log_info "Homebrewの確認中..."
if ! command -v brew &> /dev/null; then
    log_warning "Homebrewがインストールされていません"
    log_info "Homebrewをインストール中..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
log_success "Homebrew 確認完了: $(brew --version | head -1)"

# ================================
# 3. Python 3.9.6 の確認・インストール
# ================================

log_info "Python 3.9.6 の確認中..."

# pyenv のインストール確認
if ! command -v pyenv &> /dev/null; then
    log_warning "pyenv がインストールされていません"
    log_info "pyenv をインストール中..."
    brew install pyenv
    log_info "pyenv をシェル設定に追加中..."
    {
        echo 'export PATH="$HOME/.pyenv/bin:$PATH"'
        echo 'eval "$(pyenv init --path)"'
        echo 'eval "$(pyenv init -)"'
    } >> ~/.zshrc
    source ~/.zshrc
fi

# Python 3.9.6 のインストール
if ! pyenv versions | grep -q "3.9.6"; then
    log_info "Python 3.9.6 をインストール中... (数分かかります)"
    pyenv install 3.9.6
else
    log_success "Python 3.9.6 はインストール済みです"
fi

# ================================
# 4. 仮想環境の作成
# ================================

VENV_NAME="ocr_env"
VENV_PATH="$HOME/$VENV_NAME"

log_info "仮想環境を作成中: $VENV_PATH"

if [ -d "$VENV_PATH" ]; then
    log_warning "仮想環境が既に存在します: $VENV_PATH"
    read -p "既存の仮想環境を削除して新しく作成しますか? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_PATH"
    else
        log_info "既存の仮想環境を使用します"
    fi
fi

if [ ! -d "$VENV_PATH" ]; then
    # Python 3.9.6 で仮想環境を作成
    ~/.pyenv/versions/3.9.6/bin/python3.9 -m venv "$VENV_PATH"
    log_success "仮想環境を作成しました: $VENV_PATH"
fi

# 仮想環境を有効化
source "$VENV_PATH/bin/activate"
log_success "仮想環境を有効化しました"

# ================================
# 5. Python パッケージのインストール
# ================================

log_info "Python パッケージをアップグレード中..."
pip install --upgrade pip setuptools wheel

# ================================
# 6. Option A: PaddleOCR のインストール
# ================================

log_info ""
log_info "=========================================="
log_info "Option A: PaddleOCR のインストール"
log_info "=========================================="

read -p "PaddleOCR をインストールしますか? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "PaddleOCR をインストール中... (数分かかります)"
    pip install paddlepaddle==2.5.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
    pip install paddleocr

    log_info "PaddleOCR をテスト中..."
    python3 << 'EOF'
try:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    print("✅ PaddleOCR インストール成功")
except Exception as e:
    print(f"❌ PaddleOCR インストール失敗: {e}")
    exit(1)
EOF
    log_success "PaddleOCR のインストール完了"
else
    log_warning "PaddleOCR のインストールをスキップしました"
fi

# ================================
# 7. Option B: EasyOCR のインストール
# ================================

log_info ""
log_info "=========================================="
log_info "Option B: EasyOCR のインストール"
log_info "=========================================="

read -p "EasyOCR をインストールしますか? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "EasyOCR をインストール中..."
    pip install easyocr opencv-python

    log_info "EasyOCR をテスト中..."
    python3 << 'EOF'
try:
    import easyocr
    reader = easyocr.Reader(['ja'])
    print("✅ EasyOCR インストール成功")
except Exception as e:
    print(f"❌ EasyOCR インストール失敗: {e}")
    exit(1)
EOF
    log_success "EasyOCR のインストール完了"
else
    log_warning "EasyOCR のインストールをスキップしました"
fi

# ================================
# 8. Tesseract OCR のインストール
# ================================

log_info ""
log_info "=========================================="
log_info "Option C: Tesseract OCR のインストール"
log_info "=========================================="

read -p "Tesseract OCR をインストールしますか? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Tesseract OCR をインストール中..."
    brew install tesseract tesseract-lang

    log_info "Tesseract をテスト中..."
    python3 << 'EOF'
try:
    import pytesseract
    pytesseract.get_tesseract_version()
    print("✅ Tesseract インストール成功")
except Exception as e:
    print(f"❌ Tesseract インストール失敗: {e}")
    exit(1)
EOF
    pip install pytesseract

    log_success "Tesseract OCR のインストール完了"
else
    log_warning "Tesseract OCR のインストールをスキップしました"
fi

# ================================
# 9. 追加ユーティリティ
# ================================

log_info ""
log_info "=========================================="
log_info "追加ユーティリティのインストール"
log_info "=========================================="

log_info "NumPy, Pillow, その他のユーティリティをインストール中..."
pip install numpy pillow matplotlib scipy

log_success "追加ユーティリティのインストール完了"

# ================================
# 10. セットアップサマリー
# ================================

log_info ""
log_info "=========================================="
log_info "セットアップ完了"
log_info "=========================================="

log_success "環境セットアップが完了しました"

echo ""
echo "【次のステップ】"
echo ""
echo "1. 仮想環境の有効化:"
echo "   source $VENV_PATH/bin/activate"
echo ""
echo "2. Python ファイル位置:"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/implementation_examples.py" ]; then
    echo "   $SCRIPT_DIR/implementation_examples.py"
fi
echo ""
echo "3. テスト実行:"
echo "   python3 implementation_examples.py"
echo ""
echo "4. 仮想環境の無効化:"
echo "   deactivate"
echo ""

# シェル設定ファイルに仮想環境パスを追加
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "OCR_VENV" "$HOME/.zshrc"; then
        echo "" >> "$HOME/.zshrc"
        echo "# OCR環境変数" >> "$HOME/.zshrc"
        echo "export OCR_VENV='$VENV_PATH'" >> "$HOME/.zshrc"
        echo "alias activate_ocr='source \$OCR_VENV/bin/activate'" >> "$HOME/.zshrc"
        log_success "シェル設定に追加しました (activate_ocr コマンド)"
    fi
fi

log_success "すべてのセットアップが完了しました"
