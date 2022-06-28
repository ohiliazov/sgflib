import re
from typing import Pattern, Match, List

from .exceptions import (
    SGFPropertyValueParseError,
    SGFPropertyParseError,
    SGFNodeParseError,
    SGFGameTreeParseError,
)
from .helpers import convert_control_chars
from .property import SGFProperty
from .node import SGFNode
from .game_tree import SGFGameTree

reGameTreeStart = re.compile(r"\s*\(")
reGameTreeEnd = re.compile(r"\s*\)")
reNodeStart = re.compile(r"\s*;")
rePropLabel = re.compile(r"\s*([a-zA-Z]+)(?=\s*\[)")
rePropValueStart = re.compile(r"\s*\[")
rePropValueEnd = re.compile(r"]")
reEscape = re.compile(r"\\[]\\]")
reLineBreak = re.compile(r"(\r\n?|\n\r?)*")


class SGFParser:
    def __init__(self, data: str, index: int = 0):
        self.data = data
        self.index = index

    def _match(self, pattern: Pattern) -> Match:
        return pattern.match(self.data, self.index)

    def _search(self, pattern: Pattern) -> Match:
        return pattern.search(self.data, self.index)

    def parse_game_trees(self) -> List[SGFGameTree]:
        """
        Parses multiple SGFGameTrees.

        Called when "(" encountered.
        Finishes when last ")" encountered.
        """
        trees = []
        try:
            while True:
                trees.append(self.parse_tree())
        except SGFGameTreeParseError:
            return trees

    def parse_tree(self) -> SGFGameTree:
        """
        Parses single SGFGameTree, which contains multiple SGFNodes and SGFGameTrees (variations).

        SGFGameTree example:
            - (;B[dd])
            - (;B[dd];W[pp](;B[dp];W[pd])(;B[pd];W[dp]))
        Called when "(" encountered.
        Finishes when ")" encountered.
        """
        match = self._match(reGameTreeStart)
        if not match:
            raise SGFGameTreeParseError("Expected `(` at the start of SGFGameTree.")

        # consume "("
        self.index = match.end()

        nodes = []
        try:
            while True:
                nodes.append(self.parse_node())
        except SGFNodeParseError:
            if not nodes:
                raise SGFGameTreeParseError("Expected at least one SGFNode.")

        variations = self.parse_game_trees()

        match = self._match(reGameTreeEnd)

        if not match:
            raise SGFGameTreeParseError("Expected `)` at the end of SGFGameTree.")

        # consume ")"
        self.index = match.end()

        return SGFGameTree(nodes, variations)

    def parse_node(self) -> SGFNode:
        """
        Parses single SGFNode, which contains multiple SGFPropertys.

        Called when ";" encountered.
        SGFNode ends when encountered one of the following:
            ";" - next SGFNode starts
            "(" - variation SGFGameTree starts
            ")" - SGFGameTree ends
        """
        match = self._match(reNodeStart)

        if not match:
            raise SGFNodeParseError("Expected `;` at the start of SGFNode.")

        # consume ";"
        self.index = match.end()

        # parse SGFPropertys till ";", "(" or ")"
        props = []
        try:
            while True:
                props.append(self.parse_prop())
        except SGFPropertyParseError:
            pass

        return SGFNode(props)

    def parse_prop(self) -> SGFProperty:
        """
        Parses single SGFProperty.

        Called when SGFProperty label encountered.
        Finishes when last SGFProperty value is parsed.
        """
        match = self._match(rePropLabel)

        if not match:
            raise SGFPropertyParseError(
                "Expected `[a-zA-Z]` at the start of SGFProperty."
            )

        # consume SGFProperty label
        self.index = match.end()

        prop_values = []
        try:
            while True:
                prop_values.append(self.parse_prop_value())
        except SGFPropertyValueParseError:
            if not prop_values:
                raise SGFPropertyParseError("Expected at least one SGFProperty value.")

        prop = SGFProperty(match.group(0), prop_values)
        return prop

    def parse_prop_value(self) -> str:
        """
        Parses single SGFProperty value.

        Called when "[" encountered.
        Finishes when matching "]" encountered.

        Skips all line breaks and unescapes "\\]".
        """
        match = self._match(rePropValueStart)

        if not match:
            raise SGFPropertyValueParseError(
                "Expected `[` at the start of SGFProperty value."
            )

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
                raise SGFPropertyValueParseError(
                    "Expected `]` at the end of SGFProperty value."
                )

            match_escape = self._search(reEscape)

            if not match_escape or match_escape.end() > match_end.end():
                # no more escaped characters in the SGFProperty value
                break

            # add contents of SGFProperty without `\\`
            data += (
                self.data[self.index : match_escape.start()]
                + self.data[match_escape.end() - 1]
            )
            self.index = match_escape.end()

        # add contents of SGFProperty value
        data += self.data[self.index : match_end.start()]

        # consume "]"
        self.index = match_end.end()

        return convert_control_chars(data)
