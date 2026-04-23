#!/usr/bin/env python3

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

random.seed(314159)


@dataclass
class Candidate:
    category: str
    name: str
    sequence: str
    # 0-based preferred mutation positions for local second-gen search
    focus_positions: List[int]


CANDIDATES = [
    Candidate(
        category="alpha_glycans",
        name="alpha_glycans__mut06",
        sequence=(
            "MATIFFCSFKLPLFFLPFLLPYANSLSFQISRFEPNASNILYQGEAGPSDGAIEMNTIDYSYRVGRATYA"
            "ERVPLWDSNTGNISDFTTHFSFIIDTLGQDIYSDGLAFFLAPVGFEISPNSAGGYLGLFNFTTKNSSQNQ"
            "IVLVEFDSYANPEWDPPVEHVGININSLSSAVSTPWNASFHSGDIANVWITYNASTKNLSVSWSYSRTSN"
            "SQENTTLSYDIDLPKILPEWVTIGFSAAFGLYSNRHTLLSWEFSSSLDIKETSGKKAKNTRLIMSLTVSS"
            "GILIVGLIIAFAIFWRHKQKRRKTAEMVNLTSINEDLEGGVGPRKFSYNELVSATYNFLNERKLGEGGFG"
            "AVYKGYLTDLTPIAVKKISRGLNRGRKNTSPK"
        ),
        # around the two beneficial local changes
        focus_positions=[274, 275, 276, 277, 278, 279, 315, 316, 317, 318, 319],
    ),
    Candidate(
        category="endoglucanases",
        name="endoglucanases__mut06",
        sequence=(
            "MALSSHFLLLCSLLFFIISPSIAQTSFRPKALVLPVSKDPSTLQYITKINQRTPLVPINLTLDVGGKFSW"
            "VDCEQGYVSSTYKPVRCRSAQCSLARSRSCITECYSPPRPGCNNNTCGVLPDNPFSRTGTGGELGQDVVQ"
            "VQSTDGFNPTRVVSVPSLIFTCANTFLLEGLASGVKGIAGLGRTKISLPSQFSAAFSFHRKFAVCLTSST"
            "RANGVVFFGDGPYVLLPNIEVSKNLIYTPLILNPVSTASAYFAGEPSADYFIGVKSIKINGKVVKFNATL"
            "LSINKEGYGGTKISSVNPYTVMESTIYNAVINAFVRELSSVSRVAAVAPFGACFNGKEIGSTRVGPAVPQ"
            "IDLVLQSESVYWRIFGANSMVQVSSDVLCLGFVDGGVDPRTSIVIGGHQIEDNLLQFDLASSRLGFSSSL"
            "LFRQTTCANFNFTSKL"
        ),
        focus_positions=[138, 139, 140, 141, 142, 143, 184, 185, 186, 187, 188],
    ),
    Candidate(
        category="hemicelluloses",
        name="hemicelluloses__mut07",
        sequence=(
            "AGKTGQMTVFWGRNKNEGTLKETCDTGLYTTVVISFYSVFGHGRYWGDLSGHDLRVIGADIKHCQSKNIF"
            "VFLSIGGAGKDYSLPTSKSAADVADNIWNAHMDGRRPGVFRPFGDAAVDGIDFFIDQGAPDHYDDLARNL"
            "YAYQSTSASKRVLRLTATVRCAFPDPRMKKALDTKLFERIHVRFYDDATCSYNHAGLAGVMAQWNKWTAR"
            "YPGSHVYLGLAAANVPGKNDNVFIKQLYYDLLPNVQKAKNYGGIMLWDRFYDKQTGYGKTVKYWA"
        ),
        # still only hotspot
        focus_positions=[192, 193, 194, 195, 196, 197, 198, 199, 200],
    ),
    Candidate(
        category="polygalacturonases",
        name="polygalacturonases__mut01",
        sequence=(
            "MARLSITVLIMVLFCRTALSELCNPQDKQALLQIKKELGNPTTLSSWLPNTDCCNPQWEGVSCDIDTKTY"
            "RVNSLDLTDLSLPKPYPIPSSVANLPYLSFLYISRINNLVGPISPSIAKLTKLRYLYITHTNVSGQIPHF"
            "LSQMKTLLTIDFSYNALSGTLPPSLSSLPNLLGISFDGNHISGAIPDSFGSFPKHFTVLTLSRNRLTGKI"
            "PATLAKLDLAFVDLSQNMLEGQASVLFGAKKERLQKINLAKNLLAFDLGKIRLSKSQDLGGLDLRNNRIY"
            "GNLPKVLTSFKYLKRLNVSYNDLCGEIPQGGKLQRFDESCYAHNKCLCGSPLPSCT"
        ),
        focus_positions=[280, 281, 282, 283, 284, 285, 317, 318, 319, 320, 321, 322, 352, 353, 354],
    ),
]


