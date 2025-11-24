-- Kindle Automation All-in-One Script
-- 統合版 Kindle書籍自動化スクリプト
-- 機能: スクリーンショット撮影, OCR処理, テキスト統合, 検索可能PDF作成

-- ========================================
-- 設定プロパティ (共通)
-- ========================================
property bookTitle : "KindleBook_Screenshots"
property pageWaitTime : 3
property maxPages : 50
property duplicateThreshold : 1 -- 1回重複で即座終了
property screenshotQuality : 150

-- ========================================
-- メイン処理
-- ========================================
on run
	try
		display dialog "Kindle自動化ツール (統合版)" & return & return & "実行したい処理を選択してください:" buttons {"キャンセル", "テキスト統合/PDF化", "撮影からOCRまで"} default button "撮影からOCRまで"
		
		set mainAction to button returned of result
		
		if mainAction is "撮影からOCRまで" then
			my runFullWorkflow()
		else if mainAction is "テキスト統合/PDF化" then
			my runPostProcessing()
		end if
		
	on error errMsg number errNum
		if errNum is not -128 then
			display dialog "エラーが発生しました: " & errMsg buttons {"OK"}
		end if
	end try
end run

-- ========================================
-- ワークフロー制御
-- ========================================

-- フルワークフロー (撮影 -> PDF -> OCR -> 検索可能PDF -> テキスト統合)
on runFullWorkflow()
	-- Step 1: 撮影 & PDF作成
	set captureResult to my runScreenshotTask()
	if captureResult is false then return
	
	set projectFolder to item 1 of captureResult
	
	-- Step 2: OCR処理
	display dialog "撮影が完了しました。OCR処理を開始しますか？" buttons {"終了", "開始"} default button "開始"
	if button returned of result is "終了" then return
	
	my runOCRTask(projectFolder)
	
	-- Step 3: 検索可能PDF & テキスト統合
	display dialog "OCR処理が完了しました。検索可能PDF作成とテキスト統合を行いますか？" buttons {"終了", "開始"} default button "開始"
	if button returned of result is "終了" then return
	
	my runSearchablePDFTask(projectFolder)
	my runTextMergeTask(projectFolder)
	
	display dialog "全ての処理が完了しました！" buttons {"OK"}
end runFullWorkflow

-- 後処理ワークフロー (OCR以降のみ)
on runPostProcessing()
	set selectedFolder to choose folder with prompt "プロジェクトフォルダを選択してください："
	set projectFolder to selectedFolder as string
	
	set actionList to {"OCR処理", "検索可能PDF作成", "テキスト統合"}
	set selectedAction to choose from list actionList with prompt "実行する処理を選択:" default items {"OCR処理"}
	
	if selectedAction is false then return
	set actionName to item 1 of selectedAction
	
	if actionName is "OCR処理" then
		my runOCRTask(projectFolder)
	else if actionName is "検索可能PDF作成" then
		my runSearchablePDFTask(projectFolder)
	else if actionName is "テキスト統合" then
		my runTextMergeTask(projectFolder)
	end if
end runPostProcessing

-- ========================================
-- 1. スクリーンショット撮影機能
-- ========================================
on runScreenshotTask()
	-- Step 1: 初期化
	if not my initializeScript() then return false
	
	-- Step 2: ユーザー設定
	set userConfig to my getUserConfiguration()
	if userConfig is false then return false
	
	-- Step 3: プロジェクトフォルダ作成
	set projectFolder to my createProjectFolder(userConfig)
	
	-- Step 4: Kindleアプリ準備
	if not my prepareKindleApp() then return false
	
	-- Step 5: 実行確認
	set startDialog to display dialog "準備完了" & return & return & "設定:" & return & "• プロジェクト: " & (projectName of userConfig) & return & "• 最大ページ数: " & (maxPages of userConfig) & return & "• 待機時間: " & (pageWaitTime of userConfig) & "秒" & return & "• 書籍終了検知: 即座停止" & return & return & "スクリーンショットを開始しますか？" buttons {"キャンセル", "開始"} default button "開始"
	
	if button returned of startDialog is "キャンセル" then return false
	
	-- Step 6: スクリーンショット処理
	set captureResult to my executeScreenshotCapture(projectFolder, userConfig)
	
	-- Step 7: PDF統合処理
	set pdfResult to my executePDFGeneration(projectFolder, userConfig, captureResult)
	
	-- Step 8: 完了レポート
	my showCompletionReport(projectFolder, captureResult, pdfResult)
	
	return {projectFolder, captureResult}
