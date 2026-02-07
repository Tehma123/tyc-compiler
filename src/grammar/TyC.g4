grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// Program Structure
// Note: Semantic analysis must enforce that a 'main' function exists
// with signature: void main() or main() with inferred void return type
program
    : (decl)* EOF
    ;

decl
    : structDecl
    | funcDecl
    ;

structDecl
    : STRUCT ID LBRACE structMember* RBRACE SEMI
    ;

structMember
    : typeSpec ID SEMI
    ;

funcDecl
    : returnType? ID LPAREN paramList? RPAREN block
    ;

paramList
    : param (COMMA param)*
    ;

param
    : typeSpec ID
    ;

// Types
// NOTE: VOID is only allowed as a function return type (see returnType)
typeSpec
    : INT
    | FLOAT
    | STRING
    | ID
    ;

returnType
    : typeSpec
    | VOID
    ;

// Block + statements
block
    : LBRACE stmt* RBRACE
    ;

stmt
    : varDecl
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | block
    | exprStmt
    ;

varDecl
    : AUTO ID (ASSIGN expr)? SEMI
    | typeSpec ID (ASSIGN expr)? SEMI
    ;

exprStmt
    : expr SEMI
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN expr? SEMI
    ;

// Control flow
ifStmt
    : IF LPAREN expr RPAREN stmt (ELSE stmt)?
    ;

whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;

// for(init; cond; update) stmt
forStmt
    : FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN stmt
    ;

forInit
    : varDeclFor
    | assignOnly
    ;

varDeclFor
    : AUTO ID (ASSIGN expr)?
    | typeSpec ID (ASSIGN expr)?
    ;

forUpdate
    : assignOnly
    | incDecExpr
    ;

// switch (expr) { case ... default ... }
switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchSection* defaultSection? switchSection* RBRACE
    ;

switchSection
    : (caseLabel)+ stmt*
    ;

defaultSection
    : DEFAULT COLON stmt*
    ;

caseLabel
    : CASE constExpr COLON
    ;

constExpr
    : constAddExpr
    ;

constAddExpr
    : constMulExpr ((PLUS | MINUS) constMulExpr)*
    ;

constMulExpr
    : constUnaryExpr ((MUL | DIV | MOD) constUnaryExpr)*
    ;

constUnaryExpr
    : (PLUS | MINUS) constUnaryExpr
    | constPrimary
    ;

constPrimary
    : INT_LITERAL
    | LPAREN constExpr RPAREN
    ;
expr
    : assignExpr
    ;

assignExpr
    : assignOnly
    | orExpr
    ;

assignOnly
    : lvalue ASSIGN assignExpr             // right-associative
    ;

orExpr
    : andExpr (OR andExpr)*
    ;

andExpr
    : eqExpr (AND eqExpr)*
    ;

eqExpr
    : relExpr ((EQ | NEQ) relExpr)*
    ;

relExpr
    : addExpr ((LT | LE | GT | GE) addExpr)*
    ;

addExpr
    : mulExpr ((PLUS | MINUS) mulExpr)*
    ;

mulExpr
    : unaryExpr ((MUL | DIV | MOD) unaryExpr)*
    ;

// prefix: ! + - ++ --
unaryExpr
    : prefixIncDec
    | (NOT | PLUS | MINUS) unaryExpr
    | postfixExpr
    ;

prefixIncDec
    : (INC | DEC) lvalue
    ;

incDecExpr
    : prefixIncDec
    | lvalue (INC | DEC)
    ;

// postfix: member access has highest precedence, then call, ++ --
// All postfix operators are left-associative at the same level
postfixExpr
    : postfixPrimary postfixOp*
    ;

postfixOp
    : DOT ID
    | INC
    | DEC
    ;

postfixPrimary
    : postfixCall
    | primaryExpr
    ;

postfixCall
    : ID LPAREN argList? RPAREN
    ;

lvalue
    : ID (DOT ID)*
    | postfixCall (DOT ID)+
    | LPAREN lvalue RPAREN
    ;

argList
    : expr (COMMA expr)*
    ;

primaryExpr
    : INT_LITERAL
    | FLOAT_LITERAL
    | STRING_LITERAL
    | structLiteral
    | ID
    | LPAREN expr RPAREN
    ;

structLiteral
    : LBRACE (expr (COMMA expr)*)? RBRACE
    ;

WS : [ \t\f\r\n]+ -> skip ; // skip spaces, tabs, formfeed

LINE_COMMENT: '//' ~[\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;

AUTO: 'auto';

BREAK: 'break';

CASE: 'case';

CONTINUE: 'continue';

DEFAULT: 'default';

ELSE: 'else';

FLOAT: 'float';

FOR: 'for';

IF: 'if';

INT: 'int';

RETURN: 'return';

STRING: 'string';

STRUCT: 'struct';

SWITCH: 'switch';

VOID: 'void';

WHILE: 'while';

ID: [a-zA-Z_][a-zA-Z_0-9]*;

OR: '||';

AND: '&&';

EQ: '==';

NEQ: '!=';

LE: '<=';

GE: '>=';

NOT: '!';

INC: '++';

DEC: '--';

PLUS: '+';

MINUS: '-';

MUL: '*';

DIV: '/';

MOD: '%';

ASSIGN: '=';

LT: '<';

GT: '>';

DOT: '.';

LPAREN: '(';

RPAREN: ')';

LBRACE: '{';

RBRACE: '}';

SEMI: ';';

COMMA: ',';

COLON: ':';

fragment DIGIT: [0-9];

fragment EXP: [eE][+-]? DIGIT+;

FLOAT_LITERAL: DIGIT+ '.' DIGIT* EXP? | '.' DIGIT+ EXP? | DIGIT+ EXP;

INT_LITERAL: DIGIT+;

ILLEGAL_ESCAPE: '"' ( '\\' [bfrnt"\\] | ~[\r\n"\\] )* '\\' ~[bfrnt"\\\r\n] { self.text = self.text[1:] };

UNCLOSE_STRING
    : '"' ( '\\' [bfrnt"\\] | ~[\r\n"\\] )* ( '\r'? '\n' | EOF )
      {
        self.text = self.text[1:]
        if self.text.endswith('\n'):
            self.text = self.text[:-1]
            if self.text.endswith('\r'):
                self.text = self.text[:-1]
      }
    ;

STRING_LITERAL: '"' ( '\\' [bfrnt"\\] | ~[\r\n"\\] )* '"' { self.text = self.text[1:-1] };

ERROR_CHAR: .;
