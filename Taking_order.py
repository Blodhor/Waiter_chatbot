'''
This is a string manipulator code, so if you change the structure of the menu (cardapio.txt) or the entity file, this will be useless.

The main objective of this code is to correctly save info about an order from a client and to manage the bill. In summary, it's just a method for the AI to perform based on what intention it thinks the client has, i.e., if the client asks for the bill the AI will acess the info made here and saved somewhere (probably an object attribute) and use the code here to calculate the final price to pay.


This code was built to work with portuguese, if you'll be using another language for your waiter and don't know what to do, i translated to english the comments on this file to help you understand what was done.
'''

'''
It is really important to use the deepcopy method since python always treat variables' names as pointers. If you know another programming language like C or Java, you know what kind of undesirable mess you can make with pointers and temporary structures.
'''
import os
from copy import deepcopy as dcpy

def card_entidade(arq_entidade='entities.txt', arq_cardapio='cardapio.txt'):
	'''Stores the entity file in a dictionary and the menu in a vector. Returning the tuple (entities, menu)'''
	ent = open(arq_entidade,'r')
	info_ent = os.stat(arq_entidade)
	entidades = {}

	card = open(arq_cardapio,'r')
	info_card = os.stat(arq_cardapio)
	cardapio =[]

	#entities
	temp_ent = ent.readline().lower()
	while ent.tell() != info_ent.st_size:
		t_ent = temp_ent.split(':')
		entidades[t_ent[0]] = t_ent[1][:-1].split(',')
		temp_ent = ent.readline().lower()
	#as temo_ent updates at the end of the loop, the 'while' does not do the last iteration
	t = temp_ent.split(':')
	entidades[t[0]] = t[1][:-1].split(',')
	ent.close()

	#I do not use the command 'readlines()' to read the entire file, as this way the code would be case sensitive (which is undesirable)

	t_card = card.readline().lower()
	while card.tell() != info_card.st_size:
		cardapio.append(t_card)
		t_card = card.readline().lower()
	card.close()

	return (entidades,cardapio)