end runScreenshotTask

-- 初期化
on initializeScript()
	try
		tell application "System Events"
			set frontApp to name of first process whose frontmost is true
		end tell
		return true
	on error
		display dialog "アクセシビリティ権限が必要です。" buttons {"OK"}
		return false
	end try
end initializeScript

-- ユーザー設定取得
on getUserConfiguration()
	try
		set nameDialog to display dialog "プロジェクト名を入力してください:" default answer bookTitle buttons {"キャンセル", "OK"} default button "OK"
		if button returned of nameDialog is "キャンセル" then return false
		set projectName to text returned of nameDialog
		
		set advancedDialog to display dialog "詳細設定を変更しますか？" & return & return & "現在の設定:" & return & "• ページ間待機: " & pageWaitTime & "秒" & return & "• 最大ページ数: " & maxPages & return & "• 書籍終了検知: 即座停止" buttons {"デフォルト使用", "詳細設定"} default button "デフォルト使用"
		
		if button returned of advancedDialog is "詳細設定" then
			return my getAdvancedSettings(projectName)
		else
			return {projectName:projectName, pageWaitTime:pageWaitTime, maxPages:maxPages, duplicateThreshold:duplicateThreshold}
		end if
	on error
		return false
	end try
end getUserConfiguration

on getAdvancedSettings(projectName)
	try
		set waitDialog to display dialog "ページ間待機時間（秒）:" default answer (pageWaitTime as string) buttons {"OK"}
		set newWaitTime to (text returned of waitDialog) as integer
		
		set maxDialog to display dialog "最大ページ数（推奨50）:" default answer "50" buttons {"OK"}
		set newMaxPages to (text returned of maxDialog) as integer
		
		if newMaxPages > 100 then
			display dialog "安全のため100ページを上限とします。" buttons {"OK"}
			set newMaxPages to 100
		end if
		
		return {projectName:projectName, pageWaitTime:newWaitTime, maxPages:newMaxPages, duplicateThreshold:duplicateThreshold}
	on error
		return {projectName:projectName, pageWaitTime:pageWaitTime, maxPages:maxPages, duplicateThreshold:duplicateThreshold}
	end try
end getAdvancedSettings

-- プロジェクトフォルダ作成
on createProjectFolder(userConfig)
	try
		set desktopPath to (path to desktop) as string
		set folderName to projectName of userConfig
		set projectFolder to desktopPath & folderName & ":"
		
		tell application "Finder"
			if not (exists folder projectFolder) then
				make new folder at desktop with properties {name:folderName}
			end if
		end tell
		
		my saveProjectSettings(projectFolder, userConfig)
		return projectFolder
	on error
		return (path to desktop) as string
	end try
end createProjectFolder

on saveProjectSettings(projectFolder, userConfig)
	try
		set settingsPath to projectFolder & "project_settings.txt"
		set settingsContent to "プロジェクト設定" & return & "作成日時: " & (current date) & return & "プロジェクト名: " & (projectName of userConfig) & return & "ページ間待機: " & (pageWaitTime of userConfig) & "秒" & return & "最大ページ数: " & (maxPages of userConfig) & return & "書籍終了検知: 即座停止" & return
		
		set settingsFile to open for access file settingsPath with write permission
		write settingsContent to settingsFile
		close access settingsFile
	on error
		try
			close access file (projectFolder & "project_settings.txt")
		end try
	end try
end saveProjectSettings

