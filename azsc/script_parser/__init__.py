import sys
import logging
import os 
from lark import Lark

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def run_parser(script, target, debug):
    if (debug == True):
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("AZ Script Compiler v 0.1")

    #os.path.join(os.path.split(__file__)[0], "monitor.js")
    logging.info("loading grammar")
    with open(os.path.join(__location__, os.path.join('..', 'grammar', 'azsc.lark')), 'r') as f:
        grammar = f.read()

    logging.info("loading script file")
    try:
        with open(script, 'r') as f:
            text = f.read()
    except IOError:
        error_message = "script {0} file not found".format(script)
        logging.error(error_message)
        return "ERROR: " + error_message

    logging.info("setting up parser")
    lark = Lark(grammar)

    logging.info("generating parse tree")
    tree = lark.parse(text)

    logging.debug("parse tree:\n" + tree.pretty())

    logging.info("importing parse tree transformer")
    from azsc.transformers.AZSTransformer import AZSTransformer

    logging.info("compiling")
    t = AZSTransformer()
    t.transform(tree)
    cmd = t.get_command()

    if (debug==True):
        logging.debug("context:")
        ctx = t.get_context()
        for c in ctx:
            logging.debug("\t[%s]=%s", str(c), str(ctx[c]))

    logging.info("done")   

    return cmd
