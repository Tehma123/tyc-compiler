"""
Lexer test cases for TyC compiler
Tests all lexical elements: keywords, identifiers, operators, literals, comments, and error cases
"""

import pytest
from tests.utils import Tokenizer
from src.grammar.lexererr import UncloseString, IllegalEscape, ErrorToken


# ============================================================================
# KEYWORDS (Tests 1-15)
# ============================================================================

def test_01_keyword_auto():
    """Test 'auto' keyword"""
    tokenizer = Tokenizer("auto")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'AUTO'
    assert tokens[0].text == 'auto'


def test_02_keyword_int():
    """Test 'int' keyword"""
    tokenizer = Tokenizer("int")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'


def test_03_keyword_float():
    """Test 'float' keyword"""
    tokenizer = Tokenizer("float")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'FLOAT'


def test_04_keyword_string():
    """Test 'string' keyword"""
    tokenizer = Tokenizer("string")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING'


def test_05_keyword_void():
    """Test 'void' keyword"""
    tokenizer = Tokenizer("void")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'VOID'


def test_06_keyword_struct():
    """Test 'struct' keyword"""
    tokenizer = Tokenizer("struct")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRUCT'


def test_07_keyword_if():
    """Test 'if' keyword"""
    tokenizer = Tokenizer("if")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'IF'


def test_08_keyword_else():
    """Test 'else' keyword"""
    tokenizer = Tokenizer("else")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ELSE'


def test_09_keyword_while():
    """Test 'while' keyword"""
    tokenizer = Tokenizer("while")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'WHILE'


def test_10_keyword_for():
    """Test 'for' keyword"""
    tokenizer = Tokenizer("for")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'FOR'


def test_11_keyword_switch():
    """Test 'switch' keyword"""
    tokenizer = Tokenizer("switch")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'SWITCH'


def test_12_keyword_case():
    """Test 'case' keyword"""
    tokenizer = Tokenizer("case")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'CASE'


def test_13_keyword_default():
    """Test 'default' keyword"""
    tokenizer = Tokenizer("default")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'DEFAULT'


def test_14_keyword_break_continue_return():
    """Test 'break', 'continue', 'return' keywords"""
    tokenizer = Tokenizer("break continue return")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'BREAK'
    assert tokens[1].type == 'CONTINUE'
    assert tokens[2].type == 'RETURN'


def test_15_keywords_case_sensitive():
    """Test that keywords are case-sensitive"""
    tokenizer = Tokenizer("Int INT Float AUTO Auto")
    tokens = tokenizer.tokenize()
    # These should all be identifiers, not keywords
    assert all(tok.type == 'ID' for tok in tokens[:5])


# ============================================================================
# IDENTIFIERS (Tests 16-20)
# ============================================================================

def test_16_identifier_simple():
    """Test simple identifiers"""
    tokenizer = Tokenizer("x y z variable")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'ID' for tok in tokens[:4])


def test_17_identifier_with_underscore():
    """Test identifiers with underscores"""
    tokenizer = Tokenizer("_var var_ _123 __double")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'ID' for tok in tokens[:4])


def test_18_identifier_with_digits():
    """Test identifiers with digits"""
    tokenizer = Tokenizer("var1 x2y3 name123")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'ID' for tok in tokens[:3])


def test_19_identifier_long():
    """Test long identifier"""
    tokenizer = Tokenizer("this_is_a_very_long_identifier_name_123")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'
    assert tokens[0].text == "this_is_a_very_long_identifier_name_123"


def test_20_identifier_vs_keyword():
    """Test identifiers that contain keywords"""
    tokenizer = Tokenizer("intValue floatNumber automate")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'ID' for tok in tokens[:3])


# ============================================================================
# OPERATORS (Tests 21-30)
# ============================================================================

def test_21_arithmetic_operators():
    """Test arithmetic operators"""
    tokenizer = Tokenizer("+ - * / %")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'PLUS'
    assert tokens[1].type == 'MINUS'
    assert tokens[2].type == 'MUL'
    assert tokens[3].type == 'DIV'
    assert tokens[4].type == 'MOD'


