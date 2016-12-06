# Tests writing amber format with amber parameters
# Special isopeptide bond between two residues
import pytest
import subprocess, os

dir = os.path.dirname(__file__) + "/"
#==============================================================================

def test_amber_custom_residues(tmpdir):
    import vmd, molecule
    from atomsel import atomsel
    from Dabble.param import AmberWriter

    # Generate the file
    p = str(tmpdir.mkdir("3nob_custom"))
    molid = molecule.load("mae", dir + "prepped.mae")
    w = AmberWriter(molid, tmp_dir=p, forcefield="amber", hmr=False,
                    extra_topos=["glx.off", "lyx.off"],
                    extra_params=["join.frcmod", "analogies.frcmod"],
                    override_defaults=False)
    w.write("test")

    # Load the output file and start checking it
    m2 = molecule.load("parm7", "test.prmtop", "rst7", "test.inpcrd")
    molecule.set_top(m2)

    # Check the two custom residues are present
    assert(len(atomsel("resname GLX")) == 7)
    assert(len(atomsel("resname LYX")) == 20)

    # Check the custom residues have gaff2 atom types
    assert("n" in atomsel("resname LYX").get("type"))
    assert("n2" in atomsel("resname GLX").get("type"))

    # Check the normal residues have ff14SB atom types
    assert("N" in atomsel("resname LYS").get("type"))
    assert("N" in atomsel("resname GLY").get("type"))

    # Check that the isopeptide bond is there
    lybonds = []
    for x in atomsel("resname LYX").bonds:
        lybonds.extend(x)
    assert(any(x in lybonds for x in atomsel("resname GLX").get("index")))

#==============================================================================