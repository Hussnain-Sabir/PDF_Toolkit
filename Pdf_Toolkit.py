#!/usr/bin/env python3         # this is for linux and mac only to access the script from terminal directly
from pathlib import Path
import shutil
from PIL import Image
from pypdf import PdfReader,PdfWriter


def Image_to_PDF(path):
    print("Converting into PDFs ...................")

    valid_extensions=(".jpg",".jpeg",".png",".webp")
    Target_directory = path / "IMG_to_PDF"

    if not Target_directory.exists():
        parent_check = path.parent / "IMG_to_PDF"
        if parent_check.exists():
            Target_directory = parent_check
        else:
            Target_directory.mkdir()

    convert=[]
    
    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() in valid_extensions:
                with Image.open(item) as img:
                    img=img.convert("RGB")
                    convert.append(img)

    print(f"Found {len(convert)} files")

    if convert:
        Output_path= Target_directory / "Merged_files.pdf"
        i=1
        while Output_path.exists():
            Output_path= Target_directory / f"Merged_files_{i}.pdf"
            i+=1

        convert[0].save(Output_path, save_all=True, append_images=convert[1:])
        print(f"Conversion Completed -> Saved to: {Target_directory.name} Folder....")
    else:
        print("No valid images found for conversion!")


def PDFs_Merger(path):
    print("Merging PDFs ...................")

    Target_directory = path / "Merged_PDFs"

    if not Target_directory.exists():
        parent_check = path.parent / "Merged_PDFs"
        if parent_check.exists():
            Target_directory = parent_check
        else:
            Target_directory.mkdir()

    convert=[]

    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() == ".pdf":
                convert.append(item)

    print(f"Found {len(convert)} files")

    if convert:
        convert=sorted(convert)
        merger= PdfWriter()

        Output_path= Target_directory / "Merged_files.pdf"
        i=1
        while Output_path.exists():
            Output_path= Target_directory / f"Merged_files_{i}.pdf"
            i+=1

        for item in convert:
            merger.append(item)

        merger.write(Output_path)
        merger.close()
        print(f"PDFs Merged -> Saved to: {Target_directory.name} Folder....")
    else:
        print("No valid PDFs found for conversion!")


def IMG_merge_PDF(path):
    print("Merging Images & PDFs ...................")

    valid_extensions=(".jpg",".jpeg",".png",".webp")
    Target_directory = path / "Merged_All"

    if not Target_directory.exists():
        parent_check = path.parent / "Merged_All"
        if parent_check.exists():
            Target_directory = parent_check
        else:
            Target_directory.mkdir()

    convert=[]

    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() in (valid_extensions + (".pdf",)):
                convert.append(item)

    
    print(f"Found {len(convert)} files")

    if convert:
        convert= sorted(convert)
        hidden_directory = Target_directory / ".temp_pdfs"
        hidden_directory.mkdir(exist_ok=True)

        Output_path= Target_directory / "Merged_All.pdf"
        i=1
        while Output_path.exists():
            Output_path= Target_directory / f"Merged_All_{i}.pdf"
            i+=1

        merger= PdfWriter()

        for item in convert:
            if not item.suffix.lower() in valid_extensions:
                merger.append(item)
            else:
                with Image.open(item) as img:
                    img=img.convert("RGB")
                    temp_path = hidden_directory / f"{item.stem}.pdf"
                    img.save(temp_path)
                    merger.append(temp_path)

        merger.write(Output_path)
        merger.close()
        if hidden_directory.exists():
            shutil.rmtree(hidden_directory)
        print(f"IMGs & PDFs are Merged -> Saved to: {Target_directory.name} Folder....")
    else:
        print("No valid IMGs & PDFs found for conversion!")


def PDF_Compressor(path, target_mb=4):
    print("Compressing PDF ...................")

    Target_directory = path.parent / "Compressed_PDFs"

    if not Target_directory.exists():
        parent_check = path.parent.parent / "Compressed_PDFs"
        if parent_check.exists():
            Target_directory = parent_check
        else:
            Target_directory.mkdir()

    if path.is_file() and path.suffix.lower() == ".pdf":
        original_size = path.stat().st_size
        target_bytes = target_mb * 1024 * 1024

        Output_path = Target_directory / f"{path.stem}_compressed.pdf"
        i = 1
        while Output_path.exists():
            Output_path = Target_directory / f"{path.stem}_compressed_{i}.pdf"
            i += 1

        quality_levels = [
            (80, 1.0),
            (60, 1.0),
            (40, 0.8),
            (25, 0.7),
            (15, 0.6),
            (10, 0.5),
        ]
        best_size = None

        for quality, scale in quality_levels:
            reader = PdfReader(path)
            writer = PdfWriter()

            for page in reader.pages:
                added_page = writer.add_page(page)
                added_page.compress_content_streams()

                try:
                    images = list(added_page.images)
                except Exception:
                    images = []

                for img in images:
                    try:
                        pil_img = img.image
                        if scale < 1.0:
                            new_size = (
                                max(1, int(pil_img.width * scale)),
                                max(1, int(pil_img.height * scale)),
                            )
                            pil_img = pil_img.resize(new_size, Image.LANCZOS)
                        img.replace(pil_img, quality=quality)
                    except Exception:
                        pass

            if hasattr(writer, "deduplicate_identical_objects"):
                writer.deduplicate_identical_objects()

            writer.write(Output_path)
            writer.close()

            best_size = Output_path.stat().st_size

            if best_size <= target_bytes:
                break

        print(f"Tried {target_mb}MB, Final achieved = {best_size / (1024 * 1024):.2f} MB -> Saved to: {Output_path.name}")
    else:
        print("Path is not a valid PDF file!")



         


print("Select an option to proceed: ")
print("1. Convert Images to PDF")
print("2. Merge PDFs")
print("3. Merge Images & PDFs together")
print("4. Compress a PDF")

choice = input("Enter choice (1-4): ").strip()

if choice in ("1", "2", "3"):
    path = input("Enter the folder path (press Enter to use current folder): ").strip()
    path = Path(path.replace("'", "")).expanduser() if path else Path.cwd()

    if not path.exists():
        print(f"Path does not exits!: {path}")
    elif not path.is_dir():
        print(f"Path is not a folder!: {path}")
    else:
        if choice == "1":
            Image_to_PDF(path)
        elif choice == "2":
            PDFs_Merger(path)
        elif choice == "3":
            IMG_merge_PDF(path)

elif choice == "4":
    path = input("Enter the PDF file path: ")
    path = Path(path.strip().replace("'", "")).expanduser()

    if not path.exists():
        print(f"Path does not exits!: {path}")
    elif not path.is_file() or path.suffix.lower() != ".pdf":
        print(f"Path is not a valid PDF file!: {path}")
    else:
        target = input("Enter target size in MB (default 4): ").strip()
        try:
            target_mb = float(target) if target else 4
        except ValueError:
            print("Invalid number, using default 4MB")
            target_mb = 4
        PDF_Compressor(path, target_mb)

else:
    print("Invalid choice!")