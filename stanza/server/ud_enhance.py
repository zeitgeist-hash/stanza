"""
Invoke the UniversalEnhancer module from corenlp
"""

import stanza
from stanza.protobuf import SemgrexRequest, SemgrexResponse
from stanza.server.java_protobuf_requests import send_request, add_token, add_word_to_graph

