#!/usr/bin/env python3

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


random.seed(42)


@dataclass
class Candidate:
    category: str
    name: str
    sequence: str


CANDIDATES = [
    Candidate(
        category="alpha_glycans",
        name="GLT69121.1_hypothetical_protein_SLA2020_412970_Shorea_laevis",
        sequence=(
            "MATIFFCSFKLPLFFLPFLLPYANSLSFQISRFEPNASNILYQGEAGPSDGAIEMNTIDYSYRVGRATYA"
            "ERVPLWDSNTGNISDFTTHFSFIIDTLGQDIYSDGLAFFLAPVGFEISPNSAGGYLGLFNFTTKNSSQNQ"
            "IVLVEFDSYANPEWDPPVEHVGININSLSSAVSTPWNASFHSGDIANVWITYNASTKNLSVSWSYQRTSN"
            "SQENTTLSYDIDLPKILPEWVTIGFSAAFGLYSERHTLLSWEFSSSLDIKETSGKKAKNTRLIMSLTVSS"
            "GILIVGLIIAFAIFWRHKQKRRKTAEMVNLTSINEDLEGGVGPRKFSYNELVSATYNFLNERKLGEGGFG"
            "AVYKGYLTDLTPIAVKKISRGLNRGRKNTSPK"
        ),
    ),
    Candidate(
        category="endoglucanases",
        name="XP_038706902.1_probable_aspartic_proteinase_GIP2_Tripterygium_wilfordii",
        sequence=(
            "MALSSHFLLLCSLLFFIISPSIAQTSFRPKALVLPVSKDPSTLQYITKINQRTPLVPINLTLDVGGQFSW"
            "VDCEQGYVSSTYKPVRCRSAQCSLARSRSCITECYSPPRPGCNNNTCGVLPDNPFSRTGTGGELGQDVVS"
            "VQSTDGFNPTRVVSVPSLIFTCANTFLLEGLANGVKGIAGLGRTKISLPSQFSAAFSFHRKFAVCLTSST"
            "RANGVVFFGDGPYVLLPNIEVSKNLIYTPLILNPVSTASAYFAGEPSADYFIGVKSIKINGKVVKFNATL"
            "LSINKEGYGGTKISSVNPYTVMESTIYNAVINAFVRELSSVSRVAAVAPFGACFNGKEIGSTRVGPAVPQ"
            "IDLVLQSESVYWRIFGANSMVQVSSDVLCLGFVDGGVDPRTSIVIGGHQIEDNLLQFDLASSRLGFSSSL"
            "LFRQTTCANFNFTSKL"
        ),
    ),
    Candidate(
        category="hemicelluloses",
        name="rixi_1_B",
        sequence=(
            "AGKTGQMTVFWGRNKNEGTLKETCDTGLYTTVVISFYSVFGHGRYWGDLSGHDLRVIGADIKHCQSKNIF"
            "VFLSIGGAGKDYSLPTSKSAADVADNIWNAHMDGRRPGVFRPFGDAAVDGIDFFIDQGAPDHYDDLARNL"
            "YAYNSQYASKRVLRLTATVRCAFPDPRMKKALDTKLFERIHVRFYDDATCSYNHAGLAGVMAQWNKWTAR"
            "YPGSHVYLGLAAANVPGKNDNVFIKQLYYDLLPNVQKAKNYGGIMLWDRFYDKQTGYGKTVKYWA"
        ),
    ),
    Candidate(
        category="polygalacturonases",
        name="XP_017408146.1_polygalacturonase_inhibitor_2_Vigna_angularis",
        sequence=(
            "MARLSITVLIMVLFCRTALSELCNPQDKQALLQIKKELGNPTTLSSWLPNTDCCNPQWEGVSCDIDTKTY"
            "RVNSLDLTDLSLPKPYPIPSSVANLPYLSFLYISRINNLVGPISPSIAKLTKLRYLYITHTNVSGQIPHF"
            "LSQMKTLLTIDFSYNALSGTLPPSLSSLPNLLGISFDGNHISGAIPDSFGSFPKHFTVLTLSRNRLTGKI"
            "PATLAKLDLAFVDLSQNMLEGDASVLFGAKKERLQKINLAKNLLAFDLGKIRLSKSKDLGGLDLRNNRIY"
            "GNLPKVLTSFKYLKRLNVSYNNLCGEIPQGGKLQRFDESCYAHNKCLCGSPLPSCT"
        ),
    ),
]


# Conservative mutation pools meant to perturb interface chemistry
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

# For RIXI: only mutate within this discovered hotspot
RIXI_MOTIF = "YAYNSQYASKRV"


def choose_mutant_residue(wt: str) -> str:
    pool = MUTATION_POOLS.get(wt, "ASTNQKRDE")
    choices = [x for x in pool if x != wt]
    return random.choice(choices)


