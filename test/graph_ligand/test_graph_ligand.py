# Tests the MoleculeGraph functionality by readin in the 
# mae and str file, and matching up atoms

import pytest
import networkx as nx
import subprocess
from DabbleParam import MoleculeGraph, parse_vmd
import vmd
import molecule
from atomsel import atomsel

def test_read_str(capfd, tmpdir):
    """
    Tests if a str file can be properly read in
    """
    g = MoleculeGraph(["lsd_prot_trunc.str","masses.rtf"])
    nx.write_dot(g.known_res["LSD"], str(tmpdir)+"/test.dot")
    subprocess.check_call(["diff", "-q", "correct_str.dot", str(tmpdir)+"/test.dot"])

def test_read_mol(capfd, tmpdir):

    molid = molecule.load("mae", "lsd_prot.mae")
    rgraph = parse_vmd(atomsel())
    nx.write_dot(rgraph, str(tmpdir)+"/test2.dot")
    subprocess.check_call(["diff", "-q", "correct_mae.dot", str(tmpdir)+"/test2.dot"])

def test_compare_mol():
    molid = molecule.load("mae", "lsd_prot.mae")
    g = MoleculeGraph(["lsd_prot.str","masses.rtf"])
    (name, mdict) = g.get_names(atomsel())
    correctnames = {0: 'C13', 1: 'N2', 2: 'C12', 3: 'C11', 4: 'C15', 5: 'C7', 6: 'C3', 7: 'C8', 8: 'N1', 9: 'C1', 10: 'C4', 11: 'C5', 12: 'C2', 13: 'C6', 14: 'C9', 15: 'C10', 16: 'C14', 17: 'C16', 18: 'O1', 19: 'N3', 20: 'C17', 21: 'C18', 22: 'C19', 23: 'C20', 24: 'H131', 25: 'H132', 26: 'H121', 27: 'H122', 28: 'H123', 29: 'H11', 30: 'H151', 31: 'H8', 32: 'H4', 33: 'H5', 34: 'H2', 35: 'H10', 36: 'H14', 37: 'H171', 38: 'H172', 39: 'H181', 40: 'H182', 41: 'H183', 42: 'H191', 43: 'H192', 44: 'H201', 45: 'H202', 46: 'H203', 47: 'H152', 48: 'HN1', 49: 'HN2'}
    names = mdict.next()
    assert(name == "LSD")
    assert(names == correctnames)
    
