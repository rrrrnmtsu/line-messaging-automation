#!/opt/homebrew/bin/python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import json
import time
from datetime import datetime

class KindleAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindle Automation Tool")
        self.root.geometry("600x700")
        
        # 強制ライトモード設定
        bg_color = "#ffffff"
        fg_color = "#000000"
        
        self.root.configure(bg=bg_color)
        self.root.option_add('*background', bg_color)
        self.root.option_add('*foreground', fg_color)
        self.root.option_add('*Entry.background', '#ffffff')
        self.root.option_add('*Text.background', '#ffffff')
        self.root.option_add('*Button.highlightBackground', bg_color)
        
        # Ttkスタイル設定
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
            
        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", background="#e0e0e0", foreground=fg_color)
        
        # 設定ファイルパス
        self.config_file = os.path.expanduser("~/.kindle_automation_config.json")
        self.load_config()
        
        self.create_widgets()
        self.is_running = False
        self.stop_event = threading.Event()

    def load_config(self):
        self.config = {
            "working_folder": os.path.expanduser("~/Desktop/KindleBook"),
            "wait_time": "3",
            "max_pages": "50",
            "direction": "left", # left or right
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass

    def save_config(self):
        self.config["working_folder"] = self.working_folder_var.get()
        self.config["wait_time"] = self.wait_time_var.get()
        self.config["max_pages"] = self.max_pages_var.get()
        self.config["direction"] = self.direction_var.get()
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
        except:
            pass

    def create_widgets(self):
        # メインフレーム (tk.Frameを使用)
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- 設定セクション ---
        settings_frame = ttk.LabelFrame(main_frame, text="基本設定", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # 作業フォルダ
        ttk.Label(settings_frame, text="作業フォルダ:").grid(row=0, column=0, sticky=tk.W)
        self.working_folder_var = tk.StringVar(value=self.config["working_folder"])
        
        folder_frame = tk.Frame(settings_frame, bg="#ffffff")
        folder_frame.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Entry(folder_frame, textvariable=self.working_folder_var, width=30).pack(side=tk.LEFT)
        ttk.Button(folder_frame, text="参照...", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        
        # 待機時間
        ttk.Label(settings_frame, text="ページめくり待機(秒):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wait_time_var = tk.StringVar(value=self.config["wait_time"])
        ttk.Entry(settings_frame, textvariable=self.wait_time_var, width=10).grid(row=1, column=1, padx=5, sticky=tk.W)
        
        # 最大ページ数
        ttk.Label(settings_frame, text="最大ページ数 (安全停止):").grid(row=2, column=0, sticky=tk.W)
        self.max_pages_var = tk.StringVar(value=self.config["max_pages"])
        ttk.Entry(settings_frame, textvariable=self.max_pages_var, width=10).grid(row=2, column=1, padx=5, sticky=tk.W)

        # ページめくり方向
        ttk.Label(settings_frame, text="めくり方向:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.direction_var = tk.StringVar(value=self.config.get("direction", "left"))
        
        dir_frame = tk.Frame(settings_frame, bg="#ffffff")
        dir_frame.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # スタイル調整 (ラジオボタンの背景白)
        style = ttk.Style()
        style.configure("TRadiobutton", background="#ffffff", foreground="#000000")
        
        ttk.Radiobutton(dir_frame, text="左へ (← 縦書き)", variable=self.direction_var, value="left").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(dir_frame, text="右へ (→ 横書き)", variable=self.direction_var, value="right").pack(side=tk.LEFT, padx=5)
        
        # --- 操作セクション ---
        action_frame = ttk.LabelFrame(main_frame, text="実行アクション", padding="10")
        action_frame.pack(fill=tk.X, pady=5)
        
        self.btn_capture = ttk.Button(action_frame, text="📸 撮影開始 (新規/追記)", command=self.start_capture)
        self.btn_capture.pack(fill=tk.X, pady=2)
        
        self.btn_ocr = ttk.Button(action_frame, text="📝 OCR実行 (テキスト抽出)", command=self.start_ocr)
        self.btn_ocr.pack(fill=tk.X, pady=2)
        
        self.btn_pdf = ttk.Button(action_frame, text="📄 PDF作成 (画像+透明テキスト)", command=self.start_pdf)
        self.btn_pdf.pack(fill=tk.X, pady=2)
        
        self.btn_full = ttk.Button(action_frame, text="🚀 全自動実行 (撮影〜PDF作成)", command=self.start_full_auto)
        self.btn_full.pack(fill=tk.X, pady=5)
        
        self.btn_stop = ttk.Button(action_frame, text="🛑 処理停止", command=self.stop_process, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X, pady=5)
        
        # --- ログセクション ---
        log_frame = ttk.LabelFrame(main_frame, text="実行ログ", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, height=15, state=tk.DISABLED, bg="#ffffff", fg="#000000")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = scrollbar.set

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=os.path.expanduser("~/Desktop"))
        if folder:
            self.working_folder_var.set(folder)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def toggle_buttons(self, running):
        state = tk.DISABLED if running else tk.NORMAL
        stop_state = tk.NORMAL if running else tk.DISABLED
        
        self.btn_capture.config(state=state)
        self.btn_ocr.config(state=state)
        self.btn_pdf.config(state=state)
        self.btn_full.config(state=state)
        self.btn_stop.config(state=stop_state)
        
        self.is_running = running

    def stop_process(self):
        if self.is_running:
            self.log("停止要求を受け付けました...")
            self.stop_event.set()

    def start_capture(self):
        self.save_config()
        self.stop_event.clear()
        self.toggle_buttons(True)
        threading.Thread(target=self.run_capture, daemon=True).start()

    def run_capture(self):
        try:
            self.log("撮影処理を開始します...")
            project_folder = self.working_folder_var.get()
            wait_time = int(self.wait_time_var.get())
            max_pages = int(self.max_pages_var.get())
            
            if not project_folder:
                self.log("エラー: 作業フォルダを指定してください")
                return

            if not os.path.exists(project_folder):
                try:
                    os.makedirs(project_folder)
                    self.log(f"フォルダ作成: {project_folder}")
                except Exception as e:
                    self.log(f"フォルダ作成エラー: {e}")
                    return
            
            # Kindleアクティブ化
            if not self.activate_kindle():
                return

            page_count = 1
            # 既存ファイルの続きから開始する場合のカウント調整
            existing_files = [f for f in os.listdir(project_folder) if f.startswith("page_") and f.endswith(".png")]
            if existing_files:
                page_count = len(existing_files) + 1
                self.log(f"既存ファイル検知: {page_count}ページ目から開始します")

            previous_hash = ""
            same_count = 0
            
            while not self.stop_event.is_set():
                if page_count > max_pages:
                    self.log("最大ページ数に到達しました")
                    break
                
                filename = f"page_{page_count:03d}.png"
                filepath = os.path.join(project_folder, filename)
                
                # 撮影
                if self.capture_screen(filepath):
                    self.log(f"撮影: {filename}")
                else:
                    self.log(f"撮影失敗: {filename}")
                    break
                
                # 重複チェック
                current_hash = self.get_file_hash(filepath)
                if current_hash == previous_hash:
                    same_count += 1
                    self.log(f"重複検知 ({same_count}/3): ページめくりを再試行します...")
                    os.remove(filepath) # 重複ファイル削除
                    
                    if same_count >= 3: # 3回連続重複で終了
                        self.log("書籍の終了を検知しました")
                        break
                    
                    # 再試行のためページめくりを行って待機
                    self.next_page()
                    for _ in range(wait_time):
                        if self.stop_event.is_set(): break
                        time.sleep(1)
                    continue # page_countを増やさずにループ先頭へ
                else:
                    same_count = 0
                
                previous_hash = current_hash
                
                # 次ページへ
                self.next_page()
                page_count += 1
                
                # 待機
                for _ in range(wait_time):
                    if self.stop_event.is_set(): break
                    time.sleep(1)
            
            self.log(f"撮影完了: 全{page_count-1}ページ")
            
        except Exception as e:
            self.log(f"エラー: {e}")
        finally:
            self.toggle_buttons(False)

    def activate_kindle(self):
        script = '''
        tell application "Amazon Kindle" to activate
        delay 1
        tell application "System Events"
            tell process "Kindle"
                if not (exists front window) then return "false"
                return "true"
            end tell
        end tell
        '''
        result = self.run_applescript(script)
        if result.strip() == "false":
            self.log("Kindleウィンドウが見つかりません")
            return False
        return True

    def capture_screen(self, filepath):
        # Kindleウィンドウの位置を取得して撮影
        script = f'''
        tell application "System Events"
            tell process "Kindle"
                if not (exists front window) then return "Error: No Window"
                set frontWindow to front window
                set {{wX, wY}} to position of frontWindow
                set {{wW, wH}} to size of frontWindow
                -- 強制的に文字列として結合する (リスト化を防ぐ)
                return "" & (wX as integer) & "|" & (wY as integer) & "|" & (wW as integer) & "|" & (wH as integer)
            end tell
        end tell
        '''
        try:
            rect_str = self.run_applescript(script).strip()
            # self.log(f"Debug: Window Geometry = '{rect_str}'")
            
            if "Error" in rect_str:
                self.log(f"撮影エラー: Kindleウィンドウが見つかりません ({rect_str})")
                return False
                
            parts = rect_str.split('|')
            if len(parts) != 4:
                self.log(f"撮影エラー: ウィンドウ情報が不正です ('{rect_str}')")
                return False
                
            x, y, w, h = map(int, parts)
            
            # 調整 (枠線除去など)
            crop_x = x + 20
            crop_y = y + 80
            crop_w = w - 40
            crop_h = h - 120
            
            if crop_w <= 0 or crop_h <= 0:
                 self.log(f"撮影エラー: ウィンドウサイズが小さすぎます ({w}x{h})")
                 return False
            
            cmd = ["screencapture", "-x", "-R", f"{crop_x},{crop_y},{crop_w},{crop_h}", filepath]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            self.log(f"撮影エラー: {e}")
            return False

    def next_page(self):
        direction = self.direction_var.get()
        key_code = 123 if direction == "left" else 124
        
        script = f'''
        tell application "System Events"
            tell process "Kindle"
                key code {key_code}
            end tell
        end tell
        '''
        self.run_applescript(script)

    def run_applescript(self, script):
        p = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if p.returncode != 0:
            raise Exception(p.stderr)
        return p.stdout

    def get_file_hash(self, filepath):
        cmd = ["md5", "-q", filepath]
        return subprocess.check_output(cmd).decode().strip()


    def start_ocr(self):
        self.save_config()
        self.stop_event.clear()
        self.toggle_buttons(True)
        threading.Thread(target=self.run_ocr, daemon=True).start()

    def run_ocr(self):
        try:
            self.log("OCR処理を開始します...")
            project_folder = self.working_folder_var.get()
            
            if not os.path.exists(project_folder):
                self.log("プロジェクトフォルダが見つかりません")
                return

            ocr_folder = os.path.join(project_folder, "OCR_Results_Final")
            if not os.path.exists(ocr_folder):
                os.makedirs(ocr_folder)

            # Swiftスクリプト作成
            swift_script_path = self.create_swift_ocr_script()
            
            # 画像ファイル取得
            images = sorted([f for f in os.listdir(project_folder) if f.endswith(".png")])
            if not images:
                self.log("画像ファイルが見つかりません")
                return
            
            total = len(images)
            processed = 0
            
            for i, image_file in enumerate(images):
                if self.stop_event.is_set(): break
                
                self.log(f"OCR処理中 ({i+1}/{total}): {image_file}")
                image_path = os.path.join(project_folder, image_file)
                
                text = self.perform_ocr_swift(image_path, swift_script_path)
                
                if text and len(text) > 10:
                    # テキストクリーンアップ（スペース除去）
                    text = self.cleanup_ocr_text(text)
                    
                    base_name = os.path.splitext(image_file)[0]
                    text_file = os.path.join(ocr_folder, f"{base_name}_final.txt")
                    with open(text_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    processed += 1
            
            # クリーンアップ
            if os.path.exists(swift_script_path):
                os.remove(swift_script_path)
                
            self.log(f"OCR完了: {processed}/{total} ファイル")
            
        except Exception as e:
            self.log(f"OCRエラー: {e}")
        finally:
            self.toggle_buttons(False)

    def cleanup_ocr_text(self, text):
        """OCRテキストのクリーンアップ: 単一スペースを削除、連続スペースは1つに"""
        import re
        # 2文字以上の連続スペースを一時的にプレースホルダーに置換
        text = re.sub(r' {2,}', '<<<SPACE>>>', text)
        # 単一の半角スペースを削除
        text = text.replace(' ', '')
        # プレースホルダーを1つのスペースに戻す
        text = text.replace('<<<SPACE>>>', ' ')
        return text

    def create_swift_ocr_script(self):
        swift_code = """#!/usr/bin/swift
import Foundation
import Vision
import AppKit

func performOCR(imagePath: String) {
    guard let image = NSImage(contentsOfFile: imagePath) else { return }
    guard let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return }
    
    let request = VNRecognizeTextRequest()
    request.recognitionLanguages = ["ja-JP", "en-US"]
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    
    do {
        try handler.perform([request])
        guard let observations = request.results else { return }
        let recognizedStrings = observations.compactMap { $0.topCandidates(1).first?.string }
        let extractedText = recognizedStrings.joined(separator: "\\n")
        print(extractedText)
    } catch {}
}

if CommandLine.arguments.count > 1 {
    performOCR(imagePath: CommandLine.arguments[1])
}
"""
        script_path = "/tmp/kindle_ocr.swift"
        with open(script_path, 'w') as f:
            f.write(swift_code)
        os.chmod(script_path, 0o755)
        return script_path

    def perform_ocr_swift(self, image_path, script_path):
        try:
            result = subprocess.run([script_path, image_path], capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return ""


    def start_pdf(self):
        self.save_config()
        self.stop_event.clear()
        self.toggle_buttons(True)
        threading.Thread(target=self.run_pdf, daemon=True).start()

    def run_pdf(self):
        try:
            self.log("PDF作成を開始します...")
            project_folder = self.working_folder_var.get()
            project_name = os.path.basename(project_folder)
            
            if not os.path.exists(project_folder):
                self.log("プロジェクトフォルダが見つかりません")
                return

            # 1. 画像のみのPDF作成
            pdf_path = os.path.join(project_folder, f"{project_name}.pdf")
            self.create_image_pdf(project_folder, pdf_path)
            
            # 2. 検索可能PDF作成 (OCR結果がある場合)
            ocr_folder = os.path.join(project_folder, "OCR_Results_Final")
            if os.path.exists(ocr_folder):
                self.log("検索可能PDFを作成中...")
                searchable_folder = os.path.join(project_folder, "PDF_Searchable_Fixed")
                if not os.path.exists(searchable_folder):
                    os.makedirs(searchable_folder)
                
                swift_pdf_script = self.create_swift_pdf_script()
                
                images = sorted([f for f in os.listdir(project_folder) if f.endswith(".png")])
                total = len(images)
                processed = 0
                
                for i, image_file in enumerate(images):
                    if self.stop_event.is_set(): break
                    
                    base_name = os.path.splitext(image_file)[0]
                    text_file = os.path.join(ocr_folder, f"{base_name}_final.txt")
                    
                    if os.path.exists(text_file):
                        self.log(f"検索可能PDF作成 ({i+1}/{total}): {image_file}")
                        image_path = os.path.join(project_folder, image_file)
                        output_path = os.path.join(searchable_folder, f"{base_name}_searchable.pdf")
                        
                        if self.create_searchable_pdf_swift(image_path, text_file, output_path, swift_pdf_script):
                            processed += 1
                
                # 統合検索可能PDF
                if processed > 0:
                    self.combine_pdfs(searchable_folder, os.path.join(project_folder, f"{project_name}_Searchable.pdf"))
                
                if os.path.exists(swift_pdf_script):
                    os.remove(swift_pdf_script)

            self.log("PDF作成完了")
            
        except Exception as e:
            self.log(f"PDFエラー: {e}")
        finally:
            self.toggle_buttons(False)

    def create_image_pdf(self, folder, output_path):
        # sipsを使ってPDF作成 (簡易版)
        try:
            cmd = f"cd '{folder}' && ls page_*.png | sort -V | xargs -I {{}} sips -s format pdf {{}} --out temp_{{}}.pdf"
            subprocess.run(cmd, shell=True, check=True)
            
            # 結合 (pythonを使用)
            script = f"""
import os
from PyPDF2 import PdfWriter
writer = PdfWriter()
files = sorted([f for f in os.listdir('{folder}') if f.startswith('temp_') and f.endswith('.pdf')])
for f in files:
    writer.append(os.path.join('{folder}', f))
with open('{output_path}', 'wb') as f:
    writer.write(f)
"""
            subprocess.run(["python3", "-c", script], check=True)
            
            # 一時ファイル削除
            subprocess.run(f"cd '{folder}' && rm temp_*.pdf", shell=True)
            self.log(f"画像PDF作成: {os.path.basename(output_path)}")
            
        except Exception as e:
            self.log(f"画像PDF作成失敗: {e}")

    def create_swift_pdf_script(self):
        swift_code = """#!/usr/bin/swift
import Foundation
import PDFKit
import AppKit

func createSearchablePDF(imagePath: String, textPath: String, outputPath: String) -> Bool {
    guard let image = NSImage(contentsOfFile: imagePath) else { return false }
    guard let ocrText = try? String(contentsOfFile: textPath, encoding: .utf8) else { return false }
    
    guard let imageData = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: imageData),
          let pdfImageData = bitmap.representation(using: .jpeg, properties: [:]) else { return false }
          
    guard let pdfPage = PDFPage(image: NSImage(data: pdfImageData)!) else { return false }
    
    let pageRect = pdfPage.bounds(for: .mediaBox)
    let hiddenRect = CGRect(x: pageRect.maxX - 1, y: pageRect.maxY - 1, width: 1, height: 1)
    
    let annotation = PDFAnnotation(bounds: hiddenRect, forType: .freeText, withProperties: nil)
    annotation.contents = ocrText
    annotation.font = NSFont.systemFont(ofSize: 0.1)
    annotation.fontColor = .clear
    annotation.color = .clear
    annotation.border = nil
    
    pdfPage.addAnnotation(annotation)
    
    let pdfDocument = PDFDocument()
    pdfDocument.insert(pdfPage, at: 0)
    
    return pdfDocument.write(to: URL(fileURLWithPath: outputPath))
}

if CommandLine.arguments.count > 3 {
    let success = createSearchablePDF(imagePath: CommandLine.arguments[1], 
                                    textPath: CommandLine.arguments[2], 
                                    outputPath: CommandLine.arguments[3])
    exit(success ? 0 : 1)
}
"""
        script_path = "/tmp/kindle_pdf.swift"
        with open(script_path, 'w') as f:
            f.write(swift_code)
        os.chmod(script_path, 0o755)
        return script_path

    def create_searchable_pdf_swift(self, image_path, text_path, output_path, script_path):
        try:
            subprocess.run([script_path, image_path, text_path, output_path], check=True)
            return True
        except:
            return False

    def combine_pdfs(self, input_folder, output_path):
        try:
            # PyPDF2を使ってPDF結合
            from PyPDF2 import PdfWriter
            
            writer = PdfWriter()
            pdfs = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".pdf")])
            
            for pdf_path in pdfs:
                writer.append(pdf_path)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            self.log(f"検索可能PDF結合完了: {os.path.basename(output_path)}")
        except Exception as e:
            self.log(f"PDF結合失敗: {e}")


    def start_full_auto(self):
        self.save_config()
        self.stop_event.clear()
        self.toggle_buttons(True)
        threading.Thread(target=self.run_full_auto, daemon=True).start()

    def run_full_auto(self):
        try:
            self.log("全自動処理を開始します...")
            self.run_capture()
            if not self.stop_event.is_set():
                self.run_ocr()
            if not self.stop_event.is_set():
                self.run_pdf()
            self.log("全工程完了")
        except Exception as e:
            self.log(f"エラー: {e}")
        finally:
            self.toggle_buttons(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = KindleAutomationGUI(root)
    root.mainloop()