-- Kindleアプリ準備
on prepareKindleApp()
	try
		tell application "Amazon Kindle"
			activate
		end tell
		delay 1
		tell application "System Events"
			tell process "Kindle"
				if not (exists front window) then
					display dialog "Kindleウィンドウが見つかりません。" buttons {"OK"}
					return false
				end if
				set frontWindow to front window
				try
					if value of attribute "AXFullScreen" of frontWindow is true then
						click (first button of frontWindow whose description is "full screen")
						delay 1
					end if
				end try
			end tell
		end tell
		delay 1
		return true
	on error errMsg
		display dialog "Kindleアプリエラー: " & errMsg buttons {"OK"}
		return false
	end try
end prepareKindleApp

-- スクリーンショット実行
on executeScreenshotCapture(projectFolder, userConfig)
	set pageCounter to 1
	set previousScreenshot to ""
	set sameScreenshotCount to 0
	set captureStartTime to current date
	
	repeat
		set screenshotPath to projectFolder & "page_" & my formatPageNumber(pageCounter) & ".png"
		set screenshotSuccess to my captureKindleScreen(screenshotPath)
		
		set currentScreenshotHash to my getImageHash(screenshotPath)
		
		if currentScreenshotHash = previousScreenshot then
			set sameScreenshotCount to sameScreenshotCount + 1
			if sameScreenshotCount ≥ 1 then
				try
					do shell script "rm -f '" & POSIX path of screenshotPath & "'"
				end try
				set pageCounter to pageCounter - 1
				display dialog "書籍の最終ページに到達しました。" buttons {"OK"} giving up after 3
				exit repeat
			end if
		else
			set sameScreenshotCount to 0
		end if
		
		if pageCounter ≥ (maxPages of userConfig) then
			display dialog "最大ページ数に到達しました。" buttons {"OK"} giving up after 3
			exit repeat
		end if
		
		my navigateToNextPage()
		delay (pageWaitTime of userConfig)
		
		set previousScreenshot to currentScreenshotHash
		set pageCounter to pageCounter + 1
	end repeat
	
	set captureEndTime to current date
	set processingTime to captureEndTime - captureStartTime
	
	return {totalPages:pageCounter, processingTime:processingTime, startTime:captureStartTime, endTime:captureEndTime}
end executeScreenshotCapture

on captureKindleScreen(savePath)
	try
		tell application "System Events"
			tell process "Kindle"
				if exists front window then
					set frontWindow to front window
					set {windowX, windowY} to position of frontWindow
					set {windowW, windowH} to size of frontWindow
				else
					tell application "Amazon Kindle" to activate
					delay 1
					set frontWindow to front window
					set {windowX, windowY} to position of frontWindow
					set {windowW, windowH} to size of frontWindow
				end if
			end tell
		end tell
		
		set cropX to windowX + 20
		set cropY to windowY + 80
		set cropW to windowW - 40
		set cropH to windowH - 120
		
		do shell script "screencapture -x -R " & cropX & "," & cropY & "," & cropW & "," & cropH & " '" & POSIX path of savePath & "'"
		return true
	on error
		return false
	end try
end captureKindleScreen

on navigateToNextPage()
	try
		tell application "Amazon Kindle" to activate
		delay 1
		tell application "System Events"
			tell process "Kindle"
				set frontmost to true
				key code 124
			end tell
		end tell
	on error
	end try
end navigateToNextPage

on executePDFGeneration(projectFolder, userConfig, captureResult)
	set pdfStartTime to current date
	set projectName to projectName of userConfig
	set pdfPath to projectFolder & projectName & ".pdf"
	
	try
		set folderPOSIX to POSIX path of projectFolder
		set pdfPathPOSIX to POSIX path of pdfPath
		
		set pdfScript to "#!/bin/bash
