import pathlib
import sys
import os
import argparse
import glob

root = '/work/yl708/pdbbind/refined-set/'
pdb_files = glob.glob(root + '*/*.pdb')

for pdb_file in pdb_files:
    working_directory = pdb_file[:pdb_file.rfind('/') + 1]
    pdb_name = pdb_file[pdb_file.rfind('/') + 1: pdb_file.rfind('_')]
    protein_name = pdb_name + '_protein'
    ligand_name = pdb_name + '_ligand'

    s = """#!/bin/bash
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=yl708@duke.edu     # Where to send mail:
#SBATCH --partition=scavenger
#SBATCH --time='1:00:00'
#SBATCH --exclusive
#SBATCH --chdir='/work/yl708/algebraic-topology-biomolecules'
#SBATCH --mem=4G

source ~/.bashrc
source ~/.bash_profile
date
hostname
conda activate /work/yl708/algebraic-topology-biomolecules/algtop-environment

module load R/4.1.1-rhel8
module load Matlab

"""
    s += '\n/work/yl708/algebraic-topology-biomolecules/algtop-environment/bin/python homology.py ' + '--working_dir ' + working_directory + ' --protein_name ' + protein_name + ' --ligand_name ' + ligand_name + '\n'

    filename = pdb_name + '_homology.sh'

    with open(filename, 'w') as script:
        script.write(s)

    os.system('sbatch ' + filename)
    os.system('rm ' + filename)
    break

