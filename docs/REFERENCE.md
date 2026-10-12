# Reference database — NOT BUILT

Date: 2026-10-12. Candidate labels and adulterant sets are unresolved; creating a species-specific reference now would imply unsupported label choices. There is no `its2_reference.fasta`.

Planned procedure (UNTESTED): after verifying each label and plausible adulterants from primary literature, query NCBI Nucleotide for `<verified binomial>[Organism] AND (ITS2[Title] OR internal transcribed spacer 2[Title]) NOT environmental samples[Organism]`. Save the exact query, date, accession.version list, original GenBank records and FASTA, checksums, voucher information and exclusion reasons. Confirm ITS2 annotation, orientation, sequence quality, taxonomic identity and marker overlap; retain multiple reliable representatives and near neighbours. Produce headers `ACCESSION.VERSION|Genus_species`. Do not treat this narrow panel as proof that unrepresented taxa are absent.

No NCBI nucleotide query has yet been executed. No accession or sequence is invented.
