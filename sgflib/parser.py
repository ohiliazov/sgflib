import re
from pathlib import Path
from typing import Pattern, Match, List, Type

from .exceptions import (
    SGFPropValueParseError,
    SGFPropParseError,
    SGFNodeParseError,
    SGFTreeParseError,
)
from .helpers import convert_control_chars
from .prop import SGFProp
from .node import SGFNode
from .tree import SGFTree

reGameTreeStart = re.compile(r"\s*\(")
reGameTreeEnd = re.compile(r'\s*\)')
reNodeStart = re.compile(r"\s*;")
rePropLabel = re.compile(r"\s*([a-zA-Z]+)(?=\s*\[)")
rePropValueStart = re.compile(r'\s*\[')
rePropValueEnd = re.compile(r']')
reEscape = re.compile(r'\\[]\\]')
reLineBreak = re.compile(r'(\r\n?|\n\r?)*')


class SGFParser:
    def __init__(self, data: str, index: int = 0):
        self.data = data
        self.index = index

    def _match(self, pattern: Pattern) -> Match:
        return pattern.match(self.data, self.index)

    def _search(self, pattern: Pattern) -> Match:
        return pattern.search(self.data, self.index)

    def parse_game_trees(self) -> List[SGFTree]:
        """
        Parses multiple SGFTrees.

        Called when "(" encountered.
        Finishes when last ")" encountered.
        """
        trees = []
        try:
            while True:
                trees.append(self.parse_tree())
        except SGFTreeParseError:
            return trees

    def parse_tree(self) -> SGFTree:
        """
        Parses single SGFTree, which contains multiple SGFNodes and SGFTrees (variations).

        SGFTree example:
            - (;B[dd])
            - (;B[dd];W[pp](;B[dp];W[pd])(;B[pd];W[dp]))
        Called when "(" encountered.
        Finishes when ")" encountered.
        """
        match = self._match(reGameTreeStart)
        if not match:
            raise SGFTreeParseError("Expected `(` at the start of SGFTree.")

        # consume "("
        self.index = match.end()

        nodes = []
        try:
            while True:
                nodes.append(self.parse_node())
        except SGFNodeParseError:
            if not nodes:
                raise SGFTreeParseError("Expected at least one SGFNode.")

        variations = self.parse_game_trees()

        match = self._match(reGameTreeEnd)

        if not match:
            raise SGFTreeParseError("Expected `)` at the end of SGFTree.")

        # consume ")"
        self.index = match.end()

        return SGFTree(nodes, variations)

    def parse_node(self) -> SGFNode:
        """
        Parses single SGFNode, which contains multiple SGFProps.

        Called when ";" encountered.
        SGFNode ends when encountered one of the following:
            ";" - next SGFNode starts
            "(" - variation SGFTree starts
            ")" - SGFTree ends
        """
        match = self._match(reNodeStart)

        if not match:
            raise SGFNodeParseError("Expected `;` at the start of SGFNode.")

        # consume ";"
        self.index = match.end()

        # parse SGFProps till ";", "(" or ")"
        props = []
        try:
            while True:
                props.append(self.parse_prop())
        except SGFPropParseError:
            pass

        return SGFNode(props)

    def parse_prop(self) -> SGFProp:
        """
        Parses single SGFProp.

        Called when SGFProp label encountered.
        Finishes when last SGFProp value is parsed.
        """
        match = self._match(rePropLabel)

        if not match:
            raise SGFPropParseError("Expected `[a-zA-Z]` at the start of SGFProp.")

        # consume SGFProp label
        self.index = match.end()

        prop_values = []
        try:
            while True:
                prop_values.append(self.parse_prop_value())
        except SGFPropValueParseError:
            if not prop_values:
                raise SGFPropParseError("Expected at least one SGFProp value.")

        prop = SGFProp(match.group(0), prop_values)
        return prop

    def parse_prop_value(self) -> str:
        """
        Parses single SGFProp value.

        Called when "[" encountered.
        Finishes when matching "]" encountered.

        Skips all line breaks and unescapes "\\]".
        """
        match = self._match(rePropValueStart)

        if not match:
            raise SGFPropValueParseError("Expected `[` at the start of SGFProp value.")

        # consume "["
        self.index = match.end()

        data = ""
        while True:
            # remove line breaks
            match_break = self._match(reLineBreak)
            if match_break:
                self.index = match_break.end()

            match_end = self._search(rePropValueEnd)
            if not match_end:
                raise SGFPropValueParseError("Expected `]` at the end of SGFProp value.")

            match_escape = self._search(reEscape)

            if not match_escape or match_escape.end() > match_end.end():
                # no more escaped characters in the SGFProp value
                break

            # add contents of SGFProp without `\\`
            data += self.data[self.index:match_escape.start()] + self.data[match_escape.end() - 1]
            self.index = match_escape.end()

        # add contents of SGFProp value
        data += self.data[self.index:match_end.start()]

        # consume "]"
        self.index = match_end.end()

        return convert_control_chars(data)