def mutate_sequence(seq: str, positions: List[int]) -> Tuple[str, List[str]]:
    seq_list = list(seq)
    muts = []
    for pos in positions:
        wt = seq_list[pos]
        new = choose_mutant_residue(wt)
        seq_list[pos] = new
        muts.append(f"{wt}{pos+1}{new}")
    return "".join(seq_list), muts


def valid_general_positions(seq: str) -> List[int]:
    positions = []
    n = len(seq)

    # avoid likely signal peptide / transmembrane-ish beginning and very tail
    start = 35
    end = n - 12

    for i in range(start, end):
        aa = seq[i]
        if aa in AVOID:
            continue
        # bias toward polar/charged/aromatic-ish residues likely to matter at interfaces
        if aa in "DENQKRSTYH":
            positions.append(i)
    return positions


def make_general_mutants(candidate: Candidate, n_mutants: int = 11) -> List[Tuple[str, str, List[str]]]:
    seq = candidate.sequence
    positions = valid_general_positions(seq)
    mutants = []
    seen = set()

    while len(mutants) < n_mutants:
        # 2–4 mutations per variant: enough to change behavior, not total chaos
        n_changes = random.choice([2, 2, 3, 3, 4])
        chosen = sorted(random.sample(positions, n_changes))
        mutant_seq, muts = mutate_sequence(seq, chosen)

        key = tuple(muts)
        if key in seen:
            continue
        seen.add(key)

        mutant_name = f"{candidate.category}__mut{len(mutants)+1:02d}"
        mutants.append((mutant_name, mutant_seq, muts))

    return mutants


def make_rixi_mutants(candidate: Candidate, n_mutants: int = 11) -> List[Tuple[str, str, List[str]]]:
    seq = candidate.sequence
    idx = seq.find(RIXI_MOTIF)
    if idx == -1:
        raise ValueError("RIXI motif not found in sequence.")

    motif_positions = list(range(idx, idx + len(RIXI_MOTIF)))

    # Focus mostly on the middle variable region, not the flanking YAY...KRV anchors
    # Y A Y N S Q Y A S K R V
    #         ^^^^^^^^^
    preferred_offsets = [3, 4, 5, 6, 7, 8]  # N S Q Y A S region-ish
    preferred_positions = [idx + o for o in preferred_offsets]

    mutants = []
    seen = set()

    while len(mutants) < n_mutants:
        n_changes = random.choice([1, 1, 2, 2, 3])
        chosen = sorted(random.sample(preferred_positions, n_changes))

        seq_list = list(seq)
        muts = []

        for pos in chosen:
            wt = seq_list[pos]

            # Slightly more focused pools for RIXI hotspot exploration
            if wt in "NQST":
                pool = "NQSTKRAD"
            elif wt == "Y":
                pool = "YFHSNQ"
            elif wt == "A":
                pool = "ASTVQ"
            else:
                pool = MUTATION_POOLS.get(wt, "ASTNQKRDE")

            choices = [x for x in pool if x != wt]
            new = random.choice(choices)
            seq_list[pos] = new
            muts.append(f"{wt}{pos+1}{new}")

        mutant_seq = "".join(seq_list)
        key = tuple(muts)
        if key in seen:
            continue
        seen.add(key)

        mutant_name = f"{candidate.category}__mut{len(mutants)+1:02d}"
        mutants.append((mutant_name, mutant_seq, muts))

    return mutants


def write_outputs(all_mutants: List[Tuple[str, str, str, str, List[str]]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    fasta_path = outdir / "first_gen_mutants.fasta"
    csv_path = outdir / "first_gen_mutants.csv"

    with open(fasta_path, "w") as fasta, open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["category", "parent_name", "mutant_name", "mutations", "sequence"])

        for category, parent_name, mutant_name, seq, muts in all_mutants:
            fasta.write(f">{mutant_name} | parent={parent_name} | muts={','.join(muts)}\n")
            for i in range(0, len(seq), 80):
                fasta.write(seq[i:i+80] + "\n")

            writer.writerow([category, parent_name, mutant_name, ",".join(muts), seq])


def main():
    outdir = Path("mutant_generation_output")
    all_mutants = []

    for cand in CANDIDATES:
        if cand.category == "hemicelluloses":
            muts = make_rixi_mutants(cand, n_mutants=11)
        else:
            muts = make_general_mutants(cand, n_mutants=11)

        for mutant_name, mutant_seq, mut_list in muts:
            all_mutants.append((cand.category, cand.name, mutant_name, mutant_seq, mut_list))

    write_outputs(all_mutants, outdir)
    print(f"Wrote {len(all_mutants)} mutants total to {outdir}/")


if __name__ == "__main__":
    main()
