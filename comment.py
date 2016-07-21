#!/usr/bin/env python

import click as _click
import envoy as _envoy

import re as _re


COMMENT_STR = '#'

def complement(int_list, min_value, max_value):
    return list(set(range(min_value, max_value + 1)) - set(int_list))


def expand_line_numbers(lines_code):
    line_numbers = []
    for code in [x.strip(' ') for x in lines_code.split(',')]:
        if '-' in code:
            start, end = code.split('-')
            line_numbers.extend( range(int(start), int(end) + 1) )
        else:
            line_numbers.append( int(code) )
    return list(set(line_numbers))

    
def sub_lines(pattern, repl, data_str, line_numbers, inverse):
    data_lines = data_str.strip('\n').split('\n')
    max_number = len(data_lines)
    if inverse:
        line_numbers = complement(line_numbers, 1, max_number)
    for ln in line_numbers:
        if ln > max_number:
            break
        # Convert to zero base index
        ln = ln - 1
        data_lines[ln] = _re.sub(pattern, repl, data_lines[ln])
    return '\n'.join(data_lines)

    
@_click.group()
def cli():
    pass


@cli.command()
@_click.argument('lines_code')
@_click.argument('input', type=_click.File('r'))
@_click.option('-s', '--symbol', default=COMMENT_STR, help='String to use a comment symbol.')
@_click.option('-i', '--inverse', is_flag=True, help='Comment out the lines that are not in the list.')
def comment(lines_code, input, symbol, inverse):
    """Comment out lines by line number."""
    _click.echo(sub_lines('^', symbol, input.read(), expand_line_numbers(lines_code), inverse))



@cli.command()
@_click.argument('lines_code')
@_click.argument('input', type=_click.File('r'))
@_click.option('-s', '--symbol', default=COMMENT_STR, help='String to use a comment symbol.')
@_click.option('-i', '--inverse', is_flag=True, help='Uncomment the lines that are not in the list.')
def uncomment(lines_code, input, symbol, inverse):
    """Uncomment lines by line number."""
    _click.echo(sub_lines('^' +symbol, '', input.read(), expand_line_numbers(lines_code), inverse))
    
    
if __name__ == '__main__':
    cli()
