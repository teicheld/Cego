function Karte(value, path2img)
img = "love.graphics.newImage(path2img)"
	return {
		value = value,
		img = img
	}
end

karte1 = Karte(4, "01.png")
print(karte1["value"])
print(karte1["img"])
