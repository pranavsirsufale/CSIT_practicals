from Bio.Seq import Seq

myDNA = Seq("ATGGCATTGTAATGGGCCGTA")
print("DNA Sequence: ", myDNA)


# Step 1: Sequence Operations
# 1. Reverse

# DNA is made up of a sequence letters A, T, C, G
# A pairs with T
# C pairs with G (Complementary base pairing)

print("Reversed DNA Sequence: ", myDNA[::-1])

# 2. Complement
# In DNA, bases pair like this A<->T and C<->G
print("My DNA complement seuqence is : ",myDNA.complement())

# 3. Reverse Complement

# This means you do both steps : Get the complement and then reverse it
# Example:
# Original:        A T G C
# Complement:     T A C G
# Reverse:        G C A T

print("My DNA reverse complement sequence is : ",myDNA.reverse_complement())


# Transcription
# Transcription is the process of making RNA from DNA
# All T (thymine) becomes U (uracil)

# Example:
# DNA:  A T G C
# RNA:  A U G C

myRNA = myDNA.transcribe()
print("My RNA sequence is : ",myRNA)


# Translation ( RNA to Protein)
# Translation is the process of making Protein from RNA
# In cells, RNA is used to make proteins, During translation:
# The RNA is read in groups of 3 bases (called codons)
# Each codon codes for a specific amino acid (building blocks of protein) , accoring to genetic code.
# Tralsation starts at the codon AUG (Methionine) and stops at a stop codnon (UAA, UAG, UGA)

# Example:
# RNA:      AUG         GCC         AUU
# Protein:  Methionine  Alanine     Isoleucine

myProtein = myRNA.translate()
print("My Protein sequence is : ",myProtein)


