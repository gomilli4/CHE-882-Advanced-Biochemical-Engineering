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
For my work with Dr. Anstine (and actually the first part of the class), I ran all of my simulations on the development nodes. They have a time limit of 2 hours though, so I had to learn to submit jobs to the queue with slurm scripts (see /scripts/slurm). I mostly used the same script for all of the jobs, but I changed the name. They all had the same directory structure and job/file naming scheme, so it was fairly simple, especially with chat gpt.

The first file I tried to run was the run_proteins.sh file. I believe the main issue was the

```
#SBATCH --partition=gpu
```

line which requested a GPU, but didn't care which one. Like I said above, the only GPUs I could get AF3 to run on were the H200s, so in the improved, run_proteins_h200.sh script, I used

```
#SBATCH --gpus=h200:1
```

which specifically requested nodes with H200s. This fixed the issues I was having with the interference steps crashing, and things went smoothly.

Another important line was this one:

```
#SBATCH --array=0-32%4
```

With this line, I was instructing the scheduler to only use a maximum of 4 workers. I was afraid that if I requested a larger number of workers or nodes, then I would be kicked down the queue because my jobs were requesting too many resources. I was told after the fact that when I use an array like this, that doesn't matter, so all I accomplished was increasing the time it took the jobs to run.

Speaking of the time, after I fixed the slurm script, I sat in the queue for 30 hours. After that, the jobs ran in less than 12 which I was happy with. After that though, I was in the queue very quickly. The job I ran immediately after the first took only 4 minutes or so to start running which I found surprising. Maybe by the time I started it, all the other students on campus were done running their semester projects and things were calming down.

### The Evolutionary Algorithm
Like Aaron and Nick, I wanted to create modified versions of the inhibitors for each of the 4 enzyme categories. To do this, I ran the first job on the inhibitors I found, and collected the best scores. Then, with chat gpt, I created my own mutation script, which applied "less-than-random" mutations to the proteins (see /scripts/mutation_scripts). I could have, and probably should have, used RFDiffusion like my group members did, but I have a hard time not trying to reinvent the wheel.

Because of all the work Aaron did to identify the most effective residues to mutate in the xylanase inhibitors, I had the script only mutate amino acids within that range. For the other proteins though, the script applied 2 to 4 mutatations per sequence. Instead of mutating randomly, though, the script mutates amino acids to other "similar" acids, meaning charged residues were swapped with other charged residues, non-polar residues with other non-polar, and then I avoid mutating amino acids that had the chance to drastically alter the structure of the protein like cytosine.

This all worked fairly well. After collecting the mutated sequence, I used the same scripts before to create the new inhibitor.fasta files, and then the generate_jsons.py script created the next generation of input files for AF3.

### Results
I was able to run the first, unmutated test, and then one full mutation test which I called "generation 1". I was able to run generation 2 (mutated top performers of the gen 1 mutants), but something went wrong and I didn't have all of the files. In the slurm script (the new version), I gave each job a 4 hour time window. In my investigations, most of the jobs ran in 30 minutes (on average) so I thought 4 hours was plenty of time. It is possible though that there were some time outs. Maybe as the evolutionary algorithm attempted to improve the ipTM scores, AF3 had to work harder to figure out the binding mechanics, and that pushed the job times above 4 hours. There could also have been situations where there was some crash or some other event that canceled the jobs. I have what could be a more complete gen 2 dataset that I had Dr. Anstine run on his own server and equipment, but I couldn't include it in the analysis because it took over 24 hours to run on his equipment (which I found very strange because his server has H200s and other really good GPUs in it). Regardless, I was able to collect some potentially interesting data.

#### Interesting Results 1
Between the unmodified inhibitors and the 1st generation mutants, there was what I thougth was an interesting trend toward the ipTM scores improving. I know that 11 proteins per generation and only 2 generations of computations really isn't good enough for an evolutionary algorithm to substantially change the binding affinities, but things did appear to improve. The averages all increased, but the spread also increased so I'm not sure exactly how much of an improvement was made. Additionally, it's possible that *no* improvements were actually made. I could have just selected the top performers and culled the poor performers, so the overall scores would improve without the mutations actually doing anything useful. This idea is supported by the 2nd generation mutants which killed the trend. In some cases, like the alpha glycans, the average was improved significantly. For the others, though, the averages either decreased or shifted up slightly while still existing within the previous generation's spread. Like I said, using RFDiffusion would have been better, as well as using significantly larger generation sizes, and a larger number of generations.

#### Interesting Results 2
Another interesting point that I brought up earlier was the fact that I may have identified a potential pectin lyase inhibitor. There was one polygalacturonase inhibitor that binded exceptionally well to the pectinase which I didn't expect. Given that characterized pectinases are difficult to find in literature, and this protein was predicted to be effective before I even mutated anything, it might be good to take that protein and note somewhere that experiments should be done to confirm whether or not it is a pectinase inhibitor.

# References
Please see literature.md for the papers I read for this project.
