def parse(tokens):
	# Функция преобразовывает токены в синтаксическое дерево

	# * / %
	for i in range(len(tokens) - 2):
		if tokens[i][0] == 'expression' and tokens[i + 2][0] == 'expression' and tokens[i + 1][0] == 'token' and\
		tokens[i + 1][1] in ['MUL', 'DIV', 'MOD']:
			return parse(
				tokens[:i] + 
				[('expression', tokens[i + 1][1], tokens[i], tokens[i + 2])] + 
				tokens[i + 3:]
			)

	# + -
	for i in range(len(tokens) - 2):
		if tokens[i][0] == 'expression' and tokens[i + 2][0] == 'expression' and tokens[i + 1][0] == 'token' and\
		tokens[i + 1][1] in ['ADD', 'SUB']:
			return parse(
				tokens[:i] + 
				[('expression', tokens[i + 1][1], tokens[i], tokens[i + 2])] + 
				tokens[i + 3:]
			)

	# > < >= <= == !=
	for i in range(len(tokens) - 2):
		if tokens[i][0] == 'expression' and tokens[i + 2][0] == 'expression' and tokens[i + 1][0] == 'token' and\
		tokens[i + 1][1] in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NQ']:
			return parse(
				tokens[:i] + 
				[('expression', tokens[i + 1][1], tokens[i], tokens[i + 2])] + 
				tokens[i + 3:]
			)

	# { expr/action + }
	for i in range(len(tokens) - 1):
		if tokens[i][0] == 'token' and tokens[i][1] == 'LEFT_X':
			lst = []
			flag = True
			u = i + 1
			while u < len(tokens) and (tokens[u][0] in ['action', 'expression'] or tokens[u] == ('token', 'SEP_2')):
				lst.append(tokens[u])
				u += 1
			if u < len(tokens) and tokens[u][0] == 'token' and tokens[u][1] == 'RIGHT_X':
				return parse(
					tokens[:i] + [(
						'actions',
						lst
					)] + tokens[u + 1:]
				)

	# while expr actions
	for i in range(len(tokens) - 2):
		if \
			tokens[i][0] == 'token' and tokens[i][1] == 'WHILE' and \
			tokens[i + 1][0] == 'expression' and \
			tokens[i + 2][0] == 'actions':
			return parse(
				tokens[:i] + [(
					'action',
					'while',
					tokens[i + 1],
					tokens[i + 2][1]
				)] + tokens[i + 3:]
			)

	# tuples
	for i in range(len(tokens) - 1):
		if tokens[i][0] == 'token' and tokens[i][1] == 'LEFT_C':
			if tokens[i + 1][0] == 'token' and tokens[i + 1][1] == 'RIGHT_C':
				return parse(
					tokens[:i] + [(
						'expression',
						'tuple',
						[]
					)] + tokens[i + 2:]
				)
			elif\
				len(tokens) > i + 3 and\
				tokens[i + 1][0] == 'expression' and\
				tokens[i + 2][0] == 'token' and tokens[i + 2][1] == 'SEP_1' and\
				tokens[i + 3][0] == 'token' and tokens[i + 3][1] == 'RIGHT_C':
				return parse(
					tokens[:i] + [(
						'expression',
						'tuple',
						[tokens[i + 1]]
					)] + tokens[i + 4:]
				)
			elif tokens[i + 1][0] == 'expression' and tokens[i + 2][0] == 'token' and tokens[i + 2][1] == 'SEP_1':
				u = i + 1
				lst = []
				while u < len(tokens) and (tokens[u][0] == 'expression' or (tokens[u][0] == 'token' and tokens[u][1] == 'SEP_1')):
					if tokens[u][0] == 'expression':
						lst.append(tokens[u])
					u += 1
				if u < len(tokens) and tokens[u][0] == 'token' and tokens[u][1] == 'RIGHT_C':
					return parse(
						tokens[:i] + [(
							'expression',
							'tuple',
							lst
						)] + tokens[u + 1:]
					)

	# (expr)
	for i in range(len(tokens) - 2):
		if \
			tokens[i][0] == 'token' and tokens[i][1] == 'LEFT_C' and\
			tokens[i + 1][0] == 'expression' and\
			tokens[i + 2][0] == 'token' and tokens[i + 2][1] == 'RIGHT_C':
			return parse(
				tokens[:i] + 
				[tokens[i + 1]] + 
				tokens[i + 3:]
			)

	# if expr actions else actions
	for i in range(len(tokens) - 4):
		if \
			tokens[i][0] == 'token' and tokens[i][1] == 'IF' and \
			tokens[i + 1][0] == 'expression' and \
			tokens[i + 2][0] == 'actions' and \
			tokens[i + 3][0] == 'token' and tokens[i + 3][1] == 'ELSE' and \
			tokens[i + 4][0] == 'actions':
			return parse(
				tokens[:i] + [(
					'action',
					'if-else',
					tokens[i + 1],
					tokens[i + 2][1],
					tokens[i + 4][1]
				)] + tokens[i + 5:]
			)

	# if expr actions
	for i in range(len(tokens) - 2):
		if \
			tokens[i][0] == 'token' and tokens[i][1] == 'IF' and \
			tokens[i + 1][0] == 'expression' and \
			tokens[i + 2][0] == 'actions':
			return parse(
				tokens[:i] + [(
					'action',
					'if',
					tokens[i + 1],
					tokens[i + 2][1],
				)] + tokens[i + 3:]
			)
	
	# var = expr
	for i in range(len(tokens) - 2)[::-1]:
		if tokens[i][0] == 'variable' and tokens[i + 1][0] == 'token' and tokens[i + 1][1] == 'ASSIGN' and\
		tokens[i + 2][0] == 'expression':
			return parse(
				tokens[:i] + 
				[('expression', 'assign', tokens[i][1], tokens[i + 2])] + 
				tokens[i + 3:]
			)

	# variable
	for i in range(len(tokens) - 1):
		if tokens[i][0] == 'variable' and not (tokens[i + 1][0] == 'token' and tokens[i + 1][1] == 'ASSIGN'):
			return parse(
				tokens[:i] + 
				[('expression', 'variable', tokens[i][1])] + 
				tokens[i + 1:]
			)

	# expr [expr] = expr
	for i in range(len(tokens) - 6):
		if \
			tokens[i][0] == 'expression' and\
			tokens[i + 1][0] == 'token' and tokens[i + 1][1] == 'LEFT_I' and\
			tokens[i + 2][0] == 'expression' and\
			tokens[i + 3][0] == 'token' and tokens[i + 3][1] == 'RIGHT_I' and\
			tokens[i + 4][0] == 'token' and tokens[i + 4][1] == 'ASSIGN' and\
			tokens[i + 5][0] == 'expression':
			return parse(
				tokens[:i] + [(
					'action',
					'setelem',
					tokens[i + 0],
					tokens[i + 2],
					tokens[i + 5]
				)] +
				tokens[i + 6:]
			)

	# expr [expr]
	for i in range(len(tokens) - 3):
		if \
			tokens[i][0] == 'expression' and\
			tokens[i + 1][0] == 'token' and tokens[i + 1][1] == 'LEFT_I' and\
			tokens[i + 2][0] == 'expression' and\
			tokens[i + 3][0] == 'token' and tokens[i + 3][1] == 'RIGHT_I':
			return parse(
				tokens[:i] + [(
					'expression',
					'getelem',
					tokens[i + 0],
					tokens[i + 2]
				)] +
				tokens[i + 4:]
			)

	return tokens
