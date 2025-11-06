import argparse
from pathlib import Path

from PIL import Image


def main(inDir, outDir, stampFile):
    """
    指定したディレクトリにある画像にスタンプ画像を合成して出力ディレクトリに出力する

    Args:
        inDir (str): 入力画像ディレクトリのパス
        outDir (str): 出力ディレクトリのパス
        stampFile (str): スタンプ画像ファイルのパス
    """
    input_dir = Path(inDir)
    output_dir = Path(outDir)
    stamp_path = Path(stampFile)

    # 入力ディレクトリの存在確認
    if not input_dir.exists():
        print(f"エラー: 入力ディレクトリが存在しません: {input_dir}")
        return

    # スタンプファイルの存在確認
    if not stamp_path.exists():
        print(f"エラー: スタンプファイルが存在しません: {stamp_path}")
        return

    # 出力ディレクトリの作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # スタンプ画像を読み込み、64x64にリサイズ
    try:
        stamp_image = Image.open(stamp_path).convert("RGBA")
        stamp_image = stamp_image.resize((64, 64), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"エラー: スタンプ画像の読み込みに失敗しました: {e}")
        return

    # サポートする画像形式
    supported_formats = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}

    # 入力ディレクトリ内の画像ファイルを処理
    processed_count = 0
    for image_file in input_dir.iterdir():
        if image_file.is_file() and image_file.suffix.lower() in supported_formats:
            try:
                # 元画像を読み込み
                base_image = Image.open(image_file).convert("RGBA")

                # スタンプの配置位置を計算（右下、16pxの余白）
                stamp_x = base_image.width - 64 - 16
                stamp_y = base_image.height - 64 - 16

                # スタンプを合成
                base_image.paste(stamp_image, (stamp_x, stamp_y), stamp_image)

                # 出力ファイルパスを生成
                output_file = output_dir / image_file.name

                # RGB形式で保存（透明度情報が不要な場合）
                if image_file.suffix.lower() in {".jpg", ".jpeg"}:
                    base_image = base_image.convert("RGB")

                # 画像を保存
                base_image.save(output_file)
                processed_count += 1
                print(f"処理完了: {image_file.name} -> {output_file.name}")

            except Exception as e:
                print(f"エラー: {image_file.name} の処理に失敗しました: {e}")
                continue

    print(f"\n処理完了: {processed_count} 枚の画像を処理しました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="指定したディレクトリにある画像にスタンプ画像を合成します。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("inDir", help="連番画像ファイルのディレクトリ")
    parser.add_argument("outDir", help="出力先のディレクトリ")
    parser.add_argument("stampFile", help="合成するスタンプ画像ファイル")

    args = parser.parse_args()

    main(args.inDir, args.outDir, args.stampFile)
