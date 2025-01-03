import numpy as np
import epde #to make your own differential equations from data

def process_summand(summand):
  summand = summand.replace(' ', '')
  summand_name = ''
  summand_dict = {}
  summand_arr = summand.split('*')
  
  if len(summand_arr) == 1 and 'd' not in summand_arr[0] and 'u' not in summand_arr[0] and 'x' not in summand_arr[0] and 's' not in summand_arr[0]:
    #checking const summand
    summand_name = '+const'
    summand_dict['coeff'] = np.round(float(summand_arr[0]), 4)
    summand_dict['term'] = [None,]
    summand_dict['pow'] = 0
    summand_dict['var'] = 0 
    return summand_name, summand_dict


  pow = []
  var = []
  term = []
  freq = []
  coeff = 1
  
  if summand[0] == '-' and not(summand[1].isdigit()):
    coeff = -1
    summand_dict['coeff'] = coeff

  for i in range(len(summand_arr)):
    frequancy = None
    power = 0
    varr = 0

    end_of_summand = summand_arr[i].find('{')
    if end_of_summand == -1: 
      #coefficient
      coeff = float(summand_arr[i])
      coeff = np.round(coeff,4)
      summand_dict['coeff'] = coeff
      if summand_dict['coeff'] < 0:
        summand_name = '-' + str(summand_dict['coeff'])[1:]
      else:
        summand_name = '+' + str(summand_dict['coeff']) 
    else:
      #part with some kind of var or trig tokens, non-coefficient
      if len(summand_name) > 0:
        summand_name = summand_name + '*' + summand_arr[i][0 : end_of_summand]
      else:
        summand_name = summand_arr[i][0 : end_of_summand]
      
      if 'x0' in summand_arr[i]:
        term.append([0,])
      else:
        term.append([None,])
    
    if coeff != 0:
      #if coeff == 0 -> summand is None and it's useless
      if 'cos' in summand or 'sin' in summand:
        index_freq = summand_arr[i].find('freq:')
        if index_freq != -1:
          index_freq_end = summand_arr[i][index_freq:].find(',')
          if index_freq_end == -1:
            index_freq_end = summand_arr[i][index_freq:].find('}')
          frequancy = summand_arr[i][index_freq + 5 : index_freq_end]
          frequancy = float(frequancy)
          frequancy = np.round(frequancy, 4)
        if 'x0' in summand_arr[i] or 's' in summand_arr[i]:
          freq.append(frequancy)
      
      index_power = summand_arr[i].find('power:')
      if index_power != -1:
        index_power_end = summand_arr[i][index_power:].find(',')
        if index_power_end == -1:
          index_power_end = summand_arr[i][index_power:].find('}')
        power = summand_arr[i][index_power + 6 : index_power + index_power_end]
        power = int(float(power))
        pow.append(power)
        if 'x0' in summand:
          var.append(varr)
  
  if  coeff ==  0:
    summand_name = None
    summand_dict = None
    return summand_name, summand_dict
  
  if len(pow) == 1:
    pow = pow[0]
  if len(var) == 1:
    var = var[0]
  if len(term) == 1:
    term = term[0]

  term_name_idx = summand_name.find('*') + 1
  term_name = summand_name[term_name_idx:]

  summand_dict[term_name] = term
  summand_dict['pow'] = pow 
  summand_dict['var'] = var
  if len(freq) > 0:
    if len(freq) == 1:
      freq = freq[0]
    summand_dict['freq'] = freq

  return summand_name, summand_dict

def parse_du(eq):
  if not (isinstance(eq, str)):
    eq = eq.text_form
  eq = eq.replace(" ", "")
  res_eq = {}
  left_eq, right_eq = eq.split('=')
  left_eq = left_eq.split('+')
  right_eq = right_eq.split('}')[0]
  right_eq += '}'
  if right_eq[0] == '-':
    left_eq.append(right_eq[1:])
  else:
    if right_eq[0] == '+':
      left_eq.append('-' + right_eq[1:])
    else:
      left_eq.append('-' + right_eq)
  #del useless information and send all to left side of equation
  
  for i in range(len(left_eq)): #parsing every summand
    summand = left_eq[i]
    summand_name, summand_dict = process_summand(summand)
    if summand_name is None or summand_dict is None:
      continue
    else:
      res_eq[summand_name] = summand_dict

  return res_eq
  
    


'''
structure of summand:

coeff
term summands, if it's du/dx0 or something like this is [0,] else [None,]
pow
if it's trigonometric - freq (optional)
var - if len 2 (coeff + 1 var) -> 0, else list of 0 ([0,0...])
'''

#Example
eq = '0.4909684923233549 * du/dx0{power: 1.0} * sin{power: 1.0, freq: 0.9695963606508056, dim: 0.0} + 0.0 * u{power: 1.0} + 0.8912866079430934 * du/dx0{power: 1.0} * cos{power: 1.0, freq: 0.9659963566320707, dim: 0.0} + -0.01055228426538488 = du/dx0{power: 1.0}'
tedeous_eq = parse_du(eq)
print(tedeous_eq)