cd '" & folderPOSIX & "'
image_count=$(ls page_*.png 2>/dev/null | wc -l)
if [ $image_count -eq 0 ]; then exit 1; fi
ls page_*.png | sort -V | xargs -I {} sips -s format pdf {} --out temp_{}.pdf
if command -v gs >/dev/null 2>&1; then
    gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE='" & pdfPathPOSIX & "' -dBATCH temp_*.pdf 2>/dev/null
else
    python3 -c \"
import os
from PyPDF2 import PdfWriter
import sys
writer = PdfWriter()
temp_files = sorted([f for f in os.listdir('.') if f.startswith('temp_') and f.endswith('.pdf')])
if not temp_files: sys.exit(1)
try:
    for temp_file in temp_files:
        with open(temp_file, 'rb') as f: writer.append_fileobj(f)
    with open('" & pdfPathPOSIX & "', 'wb') as output_file: writer.write(output_file)
except: sys.exit(1)
\"
fi
rm -f temp_*.pdf
"
		do shell script pdfScript
		set pdfEndTime to current date
		return {success:true, pdfPath:pdfPath, processingTime:(pdfEndTime - pdfStartTime)}
	on error errMsg
		return {success:false, errorMsg:errMsg, manualSteps:true}
	end try
end executePDFGeneration

on showCompletionReport(projectFolder, captureResult, pdfResult)
	set reportText to "処理完了" & return & "ページ数: " & (totalPages of captureResult)
	display dialog reportText buttons {"フォルダを開く", "OK"} default button "フォルダを開く"
	if button returned of result is "フォルダを開く" then
		tell application "Finder"
			open folder projectFolder
		end tell
	end if
end showCompletionReport

-- ========================================
-- 2. OCR処理機能
-- ========================================
on runOCRTask(projectFolderPath)
	set ocrOutputFolder to projectFolderPath & "OCR_Results_Final"
	
	tell application "Finder"
		if not (exists folder ocrOutputFolder) then
			make new folder at (projectFolderPath as alias) with properties {name:"OCR_Results_Final"}
		end if
	end tell
	
	set swiftScriptPath to createStdoutOCRScript()
	set imageFiles to getImageFiles(projectFolderPath)
	
	if (count of imageFiles) = 0 then
		display dialog "画像が見つかりません" buttons {"OK"}
		return
	end if
	
	set processedCount to 0
	set totalFiles to count of imageFiles
	set allExtractedText to ""
	
	repeat with i from 1 to totalFiles
		set currentFile to item i of imageFiles
		set fileName to name of (info for currentFile)
		
		display notification "OCR処理中: " & fileName & " (" & i & "/" & totalFiles & ")" with title "OCR"
		
		set extractedText to performStdoutOCR(currentFile, swiftScriptPath)
		
		if extractedText is not "" and (length of extractedText) > 10 then
			set textFileName to (text 1 thru -5 of fileName) & "_final.txt"
			set textFilePath to ocrOutputFolder & ":" & textFileName
			writeTextToFileRobust(extractedText, textFilePath)
			
			set allExtractedText to allExtractedText & return & return & "=== " & fileName & " ===" & return & extractedText
			set processedCount to processedCount + 1
		end if
	end repeat
	
	if allExtractedText is not "" then
		set combinedFilePath to ocrOutputFolder & ":combined_final_text.txt"
		writeTextToFileRobust(allExtractedText, combinedFilePath)
	end if
	
	do shell script "rm -f " & quoted form of swiftScriptPath
	
	display dialog "OCR完了: " & processedCount & "/" & totalFiles buttons {"OK"}
end runOCRTask

on createStdoutOCRScript()
	set swiftCode to "#!/usr/bin/swift
import Foundation
import Vision
import AppKit

