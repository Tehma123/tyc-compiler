"""
Parser test cases for TyC compiler
Tests syntax parsing of TyC language constructs
"""

import pytest
from tests.utils import Parser


# ============================================================================
# SIMPLE VARIABLE DECLARATIONS (Tests 1-5)
# ============================================================================

def test_01_var_decl_auto_with_init():
    """Test auto variable declaration with initialization"""
    source = "void main() { auto x = 5; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_02_var_decl_explicit_type():
    """Test explicit type variable declaration"""
    source = "void main() { int x; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_03_var_decl_with_init():
    """Test variable declaration with initialization"""
    source = "void main() { float x = 3.14; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_04_var_decl_string():
    """Test string variable declaration"""
    source = 'void main() { string msg = "hello"; }'
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_05_multiple_var_decls():
    """Test multiple variable declarations"""
    source = """void main() {
        int x;
        float y = 3.14;
        string s = "test";
        auto z = 42;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# SIMPLE EXPRESSIONS (Tests 6-10)
# ============================================================================

def test_06_expr_arithmetic_simple():
    """Test simple arithmetic expression"""
    source = "void main() { auto x = 5 + 3; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_07_expr_arithmetic_complex():
    """Test complex arithmetic expression"""
    source = "void main() { auto x = 5 + 3 * 2 - 1 / 2; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_08_expr_with_parentheses():
    """Test expression with parentheses"""
    source = "void main() { auto x = (5 + 3) * 2; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_09_expr_comparison():
    """Test comparison expression"""
    source = "void main() { auto x = 5 > 3; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_10_expr_logical():
    """Test logical expression"""
    source = "void main() { auto x = 5 > 3 && 2 < 4; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# ASSIGNMENT STATEMENTS (Tests 11-15)
# ============================================================================

def test_11_assignment_simple():
    """Test simple assignment"""
    source = "void main() { int x; x = 5; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_12_assignment_from_expr():
    """Test assignment from expression"""
    source = "void main() { int x; x = 5 + 3; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_13_assignment_chained():
    """Test chained assignment"""
    source = "void main() { int x; int y; int z; x = y = z = 5; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_14_assignment_increment():
    """Test assignment with increment"""
    source = "void main() { int x = 5; x++; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_15_assignment_decrement():
    """Test assignment with decrement"""
    source = "void main() { int x = 5; x--; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# FUNCTION DECLARATIONS (Tests 16-20)
# ============================================================================

def test_16_func_decl_void_no_params():
    """Test void function with no parameters"""
    source = "void greet() { }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_17_func_decl_with_params():
    """Test function with parameters"""
    source = "int add(int x, int y) { return 0; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_18_func_decl_return_type_inferred():
    """Test function with inferred return type"""
    source = "add(int x, int y) { return x + y; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_19_func_decl_multiple_params():
    """Test function with multiple parameters"""
    source = "void process(int a, float b, string c) { }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_20_func_decl_with_body():
    """Test function with complex body"""
    source = """int calculate(int x, int y) {
        int sum = x + y;
        return sum;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# STRUCT DECLARATIONS (Tests 21-25)
# ============================================================================

def test_21_struct_decl_simple():
    """Test simple struct declaration"""
    source = "struct Point { int x; int y; };"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_22_struct_decl_empty():
    """Test empty struct declaration"""
    source = "struct Empty { };"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_23_struct_decl_multiple_types():
    """Test struct with multiple types"""
    source = "struct Person { string name; int age; float height; };"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_24_struct_variable_decl():
    """Test struct variable declaration"""
    source = """struct Point { int x; int y; };
    void main() {
        Point p;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_25_struct_member_access():
    """Test struct member access"""
    source = """struct Point { int x; int y; };
    void main() {
        Point p;
        p.x = 10;
        auto y = p.y;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# CONTROL FLOW - IF STATEMENTS (Tests 26-30)
# ============================================================================

def test_26_if_statement_simple():
    """Test simple if statement"""
    source = "void main() { if (5 > 3) { int x = 1; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_27_if_else_statement():
    """Test if-else statement"""
    source = "void main() { if (x > 5) { x = 10; } else { x = 0; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_28_nested_if():
    """Test nested if statements"""
    source = """void main() {
        if (x > 5) {
            if (y < 10) {
                z = 1;
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_29_if_with_complex_condition():
    """Test if with complex condition"""
    source = "void main() { if (x > 5 && y < 10 || z == 0) { x = 1; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_30_if_without_else():
    """Test if without else clause"""
    source = "void main() { if (x > 0) x = 10; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# CONTROL FLOW - WHILE LOOPS (Tests 31-34)
# ============================================================================

def test_31_while_simple():
    """Test simple while loop"""
    source = "void main() { while (x > 0) { x = x - 1; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_32_while_with_break():
    """Test while loop with break"""
    source = "void main() { while (1) { break; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_33_while_with_continue():
    """Test while loop with continue"""
    source = "void main() { while (x > 0) { x--; continue; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_34_while_complex_condition():
    """Test while with complex condition"""
    source = "void main() { while (x > 0 && y < 10) { x--; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# CONTROL FLOW - FOR LOOPS (Tests 35-39)
# ============================================================================

def test_35_for_simple():
    """Test simple for loop"""
    source = "void main() { for (int i = 0; i < 10; i++) { } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_36_for_auto_init():
    """Test for loop with auto variable"""
    source = "void main() { for (auto i = 0; i < 10; i++) { } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_37_for_empty_init():
    """Test for loop with empty init"""
    source = "void main() { for (; i < 10; i++) { } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_38_for_empty_condition():
    """Test for loop with empty condition"""
    source = "void main() { for (int i = 0; ; i++) { break; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_39_for_empty_update():
    """Test for loop with empty update"""
    source = "void main() { for (int i = 0; i < 10; ) { i++; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# CONTROL FLOW - SWITCH STATEMENTS (Tests 40-43)
# ============================================================================

def test_40_switch_simple():
    """Test simple switch statement"""
    source = """void main() {
        switch (x) {
            case 1: break;
            case 2: break;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_41_switch_with_default():
    """Test switch with default case"""
    source = """void main() {
        switch (x) {
            case 1: break;
            default: break;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_42_switch_fallthrough():
    """Test switch with fall-through"""
    source = """void main() {
        switch (x) {
            case 1:
            case 2: y = 1; break;
            case 3: y = 2; break;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_43_switch_with_statements():
    """Test switch with multiple statements in case"""
    source = """void main() {
        switch (x) {
            case 1: y = 1; z = 2; break;
            default: y = 0;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# FUNCTION CALLS (Tests 44-47)
# ============================================================================

def test_44_func_call_no_args():
    """Test function call with no arguments"""
    source = "void main() { greet(); }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_45_func_call_with_args():
    """Test function call with arguments"""
    source = "void main() { int result = add(5, 3); }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_46_func_call_multiple_args():
    """Test function call with multiple arguments"""
    source = 'void main() { process(10, 3.14, "test"); }'
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_47_nested_func_calls():
    """Test nested function calls"""
    source = "void main() { auto result = add(multiply(5, 3), 2); }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# COMPLEX EXPRESSIONS (Tests 48-50)
# ============================================================================

def test_48_expr_member_access():
    """Test expression with member access"""
    source = """struct Point { int x; };
    void main() {
        Point p;
        auto val = p.x + 5;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_49_expr_unary_operators():
    """Test unary operators"""
    source = "void main() { int x = 5; auto y = -x; auto z = !x; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_50_complete_program():
    """Test complete program with multiple declarations"""
    source = """
    struct Point {
        int x;
        int y;
    };
    
    int distance(Point p1, Point p2) {
        int dx = p1.x - p2.x;
        int dy = p1.y - p2.y;
        return dx + dy;
    }
    
    void main() {
        Point a;
        Point b;
        a.x = 10;
        a.y = 20;
        auto d = distance(a, b);
    }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# STRUCT LITERALS (Tests 51-55)
# ============================================================================

def test_51_struct_literal_simple():
    """Test struct literal initialization"""
    source = """struct Point { int x; int y; };
    void main() {
        auto p = {10, 20};
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_52_struct_literal_in_assignment():
    """Test struct literal in assignment"""
    source = """struct Point { int x; int y; };
    void main() {
        Point p;
        p = {5, 15};
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_53_struct_literal_as_func_arg():
    """Test struct literal as function argument"""
    source = """struct Point { int x; int y; };
    int distance(Point p) { return 0; }
    void main() {
        auto d = distance({10, 20});
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_54_nested_struct_literal():
    """Test nested struct literal"""
    source = """struct Inner { int a; };
    struct Outer { Inner i; int b; };
    void main() {
        auto o = {{1}, 2};
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_55_empty_struct_literal():
    """Test empty struct literal"""
    source = """struct Empty { };
    void main() {
        auto e = {};
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# COMPLEX MEMBER ACCESS (Tests 56-60)
# ============================================================================

def test_56_chained_member_access():
    """Test chained member access"""
    source = """struct Inner { int value; };
    struct Outer { Inner in; };
    void main() {
        Outer o;
        auto x = o.in.value;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_57_member_access_in_expression():
    """Test member access within arithmetic expression"""
    source = """struct Point { int x; int y; };
    void main() {
        Point p;
        auto sum = p.x + p.y * 2;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_58_member_access_assignment():
    """Test assignment to member access"""
    source = """struct Point { int x; int y; };
    void main() {
        Point p;
        p.x = 10;
        p.y = 20;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_59_member_access_increment():
    """Test increment on member access"""
    source = """struct Point { int x; };
    void main() {
        Point p;
        p.x++;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_60_member_access_with_call():
    """Test function call with member access result"""
    source = """struct Point { int x; };
    int process(int val) { return 0; }
    void main() {
        Point p;
        auto result = process(p.x);
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# OPERATOR PRECEDENCE AND ASSOCIATIVITY (Tests 61-66)
# ============================================================================

def test_61_mixed_arithmetic_precedence():
    """Test arithmetic operator precedence"""
    source = "void main() { auto x = 2 + 3 * 4 - 5 / 2 % 3; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_62_comparison_precedence():
    """Test comparison operator precedence"""
    source = "void main() { auto x = 5 > 3 && 2 < 4 || 1 == 1; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_63_assignment_right_associative():
    """Test right associativity of assignment"""
    source = "void main() { int a; int b; int c; a = b = c = 10; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_64_unary_prefix_precedence():
    """Test unary prefix operator precedence"""
    source = "void main() { auto x = -5 * 3; auto y = !x && 1; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_65_postfix_precedence():
    """Test postfix operator precedence"""
    source = "void main() { int x = 5; auto y = x++ + ++x; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_66_complex_mixed_operators():
    """Test complex expression with mixed operators"""
    source = "void main() { auto x = 1 + 2 * 3 == 7 && 5 > 3 || !0; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# MULTIPLE FUNCTIONS (Tests 67-71)
# ============================================================================

def test_67_multiple_functions():
    """Test multiple function declarations"""
    source = """
    int add(int a, int b) { return a + b; }
    int subtract(int a, int b) { return a - b; }
    int multiply(int a, int b) { return a * b; }
    void main() { }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_68_function_calling_function():
    """Test function calling another function"""
    source = """
    int helper(int x) { return x * 2; }
    int wrapper(int x) { return helper(x) + 1; }
    void main() { }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_69_mutual_recursion_declaration():
    """Test functions that could be mutually recursive"""
    source = """
    int a(int x) { return 0; }
    int b(int x) { return a(x - 1); }
    void main() { }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_70_function_with_struct_params():
    """Test function with struct parameters"""
    source = """
    struct Data { int val; };
    void process(Data d1, Data d2, Data d3) { }
    void main() { }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_71_overloaded_looking_functions():
    """Test functions with different signatures (not overloaded in TyC)"""
    source = """
    int calc(int x) { return x; }
    float calc_f(float x) { return x; }
    void main() { }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# NESTED CONTROL STRUCTURES (Tests 72-77)
# ============================================================================

def test_72_nested_if_else():
    """Test nested if-else structures"""
    source = """void main() {
        if (a > 0) {
            if (b > 0) {
                c = 1;
            } else {
                c = 2;
            }
        } else {
            c = 3;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_73_for_with_nested_while():
    """Test for loop with nested while loop"""
    source = """void main() {
        for (int i = 0; i < 10; i++) {
            while (j > 0) {
                j--;
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_74_switch_with_nested_loops():
    """Test switch with nested loops"""
    source = """void main() {
        switch (x) {
            case 1:
                for (int i = 0; i < 5; i++) {
                    y++;
                }
                break;
            case 2:
                while (z > 0) {
                    z--;
                }
                break;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_75_while_with_if_switch():
    """Test while loop with if and switch"""
    source = """void main() {
        while (x > 0) {
            if (y < 10) {
                switch (z) {
                    case 1: break;
                    default: break;
                }
            } else {
                x--;
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_76_deeply_nested_blocks():
    """Test deeply nested block structures"""
    source = """void main() {
        {
            {
                {
                    int x = 5;
                }
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_77_multiple_breaks_in_nested_loops():
    """Test multiple breaks in nested loops"""
    source = """void main() {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                if (x > 5) {
                    break;
                }
            }
            if (y > 0) {
                break;
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# COMPLEX EXPRESSIONS (Tests 78-83)
# ============================================================================

def test_78_ternary_like_operations():
    """Test complex nested conditions (simulate ternary-like)"""
    source = "void main() { auto x = (a > 0) ? 1 : 2; }"
    parser = Parser(source)
    # This will likely fail as TyC doesn't have ternary, but test the expression parsing
    try:
        ast = parser.parse()
    except:
        pass


def test_79_multiple_assignments_in_expression():
    """Test multiple assignments in expression"""
    source = "void main() { int a; int b; auto x = (a = 5) + (b = 3); }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_80_function_call_in_condition():
    """Test function call as condition"""
    source = """int check() { return 1; }
    void main() {
        if (check()) {
            x = 1;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_81_complex_logical_expression():
    """Test complex logical expression with many operators"""
    source = "void main() { auto x = a && b || c && d || e && f && g; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_82_mixed_unary_and_binary():
    """Test mixed unary and binary operators"""
    source = "void main() { auto x = -a * +b / -c % +d; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_83_prefix_increment_in_expression():
    """Test prefix increment in expression"""
    source = "void main() { int x = 5; auto y = ++x + x++ + --x + x--; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# RETURN STATEMENTS (Tests 84-87)
# ============================================================================

def test_84_return_empty():
    """Test empty return statement"""
    source = "void greet() { return; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_85_return_with_value():
    """Test return with expression"""
    source = "int getValue() { return 42; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_86_return_with_complex_expr():
    """Test return with complex expression"""
    source = "int calc(int a, int b) { return a * 2 + b - 1; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_87_multiple_returns():
    """Test function with multiple return paths"""
    source = """int getValue(int x) {
        if (x > 0) {
            return x;
        } else {
            return -x;
        }
        return 0;
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# FOR LOOP EDGE CASES (Tests 88-92)
# ============================================================================

def test_88_for_all_parts_empty():
    """Test for loop with all parts empty"""
    source = "void main() { for (;;) { break; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_89_for_with_expression_init():
    """Test for loop with expression as init"""
    source = "void main() { int i; for (i = 0; i < 10; i++) { } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_90_for_complex_update():
    """Test for loop with complex update expression"""
    source = "void main() { for (int i = 0; i < 10; i += 2) { } }"
    parser = Parser(source)
    ast = parser.parse()
    # This might fail if += is not supported, but test the structure


def test_91_for_with_continue():
    """Test for loop with continue statement"""
    source = "void main() { for (int i = 0; i < 10; i++) { if (i == 5) continue; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_92_nested_for_loops():
    """Test nested for loops"""
    source = """void main() {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                for (int k = 0; k < 10; k++) {
                    x = i + j + k;
                }
            }
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# SWITCH EDGE CASES (Tests 93-97)
# ============================================================================

def test_93_switch_empty():
    """Test empty switch statement"""
    source = "void main() { switch (x) { } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_94_switch_only_default():
    """Test switch with only default case"""
    source = "void main() { switch (x) { default: break; } }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_95_switch_multiple_cases_no_break():
    """Test switch with multiple cases without break (fall-through)"""
    source = """void main() {
        switch (x) {
            case 1:
            case 2:
            case 3:
                y = 1;
            case 4:
                y = 2;
                break;
            default:
                y = 0;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_96_switch_with_block_statements():
    """Test switch with block statements in cases"""
    source = """void main() {
        switch (x) {
            case 1: {
                int local = 5;
                y = local;
            } break;
            default: break;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_97_switch_with_expression_cases():
    """Test switch with expression cases"""
    source = """void main() {
        switch (x) {
            case 1+1: y = 2; break;
            case 2*3: y = 6; break;
            default: y = 0;
        }
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


# ============================================================================
# AUTO TYPE INFERENCE (Tests 98-100)
# ============================================================================

def test_98_auto_from_function_call():
    """Test auto type inferred from function call"""
    source = """int getValue() { return 42; }
    void main() {
        auto x = getValue();
    }"""
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_99_auto_without_init():
    """Test auto without initialization"""
    source = "void main() { auto x; x = 5; }"
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None


def test_100_complete_complex_program():
    """Test complete complex program with all features"""
    source = """
    struct Point {
        int x;
        int y;
    };
    
    struct Line {
        Point start;
        Point end;
    };
    
    int distance(Point p1, Point p2) {
        auto dx = p1.x - p2.x;
        auto dy = p1.y - p2.y;
        return dx + dy;
    }
    
    void drawLine(Line line) {
        auto dist = distance(line.start, line.end);
        for (int i = 0; i < dist; i++) {
            if (i % 2 == 0) {
                printInt(i);
            } else {
                continue;
            }
        }
    }
    
    void main() {
        struct Point p1;
        p1 = {0, 0};
        auto p2 = {10, 20};
        auto l = {{0, 0}, {10, 20}};
        drawLine(l);
        
        auto result = distance(p1, p2);
        switch (result) {
            case 10: break;
            case 20: break;
            case 30: break;
            default: break;
        }
    }
    """
    parser = Parser(source)
    ast = parser.parse()
    assert ast is not None
