local images = {}
local x = 300
local y = 400
local imageWidth = nil
local imageHeight = nil
local imageXcenter = nil
local imageYcenter = nil
local handPosX = nil

function Player()
	cards = {}
	function drawCard()
		
	end
	function throwCard(pos)

	end
end

function Karte()

end

function Deck()

end


function getXhandCards(distance)
	-- fills an table of 4 elements and returns it
	local xPos = {}
	xPos[1] = -1 * (distance /2 + distance) + x
	for i = 2, 4 do
		xPos[i] = xPos[i-1] + distance
	end
	return xPos
end

function love.load()
	for i = 1, 22 do
		if (i<10) then
			images[i] = love.graphics.newImage("img/karten/0"..i..".png")
		else
			images[i] = love.graphics.newImage("img/karten/"..i..".png")
		end
	end
	imageWidth = images[1]:getWidth()
	imageHeight = images[1]:getHeight()
	imageXcenter = imageWidth / 2
	imageYbutton = imageHeight
	handPosX = getXhandCards(25)
end

function love.draw()
	displayHand()
end

function displayHand()
	scaleX = 0.3
	scaleY = scaleX
	rotation = math.rad(-45)
	for i = 1, 4 do
		print(rotation)
		love.graphics.draw(images[i], handPosX[i], y, rotation, scaleX, scaleY, imageXcenter, imageYbutton)
		rotation = rotation + math.rad(30)
	end
end

function love.keypressed(key)
   if key == "escape" then
	love.event.quit()
   end
end