MUTATION_POOLS = {
    "D": "ENKQAST",
    "E": "DNKQAST",
    "K": "RQAEDNST",
    "R": "KQAEDNST",
    "N": "QDSTKRA",
    "Q": "NESTKRA",
    "S": "TNADEQK",
    "T": "SNADEQK",
    "Y": "FHSN",
    "F": "YWL",
    "H": "YNQKR",
    "A": "STVQ",
    "V": "AILT",
    "L": "IVMTF",
    "I": "VLMTF",
    "M": "LIVT",
    "W": "FYH",
}

AVOID = set("CPG")


def choose_mutant_residue(wt: str) -> str:
    pool = MUTATION_POOLS.get(wt, "ASTNQKRDE")
    choices = [x for x in pool if x != wt]
    return random.choice(choices)


def valid_focus_positions(seq: str, positions: List[int]) -> List[int]:
    out = []
    for pos in positions:
        if pos < 0 or pos >= len(seq):
            continue
        aa = seq[pos]
        if aa in AVOID:
            continue
        out.append(pos)
    return out


def mutate_positions(seq: str, positions: List[int]) -> Tuple[str, List[str]]:
    seq_list = list(seq)
    muts = []
    for pos in positions:
        wt = seq_list[pos]
        new = choose_mutant_residue(wt)
        seq_list[pos] = new
        muts.append(f"{wt}{pos+1}{new}")
    return "".join(seq_list), muts


def make_second_gen_mutants(candidate: Candidate, n_mutants: int = 11) -> List[Tuple[str, str, List[str]]]:
    seq = candidate.sequence
    positions = valid_focus_positions(seq, candidate.focus_positions)

    mutants = []
    seen = set()

    while len(mutants) < n_mutants:
        if candidate.category == "hemicelluloses":
            n_changes = random.choice([1, 1, 2, 2, 3])
        else:
            n_changes = random.choice([1, 2, 2, 3])

        chosen = sorted(random.sample(positions, min(n_changes, len(positions))))
        mutant_seq, muts = mutate_positions(seq, chosen)

        key = tuple(muts)
        if key in seen:
            continue
        seen.add(key)

        mutant_name = f"{candidate.category}__gen2_mut{len(mutants)+1:02d}"
        mutants.append((mutant_name, mutant_seq, muts))

    return mutants


def write_outputs(all_mutants: List[Tuple[str, str, str, str, List[str]]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    fasta_path = outdir / "second_gen_mutants.fasta"
    csv_path = outdir / "second_gen_mutants.csv"

    with open(fasta_path, "w") as fasta, open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["category", "parent_name", "mutant_name", "mutations", "sequence"])

        for category, parent_name, mutant_name, seq, muts in all_mutants:
            fasta.write(f">{mutant_name}\n")
            fasta.write(seq + "\n")
            writer.writerow([category, parent_name, mutant_name, ",".join(muts), seq])


def main():
    outdir = Path("second_gen_mutant_generation_output")
    all_mutants = []

    for cand in CANDIDATES:
        muts = make_second_gen_mutants(cand, n_mutants=11)
        for mutant_name, mutant_seq, mut_list in muts:
            all_mutants.append((cand.category, cand.name, mutant_name, mutant_seq, mut_list))

    write_outputs(all_mutants, outdir)
    print(f"Wrote {len(all_mutants)} mutants total to {outdir}/")


if __name__ == "__main__":
    main()
