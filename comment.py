#!/usr/bin/env python

import click as _click
import envoy as _envoy

import re as _re


COMMENT_STR = '#'


def expand_line_numbers(lines_code):
    line_numbers = []
    for code in [x.strip(' ') for x in lines_code.split(',')]:
        if '-' in code:
            start, end = code.split('-')
            line_numbers.extend( range(int(start), int(end) + 1) )
        else:
            line_numbers.append( int(code) )
    return line_numbers

    
def sub_lines(pattern, repl, data_str, line_numbers):
    data_lines = data_str.strip('\n').split('\n')
    for ln in line_numbers:
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
def comment(lines_code, input, symbol):
    """Comment out lines by line number."""
    _click.echo(sub_lines('^', symbol, input.read(), expand_line_numbers(lines_code)))



@cli.command()
@_click.argument('lines_code')
@_click.argument('input', type=_click.File('r'))
@_click.option('-s', '--symbol', default=COMMENT_STR, help='String to use a comment symbol.')
def uncomment(lines_code, input, symbol):
    """Uncomment lines by line number."""
    _click.echo(sub_lines('^' +symbol, '', input.read(), expand_line_numbers(lines_code)))
    
    
if __name__ == '__main__':
    cli()
