'''
a script to automate the design of inverted PCR for telomere characterisation in Streptomyces
version 2 uses primer3 for improved primer design

Uage: python autofan2.py <path_to_genbank_file>

if you find this script helpful, please cite:
    Faurdal D et al.,
    Tying up loose ends: Recovering thousands of missing telomeres from Streptomyces and
    other Streptomycetaceae genomes. BioRxiv, 2025

for the origional protcol see:
    Fan Y et al., A self-ligation method for PCR-sequencing the telomeres of Streptomyces
    and Mycobacterium linear replicons.
    J Microbiol Methods. 2012

    and;

    Algora-Gallardo L et al.,
    Bilateral symmetry of linear streptomycete chromosomes.
    Microb Genom. 2021

Written by T.J.B.
'''

import os
from sys import argv
from typing import Tuple

from Bio import Seq, SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Restriction import RestrictionBatch

import primer3 as p3

def print_primer_line(seq: str, tm: float, name: str) -> None:
    '''
    print the primer details to the console
        arguments:
            seq: the primer sequence
            tm: the primer melting temperature
            name: the name of the primer
        returns:
            None
    '''
    primer_line = [
        name,
        seq,
        str(len(seq)),
        str(tm)
        ]
    print(",".join(primer_line))

def design_primers(template: Seq.Seq, name: str) -> None:
    '''
    design primers for inverse PCR using pydna
    during the experiment, DNA is circularised therefore,
    this function rotates the sequence to design PCR primers over the ends
            arguments:
                    template: a biopython Seq sequence
                    name: a string identifier to name the primers
            returns:
                    None
    '''
    template = str(template)
    centroid = len(template)//2
    rotated_template = template[centroid:] + template[:centroid]
    try:
        results = p3.bindings.design_primers(
        seq_args={
            "SEQUENCE_TEMPLATE": rotated_template
        },
        global_args={
            #"PRIMER_PICK_LEFT_PRIMER": 0,
            "PRIMER_OPT_SIZE": 20,
            "PRIMER_MIN_SIZE": 12,
            "PRIMER_MAX_SIZE": 25,
            "PRIMER_OPT_TM": 58.0,
            "PRIMER_MIN_TM": 50.0,
            "PRIMER_MAX_TM": 70.0,
            "PRIMER_MAX_POLY_X": 3,
            "PRIMER_NUM_RETURN": 10,
            "PRIMER_PRODUCT_OPT_SIZE": 200,
            "PRIMER_PRODUCT_SIZE_RANGE": [[centroid, 2000]]
            },
        )
        print_primer_line(
            results["PRIMER_LEFT_0_SEQUENCE"], results["PRIMER_LEFT_0_TM"], name + "_F"
            )
        print_primer_line(
            results["PRIMER_RIGHT_0_SEQUENCE"], results["PRIMER_RIGHT_0_TM"], name + "_R"
            )
    except  OSError:
        print(f"No good primers found for {name}")

def digest(record: SeqRecord) -> Tuple[Seq.Seq, Seq.Seq]:
    '''
    simulate digestion of linear chromosomes with blunt cutters
        arguments:
            record: biopython SeqRecord of a linear replicon
        returns:
           left_fragment: left fragment of linear digest
           right_fragment: right fragment of linear digest
    '''
    cutters = RestrictionBatch(["SmaI", "PvuII"])
    cuts = cutters.search(record.seq)
    cut_positions = sorted(
        [pos for positions in cuts.values() for pos in positions]
        ) #to extract from dict
    left_fragment = record.seq[0:cut_positions[0]]
    right_fragment = record.seq[cut_positions[-1]:-1]
    return left_fragment, right_fragment

def main(genome_path: str) -> None:
    '''
    main routine for autofan.py
        arguments:
            genome_path: path to genome as string
        returns:
            None
    '''
    records = SeqIO.parse(genome_path, "genbank")
    counter = 0
    for record in records:
        record_name = os.path.splitext(
            os.path.basename(genome_path)
        )[0] + "_" + str(counter)
        left_fragment, right_fragment = digest(record)
        design_primers(
            left_fragment, record_name + "_left"
        )
        design_primers(
            right_fragment, record_name + "_right"
        )
        counter +=1

GENOME_PATH = argv[1]
main(GENOME_PATH)

