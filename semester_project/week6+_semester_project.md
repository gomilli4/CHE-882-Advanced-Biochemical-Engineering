# Semester Project

In this project, we were given two different datasets. Aaron and Nicholas worked on the first set which was full of xylanases. Their goal was to create a modified version of the RIXI xylanase inhibitor that would be more effective at inhibiting all of the xylanases in their dataset. I worked on the second dataset which wasn't nearly as organized.

### Identification
To begin, I needed to identify which enzymes in the dataset were which. Some of them were easy enough to find, because the data file included the UniProt IDs. The others, however, only included the amino acid sequences. To identify these, I used  tools like BLASTP searches, and searches in InterPro and CDD which are both databases of conserved domains and functional groups. Some of the proteins had names or there were probable guesses for what they were, but for the others I just had to guess.

At the end of the process, I identified approximately 10 different "classes" of enzyme:

polygalacturonases	2
pectin lyases	1
alpha glycans	3
beta glycosidases	3
endoglucanases	2
Hemicelluloses	4
chitinases	2
rhamnogalacturonan hydrolases	1
glycoside hydryolases 128	1
glycoside hydryolases 131	2

I say approximately because some of them are in different parts of the same family like the glycoside hydrolases (GHs). Regardless, I wasn't able to use all 10 of the categories. I couldn't find inhibitors for the beta glycosidases, the chitinases, or the two GH family proteins. I also couldn't find any specific inhibitor for the rhamnogalacturonan hydrolase. That left me with

Group A:
polygalacturonases, pectin lyase

Group B:
alpha glycans

Group C:
endoglucanases

Group D:
Hemicelluloses

### Finding Inhibitors
After identifying which enzymes I even had, I needed to find inhibitors for them. The Hemicellulose-consuming enzymes were the easiest category. This group includes xylanases, and Aaron and Nick had spent a bunch of time modifying the RIXIs so I took their top five performing RIXI mutants, then used their sequences to find other xylanse inhibitors with BLASTP. This was fairly simple since these proteins have been better characterized than some of the others.

The next simplest group was the polygalacturonases. These are well known cell wall degrading enzymes, and I was able to find a number of inihibitors. I couldn't find any pectin lyase specific inhibitors (intentionally, during the simulations AF3 was fairly confident that one of the polygalacturonase inhibitors was effectively a pectinase inhibitor), but pectinases and polygalacturonases tend to be linked in the same group in the literature, so I just bundled them together.

For the endoglucanases, I was able to find a paper talking about the xyloglucan specific fungal endoglucanase inhibitor (XEGIP), and its fasta file online. This allowed me to do a BLASTP search, download the entire search, then input that search into CD-HIT, which is a very convenient tool for reducing the redundant sequences from a blast search (see /files/cd-hit_example. This folder contains the xegip fasta sequence I searched with on the BLASTP website, the seqdump file I downloaded from the search containing all of the results, and the two output files from CD-HIT which are a list of the representative sequences in the clusters it determined, and the total clusters with all of the proteins from the seqdump file.). To use CD-HIT, the command is

```
cd-hit -i seqdump.txt -o cdhit_output.fasta -c 0.7 -n 5
```

This command tells CD-HIT that the seqdump.txt file is the input it should analyze, to output its data to cdhit_output.fasta, that I want sequences that are 70% similar, and that the "window" size it uses to compare sequences should be 4 amino acids long.

Finally, I needed to find inhibitors for the alpha glycans. Doing a search, I was able to find a number of potential inhibitors from plant species like *Phaseolus vulgaris*, which made the rest of the process very similar to the endoglucanases. I did a BLASTP search, downloaded the data dump, and used CD-HIT to narrow down the search.

### Collecting the Data
Now that I had all of the potential sequences, I needed a way to get them into a usable format. To do this, I had chat gpt write a script that sorted the many many sequences and clusters into the top 11 candidates, by cluster length (/scripts/top_11_sequences/cluster_search.py). After collecting the top 11 sequences from each of the CD-HIT searches, I combined them into inhibitors.fasta files (see inputs folder), and the combined the enzymes into enzyme.fasta files. Each of these files are just lists of the enzymes.

For the next step, I had chat gpt create another script (/scripts/json_creation) that took in and read the enzyme and inhibitors files, then created a json AF3 input file for each of the combinations. As an example, if I had 2 enzymes and 3 inhibitors, then the generate_jsons.py file would create 6 jsons. The output of this file was a folder containing all of the jsons, and a job_list.txt file which would be used by the slurm script to choose the correct json file for the job it needed to run next.

After running generate_jsons.py on all of the enzyme/inhibitor file pairs for the 4 different enzyme categories, I had all of my input files generated and could move on to running the AF3 model.

### AlphaFold3
AlphaFold3 wasn't really that hard to run, assuming I could find the correct GPUs to run them on. I had an issue where I would test my slurm script (/scripts/slurm) and it would run perfectly on the dev-amd24-h200 dev node, but would crash when it was run by the actual scheduler. It was even more annoying because the only thing that would crash was the neural network inference steps (which was the shortest step), so I would wait almost 30 minutes for the CPU side database and MSA processing to be done, only for the job to crash at the important part. Eventually, chat gpt helped me specifically request *ONLY* nodes with H200s on them, which let everything run just fine.

#### Submitting to the Queue
For my work with Dr. Anstine (and actually the first part of the class)
