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
