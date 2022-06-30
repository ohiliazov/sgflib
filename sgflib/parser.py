import re
from typing import Pattern, Match, List

from .exceptions import SGFParserError
from .utils import convert_control_chars
from .collection import SGFCollection
from .property import SGFProperty
from .node import SGFNode
from .sequence import SGFSequence
from .game_tree import SGFGameTree

reGameTreeStart = re.compile(r"\s*\(")
reGameTreeEnd = re.compile(r"\s*\)")
reNodeStart = re.compile(r"\s*;")
rePropLabel = re.compile(r"\s*([a-zA-Z]+)")
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

    def parse_collection(self) -> SGFCollection:
        """
        Parse multiple SGFGameTrees into SGFCollection.

        Called when "(" encountered.
        Finishes when last ")" encountered.
        """
        game_trees = self.parse_game_trees()

        if not game_trees:
            raise SGFParserError("Expecting SGFCollection", self.data, self.index)

        if self.index != len(self.data) and not self.data[self.index :].isspace():
            raise SGFParserError("Extra data", self.data, self.index)

        return SGFCollection(game_trees)

    def parse_game_trees(self) -> List[SGFGameTree]:
        """
        Parses multiple SGFGameTrees.

        Called when "(" encountered.
        Finishes when last ")" encountered.
        """
        trees = []
        try:
            while True:
                trees.append(self.parse_game_tree())
        except SGFParserError:
            return trees

    def parse_game_tree(self) -> SGFGameTree:
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
            raise SGFParserError("Expecting SGFGameTree", self.data, self.index)

        # consume "("
        self.index = match.end()

        sequence = self.parse_sequence()
        variations = self.parse_game_trees()

        match = self._match(reGameTreeEnd)

        if not match:
            raise SGFParserError("Unterminated SGFGameTree", self.data, self.index)

        # consume ")"
        self.index = match.end()

        return SGFGameTree(sequence, variations)

    def parse_sequence(self) -> SGFSequence:
        nodes = []
        try:
            while True:
                nodes.append(self.parse_node())
        except SGFParserError:
            if not nodes:
                raise SGFParserError("Expecting SGFSequence", self.data, self.index)
        return SGFSequence(nodes)

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
            raise SGFParserError("Expecting SGFNode", self.data, self.index)

        # consume ";"
        self.index = match.end()

        # parse SGFProperties till ";", "(" or ")"
        props = []
        try:
            while True:
                props.append(self.parse_property())
        except SGFParserError:
            pass

        return SGFNode.from_properties(props)

    def parse_property(self) -> SGFProperty:
        """
        Parses single SGFProperty.

        Called when SGFProperty label encountered.
        Finishes when last SGFProperty value is parsed.
        """
        match = self._match(rePropLabel)

        if not match:
            raise SGFParserError("Expecting SGFProperty", self.data, self.index)

        # consume SGFProperty label
        self.index = match.end()

        prop_values = []
        try:
            while True:
                prop_values.append(self.parse_prop_value())
        except SGFParserError as err:
            if not prop_values:
                raise err

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
            raise SGFParserError("Expecting SGFProperty value", self.data, self.index)

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
                raise SGFParserError(
                    "Unterminated SGFProperty value", self.data, self.index
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
