# UNTESTED TEMPLATE: DADA2 denoising of paired-end ITS2 amplicons -> ASV table.
# Usage: Rscript workflow/02_dada2_its2.R data/raw results
suppressMessages(library(dada2))
args <- commandArgs(TRUE); in_dir <- args[1]; out_dir <- args[2]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(out_dir, "filtered"), showWarnings = FALSE)
fnF <- sort(list.files(in_dir, pattern = "_1.fastq", full.names = TRUE))
fnR <- sort(list.files(in_dir, pattern = "_2.fastq", full.names = TRUE))
if (!length(fnF) || length(fnF) != length(fnR)) stop("Missing or unpaired FASTQ files")
if (!identical(sub("_1.fastq.*", "", basename(fnF)), sub("_2.fastq.*", "", basename(fnR)))) stop("FASTQ sample names differ")
samples <- sub("_1.fastq.*", "", basename(fnF))
filtF <- file.path(out_dir, "filtered", paste0(samples, "_F.fq.gz"))
filtR <- file.path(out_dir, "filtered", paste0(samples, "_R.fq.gz"))
# ITS2 length varies, so do NOT truncate to a fixed length (no truncLen)
filterAndTrim(fnF, filtF, fnR, filtR, maxN = 0, maxEE = c(2, 2), truncQ = 2,
              minLen = 50, multithread = TRUE)
errF <- learnErrors(filtF, multithread = TRUE); errR <- learnErrors(filtR, multithread = TRUE)
ddF <- dada(filtF, err = errF, multithread = TRUE); ddR <- dada(filtR, err = errR, multithread = TRUE)
merged <- mergePairs(ddF, filtF, ddR, filtR)
seqtab <- removeBimeraDenovo(makeSequenceTable(merged), method = "consensus", multithread = TRUE)
rownames(seqtab) <- samples
saveRDS(seqtab, file.path(out_dir, "seqtab.rds"))
if (!ncol(seqtab)) stop("No ASVs survived filtering")
ids <- paste0("ASV", seq_len(ncol(seqtab)))
writeLines(as.vector(rbind(paste0(">", ids), colnames(seqtab))), file.path(out_dir, "asvs.fasta"))
counts <- t(seqtab)
rownames(counts) <- ids
write.csv(counts, file.path(out_dir, "asv_counts.csv"))
