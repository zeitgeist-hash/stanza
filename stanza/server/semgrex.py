"""
Invokes the Java semgrex on a document
"""

import stanza
from stanza.protobuf import SemgrexRequest, SemgrexResponse
from stanza.server.java_protobuf_requests import send_request, add_token, add_word_to_graph

def send_semgrex_request(request):
    return send_request(request, SemgrexResponse,
                        "edu.stanford.nlp.semgraph.semgrex.ProcessSemgrexRequest")

def process_doc(doc, *semgrex_patterns):
    """
    Returns the result of processing the given semgrex expression on the stanza doc.

    Currently the return is a SemgrexResponse from CoreNLP.proto
    """
    request = SemgrexRequest()
    for semgrex in semgrex_patterns:
        request.semgrex.append(semgrex)

    for sent_idx, sentence in enumerate(doc.sentences):
        query = request.query.add()
        word_idx = 0
        for token in sentence.tokens:
            for word in token.words:
                add_token(query.token, word, token)
                add_word_to_graph(query.graph, word, sent_idx, word_idx)
                word_idx = word_idx + 1

    return send_semgrex_request(request)

def main():
    nlp = stanza.Pipeline('en',
                          processors='tokenize,pos,lemma,depparse')

    doc = nlp('Unban Mox Opal! Unban Mox Opal!')
    #print(doc.sentences[0].dependencies)
    print(doc)
    print(process_doc(doc, "{}=source >obj=zzz {}=target"))

if __name__ == '__main__':
    main()
