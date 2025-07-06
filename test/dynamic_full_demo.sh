#!/bin/bash

# Dynamic Full Demo Script for emotional-decoration
# CSSファイル配置のみでScrollCastと統合
# Usage: ./test/dynamic_full_demo.sh [input_file]

# デフォルト値（ScrollCastと同じディレクトリ構造）
INPUT_FILE=${1:-"../sample_eng.txt"}
OUTPUT_DIR="../contents"
SCROLL_CAST_DIR="../scroll-cast"
EMO_DECO_CSS_DIR="css"

# ヘルプ表示
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "🎨 Dynamic Full Demo Script for emotional-decoration"
    echo
    echo "CSSファイル配置のみでScrollCastと統合"
    echo "HTMLファイル編集は一切行わず、CSSによる装飾のみ"
    echo
    echo "Usage: $0 [input_file]"
    echo
    echo "Arguments:"
    echo "  input_file   Input text file (default: ../scroll-cast/test/sample_eng.txt)"
    echo
    echo "機能:"
    echo "  - 装飾CSSファイルの配置"
    echo "  - ScrollCast統一セレクター対応確認"
    echo "  - デモHTMLファイル生成（手動CSS適用例）"
    echo "  - 非干渉設計の検証"
    echo
    echo "Output:"
    echo "  📁 Directory: $OUTPUT_DIR/"
    echo "  🎨 CSS files: text-color-*.css"
    echo "  📝 Demo: css-integration-demo.html"
    echo
    exit 0
fi

# 入力ファイルの存在確認
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: Input file '$INPUT_FILE' not found"
    echo "   Scroll-castのサンプルファイルを確認してください"
    exit 1
fi

# 出力フォルダの作成
mkdir -p "$OUTPUT_DIR/css" "$OUTPUT_DIR/demo"

echo "🎨 Dynamic Full Demo - emotional-decoration (CSS配置のみ)"
echo "   Input: $INPUT_FILE"
echo "   Output Directory: $OUTPUT_DIR/"
echo "   ScrollCast Integration: $SCROLL_CAST_DIR/"
echo "   Mode: CSS-Only (HTMLファイル編集なし)"
echo

# 実行結果を記録する配列
declare -a RESULTS
declare -a DURATIONS

# 実行時間計測関数
measure_time() {
    local start_time=$(date +%s)
    "$@" > /tmp/emo_deco_output.log 2>&1
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    echo $duration
    return $exit_code
}

# CSS装飾ファイルをコピー
echo "🎨 CSS装飾ファイルの配置中..."

css_files_copied=0
css_files_total=0

# 基本CSS装飾ファイルをコピー
((css_files_total++))
if [ -f "$EMO_DECO_CSS_DIR/text-color-simple.css" ]; then
    cp "$EMO_DECO_CSS_DIR/text-color-simple.css" "$OUTPUT_DIR/css/"
    echo "   ✅ text-color-simple.css コピー完了"
    ((css_files_copied++))
else
    echo "   ❌ text-color-simple.css が見つかりません"
fi

((css_files_total++))
if [ -f "$EMO_DECO_CSS_DIR/scroll-cast-text-color-enhancement.css" ]; then
    cp "$EMO_DECO_CSS_DIR/scroll-cast-text-color-enhancement.css" "$OUTPUT_DIR/css/"
    echo "   ✅ scroll-cast-text-color-enhancement.css コピー完了"
    ((css_files_copied++))
else
    echo "   ❌ scroll-cast-text-color-enhancement.css が見つかりません"
fi

echo

# ScrollCast HTMLファイルの統一セレクター確認
echo "🔍 ScrollCast統一セレクター使用確認..."

html_files_found=0
selector_compatible_files=0

if [ -d "$OUTPUT_DIR/html" ]; then
    for html_file in "$OUTPUT_DIR/html"/demo_*railway*.html "$OUTPUT_DIR/html"/demo_*simple_role*.html; do
        if [ -f "$html_file" ]; then
            ((html_files_found++))
            
            # ファイル名から基本情報を抽出
            basename_file=$(basename "$html_file" .html)
            template_type=""
            
            # railway または scroll テンプレートかどうか判定
            if [[ "$basename_file" == *"railway"* ]]; then
                template_type="railway"
            elif [[ "$basename_file" == *"simple_role"* ]]; then
                template_type="scroll"
            fi
            
            # 統一セレクター使用確認
            if [ -n "$template_type" ]; then
                text_container_count=$(grep -c 'class="text-container"' "$html_file" 2>/dev/null || echo "0")
                text_line_count=$(grep -c 'class="text-line"' "$html_file" 2>/dev/null || echo "0")
                data_template_count=$(grep -c "data-template=\"$template_type\"" "$html_file" 2>/dev/null || echo "0")
                
                if [ "$text_container_count" -gt 0 ] && [ "$text_line_count" -gt 0 ] && [ "$data_template_count" -gt 0 ]; then
                    echo "   ✅ $basename_file: セレクター対応済み (.text-container: $text_container_count, .text-line: $text_line_count)"
                    ((selector_compatible_files++))
                else
                    echo "   ❌ $basename_file: セレクター未対応 (.text-container: $text_container_count, .text-line: $text_line_count)"
                fi
            else
                echo "   ⚠️  $basename_file: Template-Based Architecture非対応"
            fi
        fi
    done
