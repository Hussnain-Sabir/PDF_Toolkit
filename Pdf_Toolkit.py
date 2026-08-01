from pathlib import Path
from PIL import Image
from pypdf import PdfReader,PdfWriter

path=Path.home() /  "Testing_Project"            
# path=input("Enter the folder path: ")
# path = Path(path.strip().replace("'","")).expanduser()



def image_to_PDF(path):
    valid_extensions=(".jpg",".jpeg",".png",".webp")

    print("Converting into PDFs ...................")
    Target_directory= path / "IMG_to_PDF"
    Target_directory.mkdir(exist_ok=True)

    convert=[]
    
    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() in valid_extensions:
                with Image.open(item) as img:
                    img=img.convert("RGB")
                    convert.append(img)


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
    Target_directory= path / "Merged_PDFs"
    Target_directory.mkdir(exist_ok=True)

    convert=[]

    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() == ".pdf":
                convert.append(item)

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

    Target_Directory= path / "Merged_All"
    Target_Directory.mkdir(exist_ok=True)

    convert=[]

    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() in (valid_extensions + (".pdf",)):
                convert.append(item)

    if convert:
        convert= sorted(convert)
        hidden_directory= Target_Directory / ".temp_pdfs"
        hidden_directory.mkdir(exist_ok=True)

        merger= PdfWriter()

        for item in convert:
            if not item.suffix.lower() in valid_extensions:
                merger.append(item)
            else:
                with Image.open(item) as img:
                    img=img.convert("RGB")
                    temp_path=hidden_directory / "temp_pdf.pdf"
                    img.save(temp_path)
                    merger.append(temp_path)

        Output_path= Target_Directory / "Merged_All.pdf"
        i=1
        while Output_path.exists():
            Output_path= Target_Directory / f"Merged_All_{i}.pdf"
            i+=1

        merger.write(Output_path)
        merger.close()
        print(f"IMGs & PDFs are Merged -> Saved to: {Target_Directory.name} Folder....")
    else:
        print("No valid IMGs & PDFs found for conversion!")
        



if path.exists():
    IMG_merge_PDF(path)
else:
    print(f"Path does not exits!: {path}")
