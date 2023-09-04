function shuffleTable(tbl)
    local randomIndex, tmp
    for currentIndex = #tbl, 2, -1 do
        randomIndex = math.random(currentIndex)
        tmp = tbl[currentIndex]
        tbl[currentIndex] = tbl[randomIndex]
        tbl[randomIndex] = tmp
    end
end

function loadCard(value)
	function getFileName(value)
		if (value<10) then 
			path = "img/karten/0"..value..".png"
		else
			path = "img/karten/"..value..".png"
		end
		return path
	end
	imgFile = getFileName(value)
	img = "love.graphics.newImage("..imgFile..")"
	return {
		value = value,
		img = img
	}
end

function getDeck(amount)
	cards = {}
	--check if all files are there
	for i = 1, amount do
		newCard = loadCard(i)
		table.insert(cards, newCard)
	end
	shuffleTable(cards)
	return {
		cards = cards,
		pop = function(self) 
			table.remove(self.cards, #self.cards)
			return self.cards[#cards]
		end
	}
end

function Spieler()
	karten = {}
	return {
		zeigeHandKarten = function(self)
			print("alle Spieler sehen deine Karten(2implemend)")
			for i = 1, #karten do
				print("Wert: "..karten[i].value)
				print("Bild: "..karten[i].img)
			end
		end,
		zieheKarte = function(self)
			newCard = deck:pop()
			table.insert(karten, newCard)
		end,
		werfeKarteWeg = function(self, pos)
			table.remove(karten, pos)
		end
	}

end

function foo()
	print(deck:pop())
end

local deck = getDeck(22)
local patrick = Spieler()

print("patrick zieht eine karte")
foo()
--patrick:zieheKarte()
--print("patrick zieht eine karte")
--patrick:zieheKarte()
--print("patrick zeigt seine karten")
--partrick:zeigeKarten()
--print("patrick wirft eine karte weg")
--patrick:werfeKarteWeg()
--print("patrick zeigt seine karten")
--partrick:zeigeKarten()
--
--deckCards = getDeck(22)
--print("amount of cards in the deck: "..#deckCards.cards)
--drawnCard = deckCards:pop()
--print("imgage: "..drawnCard.img)
--print("amount of cards in the deck: "..#deckCards.cards)
--drawnCard = deckCards:pop()
--print("imgage: "..drawnCard.img)