else
    echo "   ❌ Error: $OUTPUT_DIR/html/ ディレクトリが見つかりません"
    echo "   まずScrollCastのdynamic_full_demo.shを実行してください"
    exit 1
fi

echo

# ====================================================================
# CSS統合デモファイルの生成 (デバッグ時のみ有効化)
# デバッグが必要な場合は、以下のコメント(<<'DEBUG_DEMO')を外してください
# ====================================================================
: <<'DEBUG_DEMO'
echo "📝 CSS統合デモファイル生成中..."

demo_file="$OUTPUT_DIR/demo/css-integration-demo.html"
mkdir -p "$OUTPUT_DIR/demo"

# サンプルHTMLファイルを選択（railway と scroll から1つずつ）
sample_railway=$(find "$OUTPUT_DIR/html" -name "demo_*railway*.html" | head -n 1)
sample_scroll=$(find "$OUTPUT_DIR/html" -name "demo_*simple_role*.html" | head -n 1)

cat > "$demo_file" << 'EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScrollCast + Emotional Decoration CSS統合デモ</title>
    
    <!-- Emotional Decoration CSS -->
    <link rel="stylesheet" href="../css/text-color-simple.css">
    <link rel="stylesheet" href="../css/scroll-cast-text-color-enhancement.css">
    
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #000;
            color: #fff;
            line-height: 1.6;
        }
        
        h1, h2 {
            color: #00ff88;
            text-align: center;
        }
        
        .demo-section {
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #333;
            border-radius: 8px;
        }
        
        .file-link {
            display: inline-block;
            margin: 10px;
            padding: 8px 16px;
            background: #333;
            color: #00ff88;
            text-decoration: none;
            border-radius: 4px;
        }
        
        .file-link:hover {
            background: #555;
        }
        
        .status {
            text-align: center;
            font-size: 18px;
            margin: 20px 0;
        }
        
        .integration-info {
            background: rgba(0, 255, 136, 0.1);
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>ScrollCast + Emotional Decoration CSS統合デモ</h1>
    
    <div class="status">
        🎨 CSS-Only Integration: HTMLファイル編集なし
    </div>
    
    <div class="integration-info">
        <h3>🔧 統合方法</h3>
        <p>ScrollCast生成HTMLファイルに以下のCSSを追加するだけで装飾が適用されます：</p>
        <pre><code>&lt;link rel="stylesheet" href="css/text-color-simple.css"&gt;
&lt;link rel="stylesheet" href="css/scroll-cast-text-color-enhancement.css"&gt;</code></pre>
    </div>
    
    <div class="demo-section">
        <h2>📁 生成済みScrollCastファイル</h2>
        <p>以下のファイルにCSS装飾を手動で適用できます：</p>
        
        <h3>🚂 Railway Template</h3>
EOF

# Railway テンプレートファイルのリンクを追加
for file in "$OUTPUT_DIR/html"/demo_*railway*.html; do
    if [ -f "$file" ]; then
        basename_file=$(basename "$file")
        echo "        <a href=\"../html/$basename_file\" class=\"file-link\" target=\"_blank\">$basename_file</a>" >> "$demo_file"
    fi
done

cat >> "$demo_file" << 'EOF'
        
        <h3>📜 Scroll Template</h3>
EOF

# Scroll テンプレートファイルのリンクを追加
for file in "$OUTPUT_DIR/html"/demo_*simple_role*.html; do
    if [ -f "$file" ]; then
        basename_file=$(basename "$file")
        echo "        <a href=\"../html/$basename_file\" class=\"file-link\" target=\"_blank\">$basename_file</a>" >> "$demo_file"
    fi
done

cat >> "$demo_file" << 'EOF'
    </div>
    
    <div class="demo-section">
        <h2>🎨 装飾CSS仕様</h2>
        <ul>
            <li><strong>統一セレクター:</strong> .text-container, .text-line</li>
            <li><strong>Railway Template:</strong> 緑色の駅表示スタイル (#00ff88)</li>
            <li><strong>Scroll Template:</strong> 金色の映画クレジットスタイル (#ffd700)</li>
            <li><strong>感情レイヤー:</strong> data-emotion属性サポート</li>
            <li><strong>非干渉設計:</strong> ScrollCast動作への影響なし</li>
        </ul>
    </div>
    
    <div class="demo-section">
        <h2>📝 使用例</h2>
        <p>既存のScrollCast HTMLファイルの&lt;head&gt;セクションに装飾CSSを追加：</p>
        <pre><code>&lt;!-- 元のScrollCast CSS --&gt;
&lt;link rel="stylesheet" href="shared/scrollcast-styles.css"&gt;
&lt;link rel="stylesheet" href="railway_scroll.css"&gt;

&lt;!-- Emotional Decoration CSS追加 --&gt;
&lt;link rel="stylesheet" href="css/text-color-simple.css"&gt;
&lt;link rel="stylesheet" href="css/scroll-cast-text-color-enhancement.css"&gt;</code></pre>
    </div>
    
    <div class="demo-section">
        <h2>🔍 技術詳細</h2>
        <ul>
            <li><strong>Template-Based Architecture:</strong> 統一セレクター対応</li>
            <li><strong>CSS Override Architecture:</strong> 追加的装飾のみ</li>
            <li><strong>Compatible Files:</strong> Railway + Scroll テンプレート</li>
            <li><strong>No File Modification:</strong> HTMLファイル編集なし</li>
        </ul>
    </div>
</body>
</html>
EOF

echo "   ✅ CSS統合デモファイル生成完了: $(basename "$demo_file")"
DEBUG_DEMO

echo

echo "=================================================================="
echo "🎯 emotional-decoration CSS配置完了!"

# 結果サマリー
echo
echo "📊 CSS配置結果サマリー:"
echo "┌─────────────────────────────────────┬──────────┐"
echo "│ CSS配置結果                         │ 状況     │"
echo "├─────────────────────────────────────┼──────────┤"
printf "│ %-35s │ %-8s │\n" "CSSファイル配置" "$css_files_copied/$css_files_total"
printf "│ %-35s │ %-8s │\n" "ScrollCast統一セレクター対応" "$selector_compatible_files/$html_files_found"
printf "│ %-35s │ %-8s │\n" "デモファイル生成" "0/0"
echo "└─────────────────────────────────────┴──────────┘"

# 生成されたファイル一覧
echo
echo "📁 配置されたファイル:"
if [ -d "$OUTPUT_DIR/css" ]; then
    css_count=$(find "$OUTPUT_DIR/css" -name "*.css" | wc -l)
    echo "   🎨 CSS ディレクトリ: $OUTPUT_DIR/css/ ($css_count ファイル)"
    for file in "$OUTPUT_DIR/css"/*.css; do
        if [ -f "$file" ]; then
            size=$(ls -lh "$file" | awk '{print $5}')
            basename_file=$(basename "$file")
            echo "      $basename_file ($size)"
        fi
    done
fi

if [ -d "$OUTPUT_DIR/demo" ]; then
    demo_count=$(find "$OUTPUT_DIR/demo" -name "*.html" 2>/dev/null | wc -l)
    echo "   📝 Demo ディレクトリ: $OUTPUT_DIR/demo/ ($demo_count ファイル)"
    for file in "$OUTPUT_DIR/demo"/*.html; do
        if [ -f "$file" ]; then
            size=$(ls -lh "$file" | awk '{print $5}')
            basename_file=$(basename "$file")
            echo "      $basename_file ($size)"
        fi
    done
else
    echo "   📝 Demo ディレクトリ: ../contents/demo/ (0 ファイル)"
fi

echo
echo "📈 統計情報:"
echo "   🎨 CSS配置成功: $css_files_copied/$css_files_total"
echo "   🔍 ScrollCast統一セレクター対応: $selector_compatible_files/$html_files_found"
echo "   📝 デモファイル生成: 0"

if [ $css_files_copied -eq $css_files_total ] && [ $selector_compatible_files -gt 0 ]; then
    echo
    echo "🎉 emotional-decoration CSS配置が完了しました！"
    echo
    echo "💡 Next steps:"
    echo "   - ScrollCast生成HTMLファイルには既にCSS参照が埋め込まれています"
    echo "   - integration_test.shで生成されたHTMLファイルをブラウザで確認"
    echo "   - テキストアニメーションと装飾が同時に適用されます"
    echo
    echo "🔧 CSS適用方法:"
    echo "   1. ScrollCast HTMLファイルの<head>内に以下を追加:"
    echo "      <link rel=\"stylesheet\" href=\"css/text-color-simple.css\">"
    echo "      <link rel=\"stylesheet\" href=\"css/scroll-cast-text-color-enhancement.css\">"
    echo "   2. ファイルを保存してブラウザで開く"
    echo "   3. .text-container と .text-line に装飾が適用される"
    echo
    echo "🎨 装飾システム特徴:"
    echo "   - CSS-Only統合（HTMLファイル編集なし）"
    echo "   - Template-Based Architecture対応"
    echo "   - 非干渉設計（ScrollCast動作保持）"
    echo "   - 統一セレクター(.text-container, .text-line)対応"
    exit 0
else
    echo
    echo "⚠️  一部の配置に失敗しました"
    echo "   - CSSファイル配置状況: $css_files_copied/$css_files_total"
    echo "   - ScrollCast対応状況: $selector_compatible_files/$html_files_found"
    echo "   - CSS階層やファイル存在確認が必要"
    exit 1
fi