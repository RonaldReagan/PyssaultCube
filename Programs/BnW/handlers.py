from PIL import ImageEnhance

def blacknwhite(im,arg):
	return im.convert('LA').convert('RGBA')

def saturate(im,arg):
	#May partially remove transparency.
	converter = ImageEnhance.Color(im)
	return converter.enhance(arg)