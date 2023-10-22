import sys
from sly import Lexer, Parser
import json

from sly.lex import LexError


# Лексический анализатор
class ConfigLexer(Lexer):
    tokens = {NAME, STRING, NUMBER, LPAREN, RPAREN}
    ignore = ' \t'

    NAME = r'[A-Za-zА-Яа-яЁё][A-Za-z0-9А-Яа-яЁё_]*'
    STRING = r'"[^"]*"'
    NUMBER = r'\d+(\.\d+)?'

    LPAREN = r'\('
    RPAREN = r'\)'

    @_(r';.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)


# Синтаксический анализатор
class ConfigParser(Parser):
    tokens = ConfigLexer.tokens

    @_('STRING')
    def data(self, p):
        return p.STRING[1:-1]

    @_('NUMBER')
    def data(self, p):
        return float(p.NUMBER)

    @_('NAME')
    def data(self, p):
        return p.NAME

    @_('LPAREN s_exp_list RPAREN')
    def s_exp(self, p):
        return p.s_exp_list

    @_('data')
    def s_exp(self, p):
        return p.data

    @_('s_exp s_exp_list')
    def s_exp_list(self, p):
        return [p.s_exp] + p.s_exp_list

    @_('s_exp')
    def s_exp_list(self, p):
        return [p.s_exp]

    @_('s_exp')
    def start(self, p):
        return p.s_exp


def parse_config(input_file):
    lexer = ConfigLexer()
    parser = ConfigParser()
    with open(input_file, 'r', encoding="utf-8") as f:
        data = f.read()
        try:
            result = parser.parse(lexer.tokenize(data))
            return json.dumps(result, indent=4, ensure_ascii=False)
        except LexError as e:
            print(f"Lexical error: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py input_file")
    else:
        input_file = sys.argv[1]
        json_result = parse_config(input_file)
        if json_result:
            print(json_result)
