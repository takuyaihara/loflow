# 🎧 LoFlow プロジェクト context.md

このファイルは、LoFlow プロジェクトの設計仕様・技術要件・処理構成など、開発文脈（コンテキスト）をまとめたものです。ChatGPT などの LLM に本プロジェクトの内容を正しく伝えるために使用します。

---

## 🔰 プロジェクト目的

* AI が lo-fi BGM を自動生成・再生し続けるローカルツールを開発する
* ユーザーは `.exe` を起動するだけで使用可能
* 完全オフライン動作を前提とする

---

## 🧠 使用AIモデル

* Meta 社の MusicGen-small（MIT ライセンス）を使用
* 出力形式は 15 秒の WAV 音源
* プロンプトで BPM やリズム構造をある程度指示できる

  * 例：`lofi hip hop beat at 128 BPM, starts with a clear 4/4 rhythm, seamless, loop-ready`

---

### ⚠ 注意事項：MusicGenの拍頭制御について

MusicGen はリズム構造をある程度指示できるが、**常に1拍目から生成が始まるとは限らない**。そのため、ループ開始位置の制御は難しく、多少の拍ズレがある前提で処理・フェード設計を行っている。

---

### 🔎 補足：BPM 128 / 4小節構成を採用している理由

* 128 BPM・4拍子の1小節は約 1.875 秒
* 8小節で約 15 秒（MusicGen の最小出力長）
* 15 秒 × 4連結 = 約 60 秒の自然なループが可能
* この構成を前提にプロンプトを設計している

---

## 🔁 音楽再生方式（差し替え型ループ）

* 15秒の音源を4回連結し約60秒のMP3を生成・再生
* 再生が終了すると次の音源にキャッシュを差し替えて再生継続
* このサイクルを繰り返して無限ループ

---

## 🌀 処理フロー（非同期）

※ 非同期処理には threading.Thread を使用。生成・変換処理をバックグラウンドで順次実行する。

1. MusicGenで15秒WAVを生成
2. lameencでMP3（128kbps）に変換
3. pydubで4回連結＋2秒フェードアウト
4. pygame.mixer.musicで再生（終了検知）
5. 次音源はバックグラウンドスレッドで事前生成

---

## 🧰 使用ライブラリ

* 音声変換：lameenc
* 音声編集：pydub
* 再生制御：pygame.mixer.music
* GUI構築：Tkinter（標準・軽量・インストール不要）
* バイナリ化：PyInstaller

---

## 🖥 GUI 仕様（最小構成）

* 状態表示：再生中 / 停止中 / 生成中
* 残り時間表示（カウントダウン）
* ボタン：スタート / 一時停止 / 再生成 / 終了
* ログ表示：スクロール付きテキストエリア
* 起動時は「待機状態」から開始

---

## 📐 その他設計方針

※ 音量制御は pygame.mixer.music.set\_volume() を使用予定（0.0〜1.0 の範囲でリアルタイム調整）

* 音量スライダー：主要機能実装後に追加予定
* 設定保存（音量など）：将来的に対応
* キャッシュ削除：起動時・終了時の両方で実行
* エラー通知：通常はログ出力、致命的な場合のみポップアップ
* アプリ終了時：スレッド停止・処理中断・キャッシュ削除を確実に行う
* 配布形式：.exe 単体で GitHub Releases に配布（依存なし）

---

## 🔭 今後検討する機能（主要機能完成後）

* プロンプト手動入力切替
* MP3保存機能
* 軽量なビジュアライザ表示

---

## ✅ 現状

* 全体設計は明確かつ一貫性があり、実装可能な状態
* 曖昧な仕様はほぼなし

---

## 🧭 ChatGPT運用方針

* ChatGPT でこのプロジェクトを扱う際は、毎回メモリを初期化し、本プロジェクトの `prompt.md` を最初に読み込ませてから作業を開始すること。
* これは他プロジェクトとの文脈混在や仕様誤解を防ぎ、再現性ある支援を維持するために必須とする。

---

## ⚠️ 可変設計ポイント（検討中）

* 現在は MP3 長さを 60 秒に固定（15秒×4）
* 将来的にテンポに応じて可変長にするか検討中

---

## 🧹 開発支援ツール設定（フォーマッター / リント / 型チェック / Copilot）

* **フォーマッター**：`black`

  * VSCode 設定で `editor.defaultFormatter` に `ms-python.black-formatter` を指定
  * `editor.formatOnSave = true` により保存時自動整形

* **リント**：`Ruff`

  * `ruff.enable = true`
  * Windows 専用設定：`ruff.path = ["${workspaceFolder}/venv/Scripts/ruff.exe"]`

* **型チェック**：`mypy-type-checker` 拡張（[matangover.mypy-type-checker](https://marketplace.visualstudio.com/items?itemName=matangover.mypy-type-checker)）

  * `mypy-type-checker.preferDaemon = false`
  * `mypy-type-checker.reportingScope = "workspace"`

* **GitHub Copilot Pro**：導入済み

  * 拡張機能：`GitHub Copilot` + `GitHub Copilot Chat`
  * チャットモードは通常チャット（Edit）を常用
  * 左メニューにはアイコン非表示。`Ctrl+Alt+I` で起動
  * Copilot の出力は ChatGPT でレビューして補完
