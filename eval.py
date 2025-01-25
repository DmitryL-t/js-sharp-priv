def fun(i, dct=None):
	# dct - это переменные
	if dct == None:
		dct = {}
	if i[0] == 'expression':
		if i[1] == 'int':
			return ('int', i[2])
		if i[1] == 'float':
			return ('float', i[2])
		if i[1] == 'string':
			return ('string', i[2])
		if i[1] == 'tuple':
			return ('tuple', [fun(j, dct) for j in i[2]])
		if i[1] == 'null':
			return ('null', i[2])

		# Присваиваем переменной значение
		if i[1] == 'assign':
			variable, value = i[2], fun(i[3], dct)
			if variable == 'cout': # `cout` - вывод
				print(object_to_str(value), end='')
			else:
				dct[variable] = value
			return value
		
		# Математические операции. В случае деления на ноль, сложения числа со строкой, и так далее, возвращаем null
		if i[1] == 'getelem':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 in ['string', 'tuple'] and type2 in ['int', 'float']:
				if len(val1):
					return val1[int(val2) % len(val1)]
				return ('null', None)
			return ('null', None)

		if i[1] == 'ADD':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', val1 + val2)
				if type1 == 'float':
					return ('float', val1 + val2)
				if type1 == 'string':
					return ('string', val1 + val2)
				if type1 == 'tuple':
					return ('tuple', val1 + val2)
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('float', val1 + val2)
			return ('null', None)
		
		if i[1] == 'SUB':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', val1 - val2)
				if type1 == 'float':
					return ('float', val1 - val2)
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('float', val1 - val2)
			return ('null', None)

		if i[1] == 'MUL':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', val1 * val2)
				if type1 == 'float':
					return ('float', val1 * val2)
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('float', val1 * val2)
			if (type1, type2) == ('int', 'tuple') or (type1, type2) == ('tuple', 'int'):
				return ('tuple', val1 * val2)
			if (type1, type2) == ('string', 'int'):
				return ('string', val1 * val2)
			return ('null', None)
		
		if i[1] == 'DIV':
			try:
				x, y = fun(i[2], dct), fun(i[3], dct)
				type1, type2 = x[0], y[0]
				val1, val2 = x[1], y[1]
				if type1 == type2:
					if type1 == 'int':
						return ('int', val1 // val2) # Для нецелочисленного деления используем value1 / (value2 + 0.0)
					if type1 == 'float':
						return ('float', val1 / val2)
				if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
					return ('float', val1 / val2)
			except ZeroDivisionError:
				return ('null', None)
		
		if i[1] == 'MOD':
			try:
				x, y = fun(i[2], dct), fun(i[3], dct)
				type1, type2 = x[0], y[0]
				val1, val2 = x[1], y[1]
				if type1 == type2:
					if type1 == 'int':
						return ('int', val1 % val2)
					if type1 == 'float':
						return ('float', val1 % val2)
				if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
					return ('float', val1 % val2)
			except ZeroDivisionError:
				return ('null', None)
		
		if i[1] == 'LT':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', int(val1 < val2))
				if type1 == 'float':
					return ('int', int(val1 < val2))
				if type1 == 'string':
					return ('string', int(val1 < val2))
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('int', int(val1 < val2))
			return ('null', None)
		
		if i[1] == 'GT':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', int(val1 > val2))
				if type1 == 'float':
					return ('int', int(val1 > val2))
				if type1 == 'string':
					return ('string', int(val1 > val2))
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('int', int(val1 > val2))
			return ('null', None)
		
		if i[1] == 'LE':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', int(val1 <= val2))
				if type1 == 'float':
					return ('int', int(val1 <= val2))
				if type1 == 'string':
					return ('string', int(val1 <= val2))
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('int', int(val1 <= val2))
			return ('null', None)
		
		if i[1] == 'GE':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == type2:
				if type1 == 'int':
					return ('int', int(val1 >= val2))
				if type1 == 'float':
					return ('int', int(val1 >= val2))
				if type1 == 'string':
					return ('string', int(val1 >= val2))
			if (type1, type2) == ('int', 'float') or (type1, type2) == ('float', 'int'):
				return ('int', int(val1 >= val2))
			return ('null', None)
		
		# Если сравнивать бесконечные списки, будет ошибка
		if i[1] == 'EQ':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			return ('int', int(val1 == val2 and type1 == type2))  # Возвращает ('int', 0) или ('int', 1)

		if i[1] == 'NE':
			x, y = fun(i[2], dct), fun(i[3], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			return ('int', int(val1 != val2 or type1 != type2))  # Возвращает ('int', 0) или ('int', 1)
		
		
		# Получаем значение переменной. `cin` - это ввод числа пользователем
		if i[1] == 'variable':
			if i[2] == 'cin':
				return ('int', int(input()))
			else:
				return dct[i[2]]

	if i[0] == 'action':
		if i[1] == 'setelem':
			x, y, z = fun(i[2], dct), fun(i[3], dct), fun(i[4], dct)
			type1, type2 = x[0], y[0]
			val1, val2 = x[1], y[1]
			if type1 == 'tuple' and type2 in ['int', 'float']:
				if len(val1):
					val1[int(val2) % len(val1)] = z
					return z 
				else:
					return ('null', None)
			return ('null', None)

		if i[1] == 'while':
			while fun(i[2], dct)[1]:
				for u in i[3]:
					fun(u, dct)
		if i[1] == 'if-else':
			if fun(i[2], dct)[1]:
				for u in i[3]:
					fun(u, dct)
			else:
				for u in i[4]:
					fun(u, dct)
		if i[1] == 'if':
			if fun(i[2], dct)[1]:
				for u in i[3]:
					fun(u, dct)

def object_to_str(expr, starting=None): # Печатаем объект
	# Избегаем бесконечной рекурсии в случае, если кортеж содержит сам себя
	if expr == starting:
		return '...'

	if starting == None:
		starting = expr
	tp, val = expr
	if tp in ['int', 'float', 'string']:
		return str(val) # Числа и строки печатаем как есть
	# Рекурсия
	elif tp == 'tuple':
		if len(val) == 0:
			return '()'
		elif len(val) == 1:
			return '(' + object_to_str(val[0], starting=expr) + ',)'
		else:
			return '(' + ','.join([object_to_str(i, starting=expr) for i in val]) + ')'
