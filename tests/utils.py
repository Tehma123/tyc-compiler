"""
Utility functions and classes for testing TyC compiler
"""

import os
import sys

# Add project root and build directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
build_dir = os.path.join(project_root, "build")
sys.path.insert(0, project_root)
sys.path.insert(0, build_dir)

from build.TyCLexer import TyCLexer
from build.TyCParser import TyCParser
from antlr4 import InputStream, CommonTokenStream
from src.utils.error_listener import NewErrorListener


class ASTGenerator:
    """Class to generate AST from TyC source code."""

    def __init__(self, input_string: str):
        self.input_string = input_string
        self.input_stream = InputStream(input_string)
        self.lexer = TyCLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = TyCParser(self.token_stream)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(NewErrorListener.INSTANCE)
        # Import here to avoid circular dependency issues during build
        try:
            from src.astgen.ast_generation import ASTGeneration

            self.ast_generator = ASTGeneration()
        except ImportError:
            self.ast_generator = None

    def generate(self):
        """Generate AST from the input string."""
        if self.ast_generator is None:
            return "AST Generation Error: ASTGeneration class not found. Please implement src/astgen/ast_generation.py"
        try:
            # Parse the program starting from the entry point
            parse_tree = self.parser.program()

            # Generate AST using the visitor
            ast = self.ast_generator.visit(parse_tree)
            return ast
        except Exception as e:
            return f"AST Generation Error: {str(e)}"


class Tokenizer:
    """Lexer wrapper for testing"""

    def __init__(self, source_code: str):
        self.source_code = source_code

    def get_tokens_as_string(self) -> str:
        """Get tokens as comma-separated string (only token text)"""
        input_stream = InputStream(self.source_code)
        lexer = TyCLexer(input_stream)

        tokens = []
        try:
            while True:
                token = lexer.nextToken()
                if token.type == -1:  # EOF
                    tokens.append("<EOF>")
                    break
                tokens.append(token.text if token.text else "")
        except Exception as e:
            # If we already have some tokens, append error message
            if tokens:
                tokens.append(str(e))
            else:
                # If no tokens yet, just return error message
                return str(e)

        return ",".join(tokens)

    def tokenize(self):
        """Return a list of token-like objects with `.type` (symbolic name) and `.text`.

        Filters out whitespace and comment tokens so tests see only meaningful tokens.
        Any lexer exceptions (IllegalEscape, UncloseString, ErrorToken) are allowed
        to propagate to the caller (tests expect them).
        """
        from types import SimpleNamespace
        from src.grammar.lexererr import ErrorToken, IllegalEscape, UncloseString

        input_stream = InputStream(self.source_code)
        lexer = TyCLexer(input_stream)

        def extract_unclosed_text() -> str:
            start = self.source_code.find('"')
            if start == -1:
                return ""
            rest = self.source_code[start + 1 :]
            for idx, ch in enumerate(rest):
                if ch in "\r\n":
                    return rest[:idx]
            return rest

        def rethrow_lexer_error(err: Exception) -> None:
            msg = str(err)
            if msg.startswith("Illegal Escape In String: "):
                raise IllegalEscape(msg[len("Illegal Escape In String: ") :])
            if msg.startswith("Unclosed String: "):
                raise UncloseString(msg[len("Unclosed String: ") :])
            if msg.startswith("Error Token "):
                token_text = msg[len("Error Token ") :]
                if token_text == '"' and self.source_code.count('"') % 2 == 1:
                    raise UncloseString(extract_unclosed_text())
                raise ErrorToken(token_text)
            raise err

        result = []
        try:
            while True:
                tok = lexer.nextToken()
                if tok.type == -1:
                    break
                # Skip whitespace and comments
                if tok.type in (TyCLexer.WS, TyCLexer.LINE_COMMENT, TyCLexer.BLOCK_COMMENT):
                    continue
                # Map numeric type to symbolic name when available
                try:
                    type_name = TyCLexer.symbolicNames[tok.type]
                except Exception:
                    type_name = str(tok.type)

                result.append(SimpleNamespace(type=type_name, text=(tok.text or "")))
        except Exception as err:
            rethrow_lexer_error(err)

        return result


class Parser:
    """Parser wrapper for testing"""

    def __init__(self, source_code: str):
        self.source_code = source_code

    def parse(self) -> str:
        """Parse source code and return result"""
        input_stream = InputStream(self.source_code)
        lexer = TyCLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = TyCParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(NewErrorListener.INSTANCE)

        try:
            tree = parser.program()
            return "success"
        except Exception as e:
            return str(e)
