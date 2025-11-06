# img2mp4

指定したディレクトリ内の画像にスタンプ画像を合成します。開発時に uv コマンドを使用しているため、ドキュメント上 uv が前提のようになっていますが、Python スクリプトとしても実行可能です。

## 使い方

```bash
$ uv run main.py <inDir> <outDir> <stampPath>
```

## 環境構築

```bash
$ uv init  --app
$ uv add --link-mode=copy ruff
$ uv add --link-mode=copy pillow
```

## ライセンス

MIT License
