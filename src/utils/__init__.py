from os import path, getenv

filesPath = path.join(path.dirname(path.abspath(__file__)), "Files")
imagesPath = path.join(path.dirname(path.abspath(__file__)), "Images")
fiat = getenv("FIAT")
integrityKey = getenv("INTEGRITY_KEY")