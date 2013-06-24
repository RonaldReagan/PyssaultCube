from PIL import ImageEnhance, ImageOps

def blacknwhite(im,arg):
	return ImageOps.grayscale(im)

def saturate(im,arg):
	converter = ImageEnhance.Color(im)
	return converter.enhance(0.5)