def test_22_relational_operators():
    """Test relational operators"""
    tokenizer = Tokenizer("< > <= >=")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'LT'
    assert tokens[1].type == 'GT'
    assert tokens[2].type == 'LE'
    assert tokens[3].type == 'GE'


def test_23_equality_operators():
    """Test equality operators"""
    tokenizer = Tokenizer("== !=")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'EQ'
    assert tokens[1].type == 'NEQ'


def test_24_logical_operators():
    """Test logical operators"""
    tokenizer = Tokenizer("&& || !")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'AND'
    assert tokens[1].type == 'OR'
    assert tokens[2].type == 'NOT'


def test_25_increment_decrement():
    """Test increment and decrement operators"""
    tokenizer = Tokenizer("++ --")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INC'
    assert tokens[1].type == 'DEC'


def test_26_assignment_operator():
    """Test assignment operator"""
    tokenizer = Tokenizer("=")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ASSIGN'


def test_27_member_access_operator():
    """Test member access operator"""
    tokenizer = Tokenizer(".")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'DOT'


def test_28_operator_precedence_sequence():
    """Test operators in sequence"""
    tokenizer = Tokenizer("a+b*c-d/e%f")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'  # a
    assert tokens[1].type == 'PLUS'
    assert tokens[2].type == 'ID'  # b
    assert tokens[3].type == 'MUL'
    assert tokens[4].type == 'ID'  # c
    assert tokens[5].type == 'MINUS'
    assert tokens[6].type == 'ID'  # d
    assert tokens[7].type == 'DIV'
    assert tokens[8].type == 'ID'  # e
    assert tokens[9].type == 'MOD'
    assert tokens[10].type == 'ID'  # f


def test_29_operator_no_space():
    """Test operators without spaces"""
    tokenizer = Tokenizer("x++y--z")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'  # x
    assert tokens[1].type == 'INC'
    assert tokens[2].type == 'ID'  # y
    assert tokens[3].type == 'DEC'
    assert tokens[4].type == 'ID'  # z


def test_30_comparison_chain():
    """Test comparison operators in chain"""
    tokenizer = Tokenizer("a<b<=c>d>=e==f!=g")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'LT'
    assert tokens[3].type == 'LE'
    assert tokens[5].type == 'GT'
    assert tokens[7].type == 'GE'
    assert tokens[9].type == 'EQ'
    assert tokens[11].type == 'NEQ'


# ============================================================================
# SEPARATORS (Tests 31-35)
# ============================================================================

def test_31_parentheses():
    """Test parentheses separators"""
    tokenizer = Tokenizer("( )")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'LPAREN'
    assert tokens[1].type == 'RPAREN'


def test_32_braces():
    """Test braces separators"""
    tokenizer = Tokenizer("{ }")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'LBRACE'
    assert tokens[1].type == 'RBRACE'


def test_33_semicolon_comma():
    """Test semicolon and comma separators"""
    tokenizer = Tokenizer("; ,")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'SEMI'
    assert tokens[1].type == 'COMMA'


def test_34_colon():
    """Test colon separator"""
    tokenizer = Tokenizer(":")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'COLON'


def test_35_all_separators():
    """Test all separators in function declaration"""
    tokenizer = Tokenizer("int func(int x, float y) { return 0; }")
    tokens = tokenizer.tokenize()
    assert tokens[2].type == 'LPAREN'
    assert tokens[5].type == 'COMMA'
    assert tokens[8].type == 'RPAREN'
    assert tokens[9].type == 'LBRACE'
    assert tokens[12].type == 'SEMI'
    assert tokens[13].type == 'RBRACE'


# ============================================================================
# INTEGER LITERALS (Tests 36-38)
# ============================================================================

def test_36_integer_literals_simple():
    """Test simple integer literals"""
    tokenizer = Tokenizer("0 1 42 123 999")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'INT_LITERAL' for tok in tokens[:5])
    assert tokens[0].text == '0'
    assert tokens[2].text == '42'


def test_37_integer_literals_large():
    """Test large integer literals"""
    tokenizer = Tokenizer("1234567890 999999")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT_LITERAL'
    assert tokens[0].text == '1234567890'


