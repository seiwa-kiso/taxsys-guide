# TaxSys 業務活用ガイド

TaxSys標準機能と、社内開発Chrome拡張機能「MF業務サポート」に含まれるTaxSys向け機能を区別して紹介する静的HTMLガイドです。

## 内容
- OCR出力結果の仕訳の展開、表示幅調整、ルール適用済み行の表示切替
- MF/MJSの元帳CSVを使う仕訳ルール入力補助
- Chrome拡張機能の導入・更新、トラブル対応、業務フロー
- 機能検索、カテゴリ切替、更新履歴

## GitHub Pages 公開手順（初回のみ）
1. GitHubの `seiwa-kiso` アカウントで `https://github.com/new` を開きます。
2. Repository name は `taxsys-guide` とし、**Public** でリポジトリを作成します。顧問先データ等はアップロードしないでください。
3. リポジトリの `Add file` → `Upload files` から、このフォルダの `index.html` と `README.md` をアップロードし、`Commit changes` を押します。**ZIPファイルをそのままアップロードしないでください。**
4. リポジトリの `Settings` → `Pages` を開きます。
5. `Build and deployment` の `Source` を `Deploy from a branch` に設定します。
6. Branch を `main`、フォルダを `/(root)` に設定して `Save` を押します。
7. GitHub Pagesのデプロイ完了後、`https://seiwa-kiso.github.io/taxsys-guide/` にアクセスして検索とカテゴリ切替を確認します。

※ GitHubの画面や権限設定により表示が異なる場合があります。公開URLは設定完了前には有効とは限りません。

## 更新方法
GitHub上の `index.html` を更新すると、Pagesの再デプロイによってサイトにも反映されます。拡張機能に変更があった場合は、`mf-extension` 側の該当ファイルの差分を確認したうえで、実装内容と実機確認状況を分けて反映してください。

## 情報管理
公開GitHub Pagesは、原則としてインターネット上の誰でも閲覧できます。顧問先名・金融機関名・口座番号・金額・取引先名・実際の仕訳・証憑や認証情報を掲載しないでください。個別画面のスクリーンショットや動画は、黒塗り・ダミー化したうえで確認してから追加してください。

## 確認元
`seiwa-kiso/mf-extension` の `manifest.json`、`taxsys-journal-expand.js`、`taxsys-rule-assist.js` （2026-11-13確認）。ソースコードの存在と実機動作確認は異なります。

## TaxSys公式アップデート同期（追加）
- 情報源: https://docs.taxsys.so-labo.co.jp/releases
- 公式発表の予定は原則 **隔週木曜日**（基準: 2026-11-12）。次回 2026-11-26、12-10、12-24、2027-01-07、01-21。
- `.github/workflows/taxsys-releases.yml` は毎週木曜20:00 JSTと金曜08:00 JSTに起動し、Pythonが隔週の該当週だけ処理します。GitHubのスケジュール実行は遅延・欠落する場合があります。
- 公式ページを読み、バージョン・公開日・公式の要約・詳細リンクを `releases.json` に保存します。変更がある場合だけcommit/pushされ、GitHub Pagesに反映されます。
- **AIによる操作手順の生成、実機での動作確認、既存の手動ガイド本文の書換えはしません。** 推測の操作手順を自動公開しないための仕様です。
- 日程変更・臨時更新時は GitHub の `Actions` → `TaxSys release guide sync` → `Run workflow` で手動実行できます。
- GitHub repository `Settings` → `Actions` → `General` で Workflow permissions を **Read and write permissions** にしてください。管理者設定で権限変更不可の場合、PAT等の権限設計が別途必要です。
- 上記ファイル3点 (`scripts/`, `.github/workflows/`, `releases.json`) も含めて **ZIP解凍後の中身を** GitHubへアップロードしてください。`releases.json` は初回実行後に生成されます。
- エラー時にはActionsログを確認してください。仕様変更で抽出に失敗した際はファイルを上書きせずエラーにします。
