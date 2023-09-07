### Copyright 2023 @ Shevchenko Nikita
### 
### Permission is hereby granted, free of charge,
### to any person obtaining a copy of this software and associated documentation
### files (the “Software”), to deal in the Software without restriction,
### including without limitation the rights to use, copy, modify, merge,
### publish, distribute, sublicense, and/or sell copies of the Software,
### and to permit persons to whom the Software is furnished to do so, subject
### to the following conditions:
### 
### The above copyright notice and this permission notice shall be included
### in all copies or substantial portions of the Software.
### 
### THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
### EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
### A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
### LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
### ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Made on Python 3.11.0

import aiohttp
import asyncio

async def get_matrix(url: str) -> list[int]:
    loaded_text_result = await _load_text_from_url(url)
    if loaded_text_result == None: return []
    dimensional_array = _convert_to_2d_array(loaded_text_result)
    
    state = _init_state(dimensional_array)

    while _is_uncomplete(state):
        _do_task(state)

    return state['return_list']

async def _load_text_from_url(url: str) -> str:
    try:
        text = ''
        
        session = aiohttp.ClientSession()
        async with session.get(url) as resp:
            text = await resp.text()
        await session.close()

        #print("Something went wrong")

        return text
    except:
        return None

def _do_task(state: dict) -> None:

    neighbours = _get_neighbours(state)

    _init_on_start(state)

    if (not neighbours[state['direction']]):
        state['direction'] = _rotated_clockwise(state['direction'])

    _move_pos(state)

    if _is_uncomplete(state):
        state['return_list'].append(state['array'][state['pos_y']][state['pos_x']])
        state['history'].append([state['pos_x'], state['pos_y']])
        state['checked'] += 1

    #print(state)

def _convert_to_2d_array(text: str) -> list[list[int]]:
    num_lines = [line for line in text.split('\n')[1:-1:2]]
    numbers = []
    for line in num_lines:
        arr = []
        for num in line.split('|')[1:-1]: arr.append(int(num.strip()))
        numbers.append(arr)
            
    return numbers

def _init_state(array: list[list[int]]) -> dict:
    d = {
        'array': array,
        'size_x': _get_2d_array_size(array)[0],
        'size_y': _get_2d_array_size(array)[1],
        'checked': 0,
        'history': [],
        'pos_x': 0,
        'pos_y': 0,
        'direction': 'down',
        'return_list': [],
        'started': False
    }
    return d

def _get_2d_array_size(array: list[list[int]]) -> list:
    return [len(array[0]), len(array)]

def _is_uncomplete(state: dict) -> bool:
    return state['checked'] < state['size_x'] * state['size_y']



def _init_on_start(state: dict) -> None:
    if not state['started']:
        state['started'] = True
        state['return_list'].append(state['array'][state['pos_y']][state['pos_x']])
        state['history'].append([state['pos_x'], state['pos_y']])
        state['checked'] += 1

def _rotated_clockwise(direction: str) -> str:
    match direction:
        case 'down':
            return 'right'
        case 'right':
            return 'up'
        case 'up':
            return 'left'
        case 'left':
            return 'down'

def _move_pos(state: dict) -> None:
    match state['direction']:
        case 'down':
            state['pos_y'] += 1
        case 'up':
            state['pos_y'] -= 1
        case 'right':
            state['pos_x'] += 1
        case 'left':
            state['pos_x'] -= 1

def _get_neighbours(state: dict) -> dict:
    d = {
        'down': state['pos_y'] + 1 < state['size_y'] and state['pos_y'] + 1 >= 0 and [state['pos_x'], state['pos_y'] + 1] not in state['history'],
        'up': state['pos_y'] - 1 < state['size_y'] and state['pos_y'] - 1 >= 0 and [state['pos_x'], state['pos_y'] - 1] not in state['history'],
        'right': state['pos_x'] + 1 < state['size_x'] and state['pos_x'] + 1 >= 0 and [state['pos_x'] + 1, state['pos_y']] not in state['history'],
        'left': state['pos_x'] - 1 < state['size_x'] and state['pos_x'] - 1 >= 0 and [state['pos_x'] - 1, state['pos_y']] not in state['history']
    }
    return d

