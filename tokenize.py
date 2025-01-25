import re
def tokenize(code):
	patterns = [
		('\\\'((\\\\[rnt\\\\\\\'])|(\\\\x([\\dabcdef]{2}))|(\\\\u([\\dabcdef]{4}))|([^\\n\\\'\\\\]))*\\\'', 'STRING_1'),
		('"((\\\\[rnt\\\\"])|(\\\\x([\\dabcdef]{2}))|(\\\\u([\\dabcdef]{4}))|([^"\\n\\\\]))*"', 'STRING_2'),
		('while\\b', 'WHILE'),
		('if\\b', 'IF'),
		('else\\b', 'ELSE'),
		('\\(', 'LEFT_C'),
		('\\)', 'RIGHT_C'),
		('\\{', 'LEFT_X'),
		('\\}', 'RIGHT_X'),
		('\\[', 'LEFT_I'),
		('\\]', 'RIGHT_I'),
		('<=', 'LE'),
		('>=', 'GE'),
		('<', 'LT'),
		('>', 'GT'),
		('==', 'EQ'),
		('!=', 'NE'),
		('\\+', 'ADD'),
		('-', 'SUB'),
		('\\*', 'MUL'),
		('\\/', 'DIV'),
		('%', 'MOD'),
		('=', 'ASSIGN'),
		
		('\\d*\\.\\d+', 'FLOAT'),
		('\\d+', 'INT'),

		('[a-zA-Z\\d_$]+', 'VARIABLE'),

		(',', 'SEP_1'),
		(';', 'SEP_2'),
		('#[^\r\n]+', 'COMMENT'),
		('[ \\t\\r\\n]+', 'COMMENT1')
	]
	
	regex = re.compile('|'.join(f'(?P<{name}>{pattern})' if name else pattern for pattern, name in patterns))
	
	tokens = []
	for match in regex.finditer(code):
		kind = match.lastgroup
		if kind != None:
			value = match.group(kind)
			if kind == 'INT':
				tokens.append(('expression', 'int', int(value)))
			elif kind == 'FLOAT':
				tokens.append(('expression', 'float', float(value)))
			elif kind == 'STRING_1' or kind == 'STRING_2':
				tokens.append(('expression', 'string', eval(value)))
			elif kind == 'STRING_1' or kind == 'STRING_2':
				tokens.append(('expression', 'string', eval(value)))
			elif kind == 'NULL':
				tokens.append(('expression', 'null', None))
			elif kind in [
			'WHILE', 'IF', 'ELSE', 'ASSIGN', 'LEFT_C', 'RIGHT_C', 'SEP_1', 'LEFT_X', 
			'RIGHT_X', 'SEP_2', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'LEFT_I',
			'RIGHT_I'
			]:
				tokens.append(('token', kind))
			elif kind == 'VARIABLE':
				tokens.append(('variable', value))
	return tokens
