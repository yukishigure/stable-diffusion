import re
import os
import pandas as pd
import torch

re_attention = re.compile(r"""
\\\(|
\\\)|
\\\[|
\\]|
\\\\|
\\|
\(|
\[|
:([+-]?[.\d]+)\)|
\)|
]|
[^\\()\[\]:]+|
:
""", re.X)

re_break = re.compile(r"\s*\bBREAK\b\s*", re.S)

def split_weighted_subprompts(text):
    """
    Parses a string with attention tokens and returns a list of pairs: text and its associated weight.
    Accepted tokens are:
      (abc) - increases attention to abc by a multiplier of 1.1
      (abc:3.12) - increases attention to abc by a multiplier of 3.12
      [abc] - decreases attention to abc by a multiplier of 1.1
      \( - literal character '('
      \[ - literal character '['
      \) - literal character ')'
      \] - literal character ']'
      \\ - literal character '\'
      anything else - just text
    >>> parse_prompt_attention('normal text')
    [['normal text', 1.0]]
    >>> parse_prompt_attention('an (important) word')
    [['an ', 1.0], ['important', 1.1], [' word', 1.0]]
    >>> parse_prompt_attention('(unbalanced')
    [['unbalanced', 1.1]]
    >>> parse_prompt_attention('\(literal\]')
    [['(literal]', 1.0]]
    >>> parse_prompt_attention('(unnecessary)(parens)')
    [['unnecessaryparens', 1.1]]
    >>> parse_prompt_attention('a (((house:1.3)) [on] a (hill:0.5), sun, (((sky))).')
    [['a ', 1.0],
     ['house', 1.5730000000000004],
     [' ', 1.1],
     ['on', 1.0],
     [' a ', 1.1],
     ['hill', 0.55],
     [', sun, ', 1.1],
     ['sky', 1.4641000000000006],
     ['.', 1.1]]
    """

    res = []
    round_brackets = []
    square_brackets = []

    round_bracket_multiplier = 1.1
    square_bracket_multiplier = 1 / 1.1

    def multiply_range(start_position, multiplier):
        for p in range(start_position, len(res)):
            res[p][1] *= multiplier

    for m in re_attention.finditer(text):
        text = m.group(0)
        weight = m.group(1)

        if text.startswith('\\'):
            res.append([text[1:], 1.0])
        elif text == '(':
            round_brackets.append(len(res))
        elif text == '[':
            square_brackets.append(len(res))
        elif weight is not None and len(round_brackets) > 0:
            multiply_range(round_brackets.pop(), float(weight))
        elif text == ')' and len(round_brackets) > 0:
            multiply_range(round_brackets.pop(), round_bracket_multiplier)
        elif text == ']' and len(square_brackets) > 0:
            multiply_range(square_brackets.pop(), square_bracket_multiplier)
        else:
            parts = re.split(re_break, text)
            for i, part in enumerate(parts):
                if i > 0:
                    res.append(["BREAK", -1])
                res.append([part, 1.0])

    for pos in round_brackets:
        multiply_range(pos, round_bracket_multiplier)

    for pos in square_brackets:
        multiply_range(pos, square_bracket_multiplier)

    if len(res) == 0:
        res = [["", 1.0]]

    # merge runs of identical weights
    i = 0
    while i + 1 < len(res):
        if res[i][1] == res[i + 1][1]:
            res[i][0] += res[i + 1][0]
            res.pop(i + 1)
        else:
            i += 1

    weight_sum = 0
    for x in res:
        weight_sum += x[1]

    return [x[0] for x in res], [x[1] / weight_sum for x in res]

def logger(params, log_csv):
    os.makedirs('logs', exist_ok=True)
    cols = [arg for arg, _ in params.items()]
    if not os.path.exists(log_csv):
        df = pd.DataFrame(columns=cols) 
        df.to_csv(log_csv, index=False)

    df = pd.read_csv(log_csv)
    for arg in cols:
        if arg not in df.columns:
            df[arg] = ""
    df.to_csv(log_csv, index = False)

    li = {}
    cols = [col for col in df.columns]
    data = {arg:value for arg, value in params.items()}
    for col in cols:
        if col in data:
            li[col] = data[col]
        else:
            li[col] = ''

    df = pd.DataFrame(li,index = [0])
    df.to_csv(log_csv,index=False, mode='a', header=False)

def seamless_init(klass, mode : str):
	init = klass.__init__
	def __init__(self, *args, **kwargs):
		return init(self, *args, **kwargs, padding_mode = mode)
	klass.__init__ = __init__

def vectorize_prompt(modelCS, batch_size, prompt):
    empty_result = modelCS.get_learned_conditioning(batch_size * [""])
    result = torch.zeros_like(empty_result)
    subprompts, weights = split_weighted_subprompts(prompt)
    weights_sum = sum(weights)
    cntr = 0
    for i, subprompt in enumerate(subprompts):
        cntr += 1
        result = torch.add(result, modelCS.get_learned_conditioning(batch_size * [subprompt]), alpha=weights[i] / weights_sum)
    if cntr == 0:
        result = empty_result
    return result