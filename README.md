# PagodeLang

Essa é a PagodeLang, a linguagem inspirada na linguagem Panic! Onde você pode escrever seu código como uma música romântica de pagode!


## Exemplo de uma calculadora da sequência de Fibonacci em PagodeLang

```
Ela é Perfeita demais! Fulana é uma Perfeita!
Comentei dela com meus amigos
Fulana é Gatinha demais!
se Gatinha me ama menos que eu amo ela , então tchau, senão
Fulana é uma Gatinha sem igual! e Fulana é uma Gatinha sem por defeito!
```


## Gramática
```
start : func+

?expr : "se" op ", então" op ", senão" expr -> cond
      | op

?op   : bit_or

?bit_or  : bit_or "|" bit_and
         | bit_and

?bit_and : bit_and "&" cmp
         | cmp

?cmp   : arith "me ama menos que" arith  -> lt
       | arith "me ama mais que" arith  -> gt
       | arith "como" arith  -> eq
       | arith

?arith : arith "e" term  -> add
       | arith "sem" term  -> sub
       | term

?term  : term "vezes" value  -> mul
       | term "dividido por" value  -> div
       | value

?value : NAME
       | INT
       | call
       | "(" expr ")"

call  : NAME "é uma" args "!"

args  : expr ("," expr)*

func  : NAME "é" argn  "demais!" expr
argn  : NAME ("," NAME)*


%ignore /\n/
NAME  : /(?!\d)[A-Z]\w+/
INT   : /[^\n][\w\s]+/
OP    : /[-+*\/<>=&|]/
%ignore /\s+/
%ignore /Comentei[^\n]*/
```


## Explicação

NAMEs são palávras que começãm com letra maíscula, e INTs são representados por um conjunto de palavras com letra minúscula, onde o valor do inteiro será a quantidade de palvras.
Ex: isso seria um inteiro = 4 palavras, então representa o número 4
Para representar o zero usamos a palavra reservada "nenhum"


Para fazer comentários, basta começar a linha com a palavra Comentei