def test_38_integer_in_expression():
    """Test integer literals in expressions"""
    tokenizer = Tokenizer("x = 5 + 10 - 3")
    tokens = tokenizer.tokenize()
    assert tokens[2].type == 'INT_LITERAL'
    assert tokens[2].text == '5'
    assert tokens[4].type == 'INT_LITERAL'
    assert tokens[6].type == 'INT_LITERAL'


# ============================================================================
# FLOAT LITERALS (Tests 39-43)
# ============================================================================

def test_39_float_with_decimal():
    """Test float literals with decimal point"""
    tokenizer = Tokenizer("3.14 0.5 123.456")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:3])
    assert tokens[0].text == '3.14'


def test_40_float_with_decimal_no_fraction():
    """Test float literals with decimal point but no fraction"""
    tokenizer = Tokenizer("1. 42. 100.")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:3])


def test_41_float_no_integer_part():
    """Test float literals without integer part"""
    tokenizer = Tokenizer(".5 .123 .99")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:3])


def test_42_float_with_exponent():
    """Test float literals with exponent"""
    tokenizer = Tokenizer("1e5 2.5e10 3E-2 .5e+3 1.23E4")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:5])
    assert tokens[0].text == '1e5'
    assert tokens[2].text == '3E-2'


def test_43_float_integer_only_with_exponent():
    """Test float literals: integer with exponent (no decimal point)"""
    tokenizer = Tokenizer("5e2 123E+4 99e-1")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:3])


# ============================================================================
# STRING LITERALS (Tests 44-50)
# ============================================================================

def test_44_string_simple():
    """Test simple string literals"""
    tokenizer = Tokenizer('"hello" "world"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'
    assert tokens[0].text == 'hello'  # quotes stripped
    assert tokens[1].text == 'world'


def test_45_string_empty():
    """Test empty string literal"""
    tokenizer = Tokenizer('""')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'
    assert tokens[0].text == ''


def test_46_string_with_escapes():
    """Test string literals with escape sequences"""
    tokenizer = Tokenizer(r'"hello\nworld" "tab\there" "quote:\"" "backslash:\\"')
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'STRING_LITERAL' for tok in tokens[:4])
    assert tokens[0].text == r'hello\nworld'
    assert tokens[1].text == r'tab\there'


