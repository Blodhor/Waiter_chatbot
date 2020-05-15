# Waiter_chatbot
I'm uploading this for beginners in AI to see. This may help you!

Here I am using the sklearn libraries, so just go check them out!!

https://scikit-learn.org/stable/


Classifier_inductor.py : This program generates classifiers based on the well known algorithms Logistic Regression, Decision Tree and KNN.

  Running this will get you something like this:
  
    Running Inductor, this may take a few minutes ...
    
    8 minutes and 55.31 seconds for the Inductor to build the three classifiers
    
    Chosen classifier: Logistic Regression.
    
    Accuracy = 0.927711
    
    Precision score = 0.927711
    
    Recall score = 0.927711

    Test three intentions: (If you'd be kind, inform quantity as 'one', 'two', 'three',...since 1,2,3,... are also used to indicate a menu order.)

    Garcon! A mesa esta quebrada
    ['funcionario']
    Opa, gostaria de pedir uma agua
    ['pedido']
    quanto que devo pagar?
    ['conta']

cardapio.txt: Restaurant menu.

clienteTrain.txt: Dataset. If you'll change its format, remember to edit the conjunto_dados method from Classifier_inductor.py accordingly.

entities.txt: Menu's entities.

Taking_order.py: This program defines the methods which the AI will use to take an order and account the bill.

  Running this will get you something like this:
  
    Peça algo do cardapio
    Olá, eu gostaria de uma porção de aneis de cebola como entrada, dois tradicionais especiais e duas cocas por favor
    Pedido:ANEIS DE CEBOLA	Quantidade:1	Preço total:10.00
    Pedido:TRADICIONAIS ESPECIAIS	Quantidade:2	Preço total:30.00
    Pedido:COCA	Quantidade:2	Preço total:10.00
    Total a pagar:	50.00

Chatbot_beta.py: 


  Running this will get you something like this:
  
  Running Inductor, this may take a few minutes ...
8 minutes and 26.08 seconds for the Inductor to build the three classifiers
Chosen classifier: Logistic Regression.
Accuracy = 0.927711
Precision score = 0.927711
Recall score = 0.927711

>Seja bem vindo a hamburgueria facom, como posso ajudar?
<O que tem para hoje?
Entradas                      No  Preço

Aneis de cebolas empanados    1    10.00

Batata frita                  2    10.00

Batata rústica                3    10.00

Mandioca frita                4    10.00

Batata frita especial         5    12.00



Hambúrgueres

Kids                          6    12.00

Tradicional especial          7    15.00

Da casa                       8    15.00

Americano                     9    15.00

Frango especial               10    15.00

Frango crispy                 11    15.00

Salada especial               12    15.00

Mexicano                      13    15.00

Cordeiro                      14    20.00

Bacon premium                 15    22.00

Monstro                       16    25.00

Mignon provolone              17    25.00

Killer                        18    30.00



Sobremesas

Milk shake                    19    12.00



Bebidas

Água                          20    4.00

Citrus                        21    5.00

Água tonica                   22    5.00

Refrigerante                  23    5.00

Aquarius fresh                24    5.00

Água de coco                  25    6.00

Suco de laranja               26    7.00

Suco de abacaxi               27    7.00

Suco de maracujá              28    7.00

Heineken                      29    7.50

Budweiser                     30    7.50

Stella                        31    7.50

Eisenbanh Pilsen              32    7.50

Corona                        33    8.00

Caipirinha de limão           34    15.00

Vodka absolut dose            35    15.00

Jack Daniels dose             36    15.00

Black label dose              37    15.00

Gold label dose               38    20.00



Obs: Refrigerantes-> Coca-Cola,Fanta e Guarana

>Aqui está o cardápio! Caso esteja com dúvida em qual escolher, eu fortemente recomendo o hamburguer americano 
<Então quero dois americanos e uma corona
>Seu pedido está saindo!
<manda a conta man
>Aqui está sua conta.
Pedido:AMERICANO	Quantidade:2	Preço total:30.00
Pedido:CORONA	Quantidade:1	Preço total:8.00
Total a pagar:	38.00
<
  
