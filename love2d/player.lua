Spieler()
    AnzahlAnKarten
    Karten [] = anzahlAnKarten * Karte()
    def zeigeHandKarten
    def zieheKarte
    def werfeKarteWeg

function Player()
	cards = {}
	function drawMaxCards()
		nowAmount = nil
		if next(myTable) == nil then
			nowAmount = 0
		else
			nowAmount = #cards
		end
		for i = nowAmount, 4 do
			drawCard()
		end
		table.insert(cards, drawCard())
	function drawCard()
		return deck.pop()
	end
	function throwCard(pos)

	end
end
