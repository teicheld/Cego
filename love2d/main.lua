local images
local myTable = {}

function love.load()
	for i = 1, 22 do
		if (i<10) then
			myTable[i] = "img/karten/0"..i..".png"
		else
			myTable[i] = "img/karten/"..i..".png"
		end
	end
	image = love.graphics.newImage(myTable[3])
	for index, value in ipairs(myTable) do
		print(value)
	end
end

function love.draw()
	x = 0
	y = 0
	rotation = 0
	scaleX = 0.5
	scaleY = scaleX
	love.graphics.draw(image, x, y, 0, scaleX, scaleY)
end

function love.keypressed(key, scancode, isrepeat)
   if key == "escape" then
	love.event.quit()
   end
end
