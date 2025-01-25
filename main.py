from tokenize import tokenize
from parser import parse
from eval import fun
code = '''
i = 2
while i < 100 {
	f = 1
	j = 2
	while j < i {
		if i % j == 0 {
			f = 0;
		}
		j = j + 1
	}
	if f {
		cout = i
		cout = ' '
	}
	i = i + 1
}
'''

tokens = tokenize(code) # Токенизируем код
parsed = parse(tokens) # Преобразуем токены в блоки кода
dct = {}
for i in parsed: # Исполняем все блоки кода
	fun(i, dct)