def test_47_string_with_all_escapes():
    """Test string with all valid escape sequences"""
    tokenizer = Tokenizer(r'"\b\f\r\n\t\"\\"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'
    assert tokens[0].text == r'\b\f\r\n\t\"\\' 


def test_48_string_illegal_escape():
    """Test string with illegal escape sequence"""
    with pytest.raises(IllegalEscape) as exc_info:
        tokenizer = Tokenizer(r'"hello\aworld"')
        tokenizer.tokenize()
    assert r'hello\a' in str(exc_info.value)


def test_49_string_unclosed():
    """Test unclosed string literal"""
    with pytest.raises(UncloseString) as exc_info:
        tokenizer = Tokenizer('"hello world')
        tokenizer.tokenize()
    assert 'hello world' in str(exc_info.value)


def test_50_string_unclosed_with_newline():
    """Test unclosed string with newline"""
    with pytest.raises(UncloseString) as exc_info:
        tokenizer = Tokenizer('"hello\n')
        tokenizer.tokenize()
    # Text should not include the newline
    assert 'hello' in str(exc_info.value)
    assert '\n' not in str(exc_info.value)


# ============================================================================
# COMMENTS (Tests 51-58)
# ============================================================================

def test_51_line_comment_simple():
    """Test simple line comment"""
    tokenizer = Tokenizer("int x; // this is a comment")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3  # int, x, ;
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[2].type == 'SEMI'


def test_52_line_comment_end_of_file():
    """Test line comment at end of file without newline"""
    tokenizer = Tokenizer("x = 5; // comment")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 4  # x, =, 5, ;


def test_53_line_comment_with_code_chars():
    """Test line comment containing code-like characters"""
    tokenizer = Tokenizer("// int x = 5; float y = 3.14;\nint z;")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[1].text == 'z'


def test_54_block_comment_simple():
    """Test simple block comment"""
    tokenizer = Tokenizer("int /* comment */ x;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[2].type == 'SEMI'


def test_55_block_comment_multiline():
    """Test multiline block comment"""
    tokenizer = Tokenizer("""int /* this is
    a multi-line
    comment */ x;""")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3
    assert tokens[0].type == 'INT'


def test_56_block_comment_with_special_chars():
    """Test block comment containing special characters"""
    tokenizer = Tokenizer("x /* // not a line comment */ y;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3
    assert tokens[0].type == 'ID'
    assert tokens[0].text == 'x'
    assert tokens[1].type == 'ID'
    assert tokens[1].text == 'y'


def test_57_line_comment_with_block_syntax():
    """Test line comment containing block comment syntax"""
    tokenizer = Tokenizer("x; // /* not a block comment\ny;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 4  # x, ;, y, ;
    assert tokens[2].type == 'ID'
    assert tokens[2].text == 'y'


def test_58_consecutive_comments():
    """Test multiple consecutive comments"""
    tokenizer = Tokenizer("""
    // First comment
    /* Block comment */
    // Another line comment
    int x;
    """)
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'


# ============================================================================
# COMPLEX TOKEN SEQUENCES (Tests 59-66)
# ============================================================================

def test_59_function_declaration_complete():
    """Test complete function declaration"""
    tokenizer = Tokenizer("int add(int x, int y) { return x + y; }")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[1].text == 'add'
    assert tokens[2].type == 'LPAREN'
    assert tokens[10].type == 'RETURN'


def test_60_struct_declaration():
    """Test struct declaration"""
    tokenizer = Tokenizer("struct Point { int x; int y; };")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRUCT'
    assert tokens[1].type == 'ID'
    assert tokens[2].type == 'LBRACE'
    assert tokens[9].type == 'RBRACE'
    assert tokens[10].type == 'SEMI'


def test_61_complex_expression():
    """Test complex arithmetic expression"""
    tokenizer = Tokenizer("result = (a + b) * c - d / e % f;")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'
    assert tokens[1].type == 'ASSIGN'
    assert tokens[2].type == 'LPAREN'
    assert tokens[6].type == 'RPAREN'


def test_62_nested_member_access():
    """Test nested member access"""
    tokenizer = Tokenizer("person.address.city.name")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'
    assert tokens[1].type == 'DOT'
    assert tokens[2].type == 'ID'
    assert tokens[3].type == 'DOT'
    assert tokens[5].type == 'DOT'


def test_63_for_loop_complete():
    """Test complete for loop"""
    tokenizer = Tokenizer("for (int i = 0; i < 10; i++) { x = x + 1; }")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'FOR'
    assert tokens[1].type == 'LPAREN'
    assert tokens[12].type == 'INC'


def test_64_switch_case():
    """Test switch-case statement"""
    tokenizer = Tokenizer("switch (x) { case 1: break; default: return; }")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'SWITCH'
    assert tokens[5].type == 'CASE'
    assert tokens[7].type == 'COLON'
    assert tokens[10].type == 'DEFAULT'


def test_65_mixed_operators_no_space():
    """Test operators mixed without spaces"""
    tokenizer = Tokenizer("x=y++*--z+w%v/u")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'ASSIGN'
    assert tokens[3].type == 'INC'
    assert tokens[4].type == 'MUL'
    assert tokens[5].type == 'DEC'


def test_66_all_logical_operators():
    """Test all logical operators in expression"""
    tokenizer = Tokenizer("if (a && b || !c && (d || e)) { }")
    tokens = tokenizer.tokenize()
    assert tokens[3].type == 'AND'
    assert tokens[5].type == 'OR'
    assert tokens[6].type == 'NOT'
    assert tokens[11].type == 'OR'


# ============================================================================
# WHITESPACE AND FORMATTING (Tests 67-72)
# ============================================================================

def test_67_multiple_spaces():
    """Test multiple spaces between tokens"""
    tokenizer = Tokenizer("int     x    =    5    ;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5
    assert tokens[0].type == 'INT'


def test_68_tabs_and_spaces():
    """Test tabs and spaces as whitespace"""
    tokenizer = Tokenizer("int\tx\t=\t5;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5


def test_69_newlines_between_tokens():
    """Test newlines between tokens"""
    tokenizer = Tokenizer("int\nx\n=\n5\n;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5


def test_70_mixed_whitespace():
    """Test mixed whitespace characters"""
    tokenizer = Tokenizer("int \t\n x \f = \r\n 5;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5


def test_71_no_whitespace():
    """Test minimal whitespace"""
    tokenizer = Tokenizer("int x=5;")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 5


def test_72_empty_lines():
    """Test code with empty lines"""
    tokenizer = Tokenizer("""
    
    int x;
    
    
    float y;
    
    """)
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'
    assert tokens[3].type == 'FLOAT'


# ============================================================================
# EDGE CASES - NUMBERS (Tests 73-78)
# ============================================================================

def test_73_zero_variations():
    """Test different zero representations"""
    tokenizer = Tokenizer("0 0.0 .0 0. 0e0 0.0e0")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT_LITERAL'
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[1:6])


def test_74_number_followed_by_identifier():
    """Test number directly followed by identifier"""
    tokenizer = Tokenizer("123abc")
    tokens = tokenizer.tokenize()
    # Should be two tokens: INT_LITERAL and ID
    assert tokens[0].type == 'INT_LITERAL'
    assert tokens[0].text == '123'
    assert tokens[1].type == 'ID'
    assert tokens[1].text == 'abc'


def test_75_float_ambiguous_cases():
    """Test float literals that might be ambiguous"""
    tokenizer = Tokenizer("1.e5 .5e5 1e+5 1e-5")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:4])


def test_76_multiple_dots():
    """Test expression with multiple dots (not float)"""
    tokenizer = Tokenizer("obj.field1.field2")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'ID'
    assert tokens[1].type == 'DOT'
    assert tokens[2].type == 'ID'


def test_77_number_at_start_of_identifier():
    """Test that identifier cannot start with digit"""
    tokenizer = Tokenizer("123abc 456def")
    tokens = tokenizer.tokenize()
    # First should be INT followed by ID
    assert tokens[0].type == 'INT_LITERAL'
    assert tokens[1].type == 'ID'


def test_78_large_exponent():
    """Test float with large exponent"""
    tokenizer = Tokenizer("1e100 2.5e-50 9.99E+99")
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'FLOAT_LITERAL' for tok in tokens[:3])


# ============================================================================
# EDGE CASES - STRINGS (Tests 79-85)
# ============================================================================

def test_79_string_with_spaces():
    """Test string containing various spaces"""
    tokenizer = Tokenizer('"hello   world\\t\\ntest"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'


def test_80_consecutive_strings():
    """Test multiple string literals in sequence"""
    tokenizer = Tokenizer('"first" "second" "third"')
    tokens = tokenizer.tokenize()
    assert all(tok.type == 'STRING_LITERAL' for tok in tokens[:3])
    assert tokens[0].text == 'first'
    assert tokens[1].text == 'second'


def test_81_string_with_numbers():
    """Test string containing numbers"""
    tokenizer = Tokenizer('"The answer is 42"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'
    assert tokens[0].text == 'The answer is 42'


def test_82_string_with_operators():
    """Test string containing operator characters"""
    tokenizer = Tokenizer('"x + y = z && a || b"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'


def test_83_string_with_consecutive_escapes():
    """Test string with consecutive escape sequences"""
    tokenizer = Tokenizer(r'"\n\n\t\t\r\r"')
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRING_LITERAL'
    assert tokens[0].text == r'\n\n\t\t\r\r'


def test_84_string_illegal_escape_at_end():
    """Test string with illegal escape at the end"""
    with pytest.raises(IllegalEscape):
        tokenizer = Tokenizer(r'"hello\x"')
        tokenizer.tokenize()


def test_85_string_unclosed_at_eof():
    """Test unclosed string at EOF"""
    with pytest.raises(UncloseString):
        tokenizer = Tokenizer('"hello world')
        tokenizer.tokenize()


# ============================================================================
# OPERATOR DISAMBIGUATION (Tests 86-91)
# ============================================================================

def test_86_increment_vs_plus():
    """Test disambiguation between ++ and + +"""
    tokenizer = Tokenizer("x++ + ++y")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'INC'
    assert tokens[2].type == 'PLUS'
    assert tokens[3].type == 'INC'


def test_87_comparison_operators():
    """Test all comparison operators together"""
    tokenizer = Tokenizer("a<b<=c>d>=e")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'LT'
    assert tokens[3].type == 'LE'
    assert tokens[5].type == 'GT'
    assert tokens[7].type == 'GE'


def test_88_minus_vs_decrement():
    """Test disambiguation between - and --"""
    tokenizer = Tokenizer("x-- - --y")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'DEC'
    assert tokens[2].type == 'MINUS'
    assert tokens[3].type == 'DEC'


def test_89_assign_vs_equality():
    """Test = vs =="""
    tokenizer = Tokenizer("x = y == z")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'ASSIGN'
    assert tokens[3].type == 'EQ'


def test_90_not_vs_not_equal():
    """Test ! vs !="""
    tokenizer = Tokenizer("!x != y")
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'NOT'
    assert tokens[2].type == 'NEQ'


def test_91_and_vs_logical_and():
    """Test && operator (no single & in TyC)"""
    tokenizer = Tokenizer("x && y")
    tokens = tokenizer.tokenize()
    assert tokens[1].type == 'AND'


# ============================================================================
# ERROR CASES (Tests 92-97)
# ============================================================================

def test_92_illegal_character_basic():
    """Test illegal character"""
    with pytest.raises(ErrorToken):
        tokenizer = Tokenizer("int x = 5 @ y;")
        tokenizer.tokenize()


def test_93_illegal_character_special():
    """Test illegal special characters"""
    with pytest.raises(ErrorToken):
        tokenizer = Tokenizer("int x # y")
        tokenizer.tokenize()


def test_94_string_illegal_escape_middle():
    """Test illegal escape in middle of string"""
    with pytest.raises(IllegalEscape):
        tokenizer = Tokenizer(r'"hello\kworld"')
        tokenizer.tokenize()


def test_95_multiple_illegal_escapes():
    """Test that first illegal escape is caught"""
    with pytest.raises(IllegalEscape):
        tokenizer = Tokenizer(r'"test\q\w\e"')
        tokenizer.tokenize()


def test_96_string_unclosed_with_carriage_return():
    """Test unclosed string with carriage return"""
    with pytest.raises(UncloseString):
        tokenizer = Tokenizer('"hello\r')
        tokenizer.tokenize()


def test_97_illegal_character_in_expression():
    """Test illegal character in complex expression"""
    with pytest.raises(ErrorToken):
        tokenizer = Tokenizer("result = (a + b) $ c;")
        tokenizer.tokenize()


# ============================================================================
# COMPLEX REAL-WORLD SCENARIOS (Tests 98-100)
# ============================================================================

def test_98_complete_function_with_comments():
    """Test complete function with comments"""
    source = """
    // Calculate sum
    int sum(int a, int b) {
        /* Add two numbers */
        return a + b; // Return result
    }
    """
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[1].text == 'sum'
    assert tokens[10].type == 'RETURN'


def test_99_struct_with_initialization():
    """Test struct declaration and usage"""
    source = """
    struct Point {
        int x;
        int y;
    };
    Point p = {10, 20};
    """
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'STRUCT'
    assert tokens[11].type == 'ID'
    assert tokens[11].text == 'Point'
    assert tokens[15].type == 'INT_LITERAL'


def test_100_nested_control_structures():
    """Test nested control structures with all features"""
    source = """
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0) {
            while (x > 0) {
                x--;
            }
        } else {
            switch (i) {
                case 1: break;
                default: continue;
            }
        }
    }
    """
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    assert tokens[0].type == 'FOR'
    assert tokens[15].type == 'IF'
    assert tokens[24].type == 'WHILE'
    assert tokens[36].type == 'ELSE'
    assert tokens[38].type == 'SWITCH'
    assert tokens[43].type == 'CASE'
    assert tokens[48].type == 'DEFAULT'
