from pathlib import Path
from PIL import Image

# path=Path.home() /  "Testing_Project"            
path=input("Enter the folder path: ")
path = Path(path.strip().replace("'","")).expanduser()



def image_to_PDF(path):
    valid_extension=(".jpg",".jpeg",".png",".webp")

    print("Converting into PDFs ...................")
    Target_directory= path / "IMG_to_PDF"
    Target_directory.mkdir(exist_ok=True)

    convert=[]
    
    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() in valid_extension:
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
        print("No valid images found for conversion")



def PDFs_Merger(path):



    convert=[]

    for item in path.iterdir():
        if item.is_file():
            if item.suffix.lower() == ".pdf":
                convert.append(item.name)

    print(convert)






if path.exists():
    image_to_PDF(path)
else:
    print(f"Path does not exits!: {path}")
