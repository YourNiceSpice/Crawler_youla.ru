import re

def seller_or_not(text):
	pattern = r"размеры|распродажа|Доставка|расцветки|звоните|профиле|профиль|фото|фотографии|примерка|примерки|примерку|пишите|Оплата|гаратния"  #Ignorecae сюда же втащить
	re.IGNORECASE
	if re.search(pattern,text,re.IGNORECASE):
		return True
	else:
		return False



if __name__== '__main__':
	
	text2='Раьствием привезем 2 размера на примерку, либо 2 расцветки на выбор.'
	text3='Эко-кожа / Размер - 43 носил один раз Покупал за 80€'
	text4='Лето Размеры с 41 До 45'			

	print(seller_or_not(text2))
	print(seller_or_not(text3))
	print(seller_or_not(text4))	