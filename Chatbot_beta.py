'''
This code gathers the intention classifier, order manager and the power of an indefinite loop to create the illusion of a
thinking virtual waiter.
'''

'''
Importing the intention classier and order manager
'''

from Classifier_inductor import Indutor
from Taking_order import card_entidade, pedidos_quantidades, conta
import random
from time import time, localtime


random.seed()

class Chatbot_atendente(Indutor):
	rec_list = []
	falta_list = []
	def __init__(self,metodo='Here will be the chosen classifier... but you can write whatever, i\'m just setting a default value because of the \'promo\' flag.', promo = False):
		self.metod = metodo
		self.entidades, self.cardapio = card_entidade()

		#Important to remember: out_of_stock and recommended lists are CLASS attributes because all clients in the restaurant are equal and deserve the same treatment. But each one asks for different dishes, so the chosen dishes' list and payment are OBJECT attributes.   
		self.pagamento = ()
		self.lista_pay = []
		self.escolhidos = []
		self.quantos = []

		#Here i'm setting this out_of_stock and recommendation as object dependent only because it's way easier to test for problems (it takes more than 8 min to do the training and sampling - with a monte carlo method)
		self.rec = self.recomend_list()
		self.faltando = self.sem_estoque()
	
		#The recommended item can not be one that is out_of_stock
		while self.rec == self.faltando:
			self.rec = self.rec_list[int(random.uniform(0,len(self.rec_list)-1))]

		#A bunch of greetings. It's just an idea to sound less robotic and more human to not greet always the same way
		self.saudacao = ['Bem-vindo, prezado cliente, a hamburgueria facom! O que gostaria de pedir hoje?','Seja bem vindo a hamburgueria facom, como posso ajudar?','Seja bem vindo a hamburgueria facom, como posso servi-lo?','Boa noite, peço desculpas com antecedência, mas extraordinariamente hoje estamos sem %s.'%self.faltando]

		#Random greeting
		self.saud_i = int(random.uniform(0,len(self.saudacao)))

		#Using this '>', '<' just to differentiate between the client and the robot, but you can try whatever (i just wanted to quickly test in the terminal and get a passing grade).
		print('>'+self.saudacao[self.saud_i])
		x_inp = input('<').lower()

		#This is the reaction method for the robot 
		self.actions(ex=x_inp, promo=promo)

	def recomend_list(self):
		'''Setting a random recommendation list with only burgers. You can go see self.cardapio[9:21].'''
		hamb = self.cardapio[9:21]
		recomend = []

		for i in hamb:
			poss = i.find('  ')
			pos = i.find(' ',poss+1,len(i))
			recomend.append(i[:pos])

		self.rec_list = recomend

		return recomend[int(random.uniform(0,len(recomend)-1))]

	def sem_estoque(self):
		'''Setting a random out of stock list with only drinks (without considering water, a restaurant without water is pretty shameful).'''
		bebis = self.cardapio[26:]
		falta = []

		for i in bebis:
			poss = i.find('  ')
			pos = i.find(' ',poss+1,len(i))
			falta.append(i[:pos])

		falta.extend(self.rec_list)
		a = falta[int(random.uniform(0,len(falta)-1))][:-1]

		while a == 'água':
			a = falta[int(random.uniform(0,len(falta)-1))][:-1]

		self.falta_list = falta

		return a

	def actions(self, ex='opa, quero um cordeiro', desconto=3, fator=0.05, promo = False):
		'''Reactions of the waiter to the sample given (I use the infinite loop 'while True' because only the client can finish the conversation).'''
		if promo:
			if localtime()[6] < 4: #setting limitation on weekdays for discounts, in Brazil is quite ordinary to have discounts from monday to thursday and everything becomes more expensive on the weekend
				desc = desconto
			while True:
				#useful to set a keyword to shut the bot up.
				if ex == 'silencio_atendente':
					break
				#i'm setting this keyword to define a new client but it's propably best to create a method that verify things for you 
				if ex == 'novo_cliente':
					# you need to reset the object attributes for every new client
					self.pagamento = ()
					self.lista_pay = []
					self.escolhidos = []
					self.quantos = []

					self.saudacao = ['Bem-vindo, prezado cliente, a hamburgueria facom! O que gostaria de pedir hoje?','Seja bem vindo a hamburgueria facom, como posso ajudar?','Seja bem vindo a hamburgueria facom, como posso servi-lo?','Boa noite, peço desculpas com antecedência, mas extraordinariamente hoje estamos sem %s.'%self.faltando]
					self.saud_i = int(random.uniform(0,len(self.saudacao)))

					print('>'+self.saudacao[self.saud_i])
					ex = input('<').lower()
					continue

				inst_text = Indutor.vectorizer.transform([ex])
				y_predito = self.metod[1].predict(inst_text)

				#I'm forcing a delay in the AI's reaction to look a bit more human
				start = time()
				while (time() - start) < 1.2:
					continue

				if y_predito == 'pedido':
					#The client is requesting something
					pedido_q = pedidos_quantidades(ent=self.entidades,exemplo=ex)
					#you need to save what was ordered
					self.escolhidos.extend(pedido_q[0])
					#you also need to save how much was ordered
					self.quantos.extend(pedido_q[1])
					#Just say anything so the client knows that everything is going fine
					print('>Seu pedido está saindo!')

				elif y_predito == 'promocao':
					#if the client say anything about promotions, discounts,...
					print('>De segunda a quinta temos uma promoção de %.1f%% de desconto em todos os pedidos!'%(desconto*fator*100))

				elif y_predito == 'funcionario':
					#if there is a problem anywhere the client will complain. Say the manager or whatever problem solver employee is on the way
					print('>Sentimos muito pelo transtorno, um funcionário está a caminho.')
					#
					# code to alert someone to go help the client (it depends on the situation of the restaurant so i didn't write anything
					#
				elif y_predito == 'cardapio':
					# just in case the random greeting wants to say hello and recommend something out of stock
					if self.saud_i == len(self.saudacao)-1:
						Indutor.cardapio(self,sem_estoque=self.faltando)
						print('>Estas são as opções de hoje, com exceção de %s. Se me permite, eu recomendaria o hamburguer %s'%(self.faltando,self.rec))
					else:
						Indutor.cardapio(self)
						#the waiter recommendation is random, don't trust it lol!
						print('>Aqui está o cardápio! Caso esteja com dúvida em qual escolher, eu fortemente recomendo o hamburguer %s'%self.rec)
				elif y_predito == 'conta':
					#if the total to pay is asked you need to show it (but don't close the tab, the client can still decide to waste more money
					print('>Aqui está sua conta.')

					self.pagamento = conta(cardapio=self.cardapio,pedidos=self.escolhidos,quantos_pedidos=self.quantos,desconto=desc,fator_desconto=fator)

				if len(self.pagamento) !=0 and [self.pagamento] != self.lista_pay:
					self.lista_pay.append(self.pagamento)
				ex = input('<').lower()
		else:
			desc = 0
			while True:
				#this part is just repeating the code with promotion, well, without giving any discounts so i'll not comment again
				if ex == 'silencio_atendente':
					break
				if ex == 'novo_cliente':
					self.pagamento = ()
					self.lista_pay = []
					self.escolhidos = []
					self.quantos = []

					self.saudacao = ['Bem-vindo, prezado cliente, a hamburgueria facom! O que gostaria de pedir hoje?','Seja bem vindo a hamburgueria facom, como posso ajudar?','Seja bem vindo a hamburgueria facom, como posso servi-lo?','Boa noite, peço desculpas com antecedência, mas extraordinariamente hoje estamos sem %s.'%self.faltando]

					self.saud_i = int(random.uniform(0,len(self.saudacao)))
					print('>'+self.saudacao[self.saud_i])
					ex = input('<').lower()
					continue

				inst_text = Indutor.vectorizer.transform([ex])
				y_predito = self.metod[1].predict(inst_text)
				
				start = time()
				while (time() - start) < 1.2:
					continue
				if y_predito == 'pedido':
					pedido_q = pedidos_quantidades(ent=self.entidades,exemplo=ex)
					self.escolhidos.extend(pedido_q[0])
					self.quantos.extend(pedido_q[1])
					print('>Seu pedido está saindo!')

				elif y_predito == 'funcionario':
					print('>Sentimos muito pelo transtorno, um funcionário está a caminho.')
					#
					# code to alert someone to go help the client
					#
				elif y_predito == 'cardapio':
					if self.saud_i == len(self.saudacao)-1:
						Indutor.cardapio(self,sem_estoque=self.faltando)
						print('>Estas são as opções de hoje, com exceção de %s. Se me permite, eu recomendaria o hamburguer %s'%(self.faltando,self.rec))

					else:
						Indutor.cardapio(self)
						print('>Aqui está o cardápio! Caso esteja com dúvida em qual escolher, eu fortemente recomendo o hamburguer %s'%self.rec)

				elif y_predito == 'conta':
					print('>Aqui está sua conta.')

					self.pagamento = conta(cardapio=self.cardapio,pedidos=self.escolhidos,quantos_pedidos=self.quantos,desconto=desc,fator_desconto=fator)

				if len(self.pagamento) !=0 and [self.pagamento] != self.lista_pay:
					self.lista_pay.append(self.pagamento)
				ex = input('<').lower()

if __name__ == "__main__":

	'''With a promotion....I didn't finished testing this'''
	#roger = Indutor(treinamento = 'clienteTrain_promo.txt')
	#metod = roger.print_classificador()
	#Mel = Chatbot_atendente(metodo=metod,promo = True)
	'''Without a promotion'''
	roger = Indutor()
	metod = roger.print_classificador() #I use this method print_classificador only to better evaluate the code.  melhor_classificador already does the job.
	Mel = Chatbot_atendente(metod)