func performOCR(imagePath: String) {
    guard let image = NSImage(contentsOfFile: imagePath) else { return }
    guard let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return }
    
    let request = VNRecognizeTextRequest()
    request.recognitionLanguages = [\"ja-JP\", \"en-US\"]
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    
    do {
        try handler.perform([request])
        guard let observations = request.results else { return }
        let recognizedStrings = observations.compactMap { $0.topCandidates(1).first?.string }
        let extractedText = recognizedStrings.joined(separator: \"\\n\")
        print(extractedText)
    } catch {}
}

if CommandLine.arguments.count > 1 {
    performOCR(imagePath: CommandLine.arguments[1])
}
"
	set tempScriptPath to "/tmp/stdout_ocr_final.swift"
	do shell script "cat > " & quoted form of tempScriptPath & " << 'EOF'" & return & swiftCode & return & "EOF"
	do shell script "chmod +x " & quoted form of tempScriptPath
	return tempScriptPath
end createStdoutOCRScript

on performStdoutOCR(imageFile, swiftScriptPath)
	try
		set imagePath to POSIX path of imageFile
		set ocrOutput to do shell script "swift " & quoted form of swiftScriptPath & " " & quoted form of imagePath & " 2>/dev/null"
		if ocrOutput is not "" then
			return do shell script "echo " & quoted form of ocrOutput & " | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$' | head -50"
		else
			return ""
		end if
	on error
		return ""
	end try
end performStdoutOCR

on writeTextToFileRobust(textContent, filePath)
	try
		if textContent is "" then return
		set posixPath to POSIX path of filePath
		do shell script "cat > " & quoted form of posixPath & " << 'EOF'" & return & textContent & return & "EOF"
	on error
	end try
end writeTextToFileRobust

on getImageFiles(folderPath)
	set imageFiles to {}
	tell application "Finder"
		set folderItems to every file of folder folderPath whose name extension is "png"
		repeat with currentItem in folderItems
			set end of imageFiles to currentItem as alias
		end repeat
	end tell
	return sortFilesByName(imageFiles)
end getImageFiles

on sortFilesByName(fileList)
	set sortedList to {}
	set fileNames to {}
	repeat with currentFile in fileList
		set fileName to name of (info for currentFile)
		set end of fileNames to {fileName, currentFile}
	end repeat
	
	repeat with i from 1 to (count of fileNames)
		repeat with j from 1 to (count of fileNames) - 1
			set file1 to item j of fileNames
			set file2 to item (j + 1) of fileNames
			if (item 1 of file1) > (item 1 of file2) then
				set item j of fileNames to file2
				set item (j + 1) of fileNames to file1
			end if
		end repeat
	end repeat
	
	repeat with fileInfo in fileNames
		set end of sortedList to (item 2 of fileInfo)
	end repeat
	return sortedList
end sortFilesByName

-- ========================================
-- 3. 検索可能PDF作成機能
-- ========================================
on runSearchablePDFTask(projectFolderPath)
	set outputFolder to projectFolderPath & "PDF_Searchable_Fixed"
	tell application "Finder"
		if not (exists folder outputFolder) then
			make new folder at (projectFolderPath as alias) with properties {name:"PDF_Searchable_Fixed"}
		end if
	end tell
	
	set swiftScriptPath to createInvisibleTextScript()
	set filePairs to getImageTextPairs(projectFolderPath)
	
	if (count of filePairs) = 0 then
		display dialog "対応する画像・テキストファイルが見つかりません" buttons {"OK"}
		return
	end if
	
	set processedCount to 0
	set totalFiles to count of filePairs
	
	repeat with i from 1 to totalFiles
		set currentPair to item i of filePairs
		set imageFile to item 1 of currentPair
		set textFile to item 2 of currentPair
		set fileName to item 3 of currentPair
		
		display notification "PDF作成中: " & fileName & " (" & i & "/" & totalFiles & ")" with title "PDF"
		
		if createInvisibleTextPDF(imageFile, textFile, outputFolder, fileName, swiftScriptPath) then
			set processedCount to processedCount + 1
		end if
	end repeat
	
	if processedCount > 1 then
		createCombinedPDFFixed(outputFolder)
	end if
	
	do shell script "rm -f " & quoted form of swiftScriptPath
	display dialog "PDF作成完了: " & processedCount & "/" & totalFiles buttons {"OK"}
end runSearchablePDFTask

on createInvisibleTextScript()
	set swiftCode to "#!/usr/bin/swift
import Foundation
import PDFKit
import AppKit

func createSearchablePDFFixed(imagePath: String, textPath: String, outputPath: String) -> Bool {
    guard let image = NSImage(contentsOfFile: imagePath) else { return false }
    guard let ocrText = try? String(contentsOfFile: textPath, encoding: .utf8) else { return false }
    guard let imageData = image.tiffRepresentation, let bitmap = NSBitmapImageRep(data: imageData), let pdfImageData = bitmap.representation(using: .jpeg, properties: [:]) else { return false }
    guard let pdfPage = PDFPage(image: NSImage(data: pdfImageData)!) else { return false }
    
    let pageRect = pdfPage.bounds(for: .mediaBox)
    let hiddenRect = CGRect(x: pageRect.maxX - 1, y: pageRect.maxY - 1, width: 1, height: 1)
    let hiddenAnnotation = PDFAnnotation(bounds: hiddenRect, forType: .freeText, withProperties: nil)
    hiddenAnnotation.contents = ocrText
    hiddenAnnotation.font = NSFont.systemFont(ofSize: 0.1)
    hiddenAnnotation.fontColor = NSColor.clear
    hiddenAnnotation.color = NSColor.clear
    hiddenAnnotation.border = nil
    pdfPage.addAnnotation(hiddenAnnotation)
    
    let pdfDocument = PDFDocument()
    pdfDocument.insert(pdfPage, at: 0)
    
    guard let finalPDFData = pdfDocument.dataRepresentation() else { return false }
    do { try finalPDFData.write(to: URL(fileURLWithPath: outputPath)); return true } catch { return false }
}

if CommandLine.arguments.count > 3 {
    let success = createSearchablePDFFixed(imagePath: CommandLine.arguments[1], textPath: CommandLine.arguments[2], outputPath: CommandLine.arguments[3])
    exit(success ? 0 : 1)
}
"
	set scriptPath to "/tmp/invisible_text_pdf.swift"
	do shell script "cat > " & quoted form of scriptPath & " << 'EOF'" & return & swiftCode & return & "EOF"
	do shell script "chmod +x " & quoted form of scriptPath
	return scriptPath
end createInvisibleTextScript

on createInvisibleTextPDF(imageFile, textFile, outputFolder, fileName, swiftScriptPath)
	try
		set imagePath to POSIX path of imageFile
		set textPath to POSIX path of textFile
		set outputPath to POSIX path of outputFolder & "/" & (text 1 thru -5 of fileName) & "_searchable_fixed.pdf"
		set result to do shell script "swift " & quoted form of swiftScriptPath & " " & quoted form of imagePath & " " & quoted form of textPath & " " & quoted form of outputPath & "; echo $?"
		return (last paragraph of result) as integer = 0
	on error
		return false
	end try
end createInvisibleTextPDF

on createCombinedPDFFixed(outputFolder)
	try
		do shell script "cd " & quoted form of (POSIX path of outputFolder) & " && " & "\"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py\" -o combined_searchable_fixed.pdf *_searchable_fixed.pdf"
	on error
		try
			do shell script "cd " & quoted form of (POSIX path of outputFolder) & " && ls *_searchable_fixed.pdf | head -1 | xargs -I {} cp {} combined_searchable_fixed.pdf"
		end try
	end try
end createCombinedPDFFixed

on getImageTextPairs(folderPath)
	set filePairs to {}
	tell application "Finder"
		set imageFiles to every file of folder folderPath whose name extension is "png"
		repeat with imageFile in imageFiles
			set imageName to name of imageFile
			set baseName to text 1 thru -5 of imageName
			set textFile to missing value
			try
				set ocrFolder to folder (folderPath & "OCR_Results_Final")
				if exists file (baseName & "_final.txt") of ocrFolder then
					set textFile to file (baseName & "_final.txt") of ocrFolder
				end if
			end try
			if textFile is not missing value then
				set end of filePairs to {imageFile as alias, textFile as alias, imageName}
			end if
		end repeat
	end tell
	return filePairs
end getImageTextPairs

-- ========================================
-- 4. テキスト統合機能
-- ========================================
on runTextMergeTask(projectFolderPath)
	set ocrResultsFolder to projectFolderPath & "OCR_Results_Final:"
	
	tell application "Finder"
		if not (exists folder ocrResultsFolder) then
			display dialog "OCR結果フォルダが見つかりません" buttons {"OK"}
			return
		end if
		
		set allFiles to every file of folder ocrResultsFolder whose name contains "_final.txt"
		set textFilesList to {}
		repeat with aFile in allFiles
			set fileName to name of aFile as string
			if fileName starts with "page_" and fileName ends with "_final.txt" then
				set end of textFilesList to fileName
			end if
		end repeat
	end tell
	
	if length of textFilesList = 0 then return
	
	set sortedFilesList to my sortPageFiles(textFilesList)
	set mergedContent to ""
	set fileCounter to 0
	
	repeat with fileName in sortedFilesList
		set fileCounter to fileCounter + 1
		set filePath to ocrResultsFolder & fileName
		try
			set fileContent to read file filePath as «class utf8»
			if fileCounter = 1 then
				set mergedContent to fileContent
			else
				set mergedContent to mergedContent & return & return & fileContent
			end if
		on error
		end try
	end repeat
	
	set currentDate to current date
	set dateString to my formatDate(currentDate)
	set outputFileName to "merged_book_" & dateString & ".txt"
	set outputPath to projectFolderPath & outputFileName
	
	try
		set fileRef to open for access file outputPath with write permission
		set eof fileRef to 0
		write mergedContent to fileRef as «class utf8»
		close access fileRef
		display dialog "テキスト統合完了: " & outputFileName buttons {"OK"}
	on error
	end try
end runTextMergeTask

on sortPageFiles(fileList)
	set sortedList to {}
	set sortPairs to {}
	repeat with fileName in fileList
		set pageNum to my extractPageNumber(fileName as string)
		try
			set numericValue to pageNum as integer
			set end of sortPairs to {numericValue, fileName}
		on error
		end try
	end repeat
	
	set listLength to length of sortPairs
	repeat with i from 1 to listLength - 1
		repeat with j from 1 to listLength - i
			set currentPair to item j of sortPairs
			set nextPair to item (j + 1) of sortPairs
			if (item 1 of currentPair) > (item 1 of nextPair) then
				set item j of sortPairs to nextPair
				set item (j + 1) of sortPairs to currentPair
			end if
		end repeat
	end repeat
	
	repeat with sortPair in sortPairs
		set end of sortedList to (item 2 of sortPair)
	end repeat
	return sortedList
end sortPageFiles

on extractPageNumber(fileName)
	try
		set pageStart to (offset of "page_" in fileName) + 5
		set pageEnd to (offset of "_final.txt" in fileName) - 1
		if pageEnd > pageStart then
			return text pageStart thru pageEnd of fileName
		else
			return "000"
		end if
	on error
		return "000"
	end try
end extractPageNumber

on formatDate(dateObj)
	try
		set yearStr to year of dateObj as string
		set monthNum to month of dateObj as integer
		set dayNum to day of dateObj
		set hourNum to hours of dateObj
		set minuteNum to minutes of dateObj
		
		return yearStr & monthNum & dayNum & "_" & hourNum & minuteNum
	on error
		return "backup_" & (random number from 1000 to 9999)
	end try
end formatDate

-- 共通ユーティリティ
on formatPageNumber(pageNum)
	if pageNum < 10 then
		return "00" & pageNum
	else if pageNum < 100 then
		return "0" & pageNum
	else
		return pageNum as string
	end if
end formatPageNumber

on getImageHash(imagePath)
	try
		return do shell script "md5 -q '" & POSIX path of imagePath & "'"
	on error
		return random number from 1 to 999999
	end try
end getImageHash