def pedidos_quantidades(ent={'sobremesa': ['milk shake'], 'num': ['um', 'uma'], 'hamburguer': ['kids', 'tradicional especial'], 'pedido': ['1', '2'], 'bebida': ['\xc3\xa1gua', 'citrus'], 'entrada': ['aneis de cebola', 'batata frita']}, exemplo='quero uma citrus, por favor'):
	'''String comparator. Checks which entities the example presents and returns the order tuple with its quantity (dishes, how many dishes)'''
	entidades = dcpy(ent)
	dic = entidades['num']
	del entidades['num']
	pedidos = []
	pedidos_qt = []

	for i in entidades:
		if entidades[i] != [entidades[i][0]] and i != 'pedido':
			#more than one choice
			#there may be ambiguous dishes, eg. french fries, special french fries.
			ambiguos = []
			
			for j in range(0,len(entidades[i])):
				for jj in range(j+1,len(entidades[i])):
					if entidades[i][j] in entidades[i][jj] and entidades[i][jj] in exemplo:
						amb_pos=exemplo.find(entidades[i][jj],0,len(exemplo))
						ambiguos.append((entidades[i][j],entidades[i][jj],amb_pos,[False]))

						# AND IF THE CLIENT ASKED J AND JJ
						ex_temp = exemplo[:amb_pos]+exemplo[amb_pos+len(entidades[i][jj]):]
						if entidades[i][j] in ex_temp:
							pos_dupla = ex_temp.find(entidades[i][j])
							if pos_dupla < amb_pos:
								ambiguos[len(ambiguos)-1] = (entidades[i][j],entidades[i][jj],amb_pos,[True,pos_dupla])
							else:
								ambiguos[len(ambiguos)-1] = (entidades[i][j],entidades[i][jj],amb_pos,[True,pos_dupla+len(entidades[i][jj])])
					elif entidades[i][jj] in entidades[i][j] and entidades[i][j] in exemplo:
						amb_pos=exemplo.find(entidades[i][j],0,len(exemplo))
						ambiguos.append((entidades[i][jj],entidades[i][j],amb_pos,[False]))

						# AND IF THE CLIENT ASKED J AND JJ
						ex_temp = exemplo[:amb_pos]+exemplo[amb_pos+len(entidades[i][j]):]
						if entidades[i][jj] in ex_temp:
							pos_dupla = ex_temp.find(entidades[i][jj])
							if pos_dupla < amb_pos:
								ambiguos[len(ambiguos)-1] = (entidades[i][jj],entidades[i][j],amb_pos,[True,pos_dupla])
							else:
								ambiguos[len(ambiguos)-1] = (entidades[i][jj],entidades[i][j],amb_pos,[True,pos_dupla+len(entidades[i][j])])

			for j in entidades[i]:
				ambiguidade = False
				pos_j = 'none'
				if len(ambiguos)>0:
					for auxiliar in ambiguos:
						if j == auxiliar[0]:
							if not auxiliar[3][0]:
								#'j' is ambiguous but has not been asked
								ambiguidade = True
								amb_problem = False
								break
							else:
								#'j' is in ambiguous; both 'j' and his ambiguous match were asked
								pos_j = auxiliar[3][1]
								ambiguidade = True
								amb_problem = True
								break
				if ambiguidade and not amb_problem:
					continue
				if j in exemplo:
					pedidos.append( j ) #order added, below we check the quantity
					if pos_j == 'none':
						pos = exemplo.find(j)
					else:
						pos = pos_j

					#largest size of numeral (one to ten in portuguese) in characters: = 'quatro' (size: 6), with space we must then look up to 7 characters before 'j' to find out how many were ordered
					volta = pos-7
					if i in exemplo[:pos]:
						volta -= len(i)+2
						if volta <0:
							volta = 0

					if i == 'entrada':
						# if the client order a starter dish and another dish (this 'porção' is a way to ask for dishes like fries in portuguese)
						if 'porção' in exemplo[:pos] or 'porções' in exemplo[:pos]:
							volta -= 10

					if i == 'bebida':
						if 'dose de' in exemplo[:pos] or 'doses de' in exemplo[:pos]:
							volta -= 11

					if volta <0:
						volta = 0

					qtdefault = True
					if i in exemplo[volta:pos] and volta != 0:
						volta -= len(i) + 4
						if volta < 0:
							volta = 0

					for k in dic:
						if k in exemplo[volta:pos]:
							qtdefault = False
							pedidos_qt.append(k)
							break

					if qtdefault:
						pedidos_qt.append('um')

		elif entidades[i] != [entidades[i][0]]:
			#if it was asked for example: 'dois numero 1'(two number 1). We have to go back up to 14 characters
			numeros_no_exemplo = []
			for j in entidades[i]:
				if j in exemplo:
					#finds all numbers in the order in a redundant way (ex: in '12' there is '1', '2' and '12')
					numeros_no_exemplo.append(j)

			for j in range(0,len(numeros_no_exemplo)):
				#if you find redundant numbers, ignore the smaller ones (these cases only occur when there is a number greater than or equal to '10')
				if numeros_no_exemplo[j] == '*':
					continue

				for jj in range(j+1,len(numeros_no_exemplo)):
					if numeros_no_exemplo[jj] == '*':
						continue

					if numeros_no_exemplo[j] in numeros_no_exemplo[jj]:
							numeros_no_exemplo[j] = '*'

					elif numeros_no_exemplo[jj] in numeros_no_exemplo[j]:
							numeros_no_exemplo[jj] = '*'

			for j in numeros_no_exemplo:
				if j != '*':
					pedidos.append( j ) #order added, below we check the quantity
					pos = exemplo.find(j)
					volta = pos-14
					if volta <0:
						volta = 0

					qtdefault = True
					if i in exemplo[volta:pos] and volta != 0:
						volta -= len(i) + 4
						if volta < 0:
							volta = 0

					for k in dic:
						if k == 'um':
							if 'numero' in exemplo[volta:pos] or 'número' in exemplo[volta:pos]:
								pos -= 6

						if k in exemplo[volta:pos]:
							qtdefault = False
							pedidos_qt.append(k)
							break

						if k=='um':
							pos += 6

					if qtdefault:
						pedidos_qt.append('um')
		else:
			#type of food with unique option
			if entidades[i][0] in exemplo:
				pedidos.append( entidades[i][0] ) #order added, below we check the quantity
				pos = exemplo.find(entidades[i][0])
				volta = pos-7
				if volta <0:
					volta = 0
				qtdefault = True
				if i in exemplo[volta:pos] and volta != 0:
					volta -= len(i) + 4
					if volta < 0:
						volta = 0

				for k in dic:
					if k in exemplo[volta:pos]:
						qtdefault = False
						pedidos_qt.append(k)
						break

				if qtdefault:
					pedidos_qt.append('um')

	#translating the amount to facilitate creating the bill
	tradutor_num = {'um,uma':1, 'dois,duas':2, 'três,tres':3, 'quatro':4, 'cinco':5, 'seis': 6, 'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10}
	numb_ped = []
	for cc in pedidos_qt:
		for i in tradutor_num:
			if cc in i:
				numb_ped.append(tradutor_num[i])
				break

	return (pedidos,numb_ped)

def conta(cardapio=[],pedidos=['da casa'],quantos_pedidos=[8],desconto=0,fator_desconto=0.05):
	'''Calculates the bill and returns the tuple: (Total, CostList).'''
	plural_letras = ['ais','os','as','ns']
	pagar = []

	for ped in pedidos:
		if ped in 'coca, coca-cola, fanta, guarana':
			ped = 'refrigerante'

		for i in range(len(cardapio)):
			if ped in cardapio[i]:
				pri = cardapio[i].split()
				pagar.append(pri[len(pri)-1])
				break

			#if the order is not on this menu line, it is possible that we are dealing with a plural dish name 
			for plu in plural_letras:
				if plu in ped:
					pos = ped.find(plu)
					tt = ped[:pos+1]
					if tt in cardapio[i]:
						pri = cardapio[i].split()
						pagar.append(pri[len(pri)-1])
						break
	conta_p = []
	total_conta = 0.0

	for i in range(len(pagar)):
		item_i = float(pagar[i])*quantos_pedidos[i]
		conta_p.append( item_i)
		total_conta += item_i

	if desconto > 6:
		desconto = 6 #maximum value would be for example 30% discount with the default factor, because 'desconto'*'fator_desconto' = 6 * 5%

	tot_conta = (1 - desconto*fator_desconto)*total_conta

	#prints bill
	lista_pagamento = []

	for i in range(len(quantos_pedidos)):
		lista_pagamento.append((pedidos[i].upper(), quantos_pedidos[i], conta_p[i]))

	for i in lista_pagamento:
		print('Pedido:%s\tQuantidade:%d\tPreço total:%.2f'%(str(i[0]),i[1],i[2]))

	if tot_conta-total_conta !=0:
		print('Desconto:\t%.2f'%(tot_conta-total_conta))

	print('Total a pagar:\t%.2f'%tot_conta)

	return (total_conta,lista_pagamento)

if __name__ == "__main__":
	tst = input('Peça algo do cardapio\n').lower()
	#Testing. "Order something from the menu". eg.Olá, eu gostaria de uma porção de aneis de cebola como entrada, dois tradicionais especiais e duas cocas por favor
	entidades, cardapio = card_entidade()
	escolhidos, quantos = pedidos_quantidades(ent=entidades,exemplo=tst)
	pagamento = conta(cardapio,escolhidos,quantos)
