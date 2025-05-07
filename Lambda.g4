grammar Lambda;

prog: expr EOF;

expr
    : atom                                 # AtomExpr
    | abstraction                          # AbstractionExpr
    | expr expr                            # ApplicationExpr
    | '(' expr ')'                         # ParenExpr
    | 'if' expr 'then' expr 'else' expr    # IfExpr
    | 'let' ID '=' expr 'in' expr          # LetExpr
    | expr op=('*'|'/'|'%') expr           # MulDivExpr
    | expr op=('+'|'-') expr               # AddSubExpr
    | expr op=('<'|'>'|'<='|'>='|'=='|'!=') expr # ComparisonExpr
    | op=('not'|'!') expr                  # NotExpr
    | expr op=('and'|'&&') expr            # AndExpr
    | expr op=('or'|'||') expr             # OrExpr
    | '[' (expr (',' expr)*)? ']'          # ListExpr
    | '[' expr ',' expr '..' expr ']'      # FullRangeExpr
    | '[' expr '..' expr ']'               # SimpleRangeExpr
    | '(' (expr (',' expr)+)? ')'          # TupleExpr
    ;

abstraction
    : ('λ' | '\\') ID+ '.' expr
    ;

atom
    : ID
    | NUMBER
    | BOOLEAN
    | STRING
    ;

BOOLEAN: 'true' | 'false';
NUMBER: '-'? [0-9_]+ ('.' [0-9]+)? ([eE] [-+]? [0-9]+)?;
STRING: '"' ( ~["\\] | '\\' ["\\] )* '"';
ID: [a-zA-Z_] [a-zA-Z0-9_]*;
WS: [ \t\n\r]+ -> skip;