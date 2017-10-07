#!/usr/local/bin/python3
from localAligner import *
import sys
from argChecker import *
__author__ = 'Stef Streamer'

def printHelp():
    message = "\nThis program is an implementation of the Smith-Waterman local alignment algorithm with a linear gap model\n" \
              "This program will perform an alignment with the following default arguments if given none\n" \
              "Sequence Q: GCTGGAAGGCAT\n" \
              "Sequence P: GCAGAGCACG\n" \
              "Match score +5\n" \
              "Mismatch score -4\n" \
              "Gap penalty -4\n" \
              "\n\nProgram usage:\n" \
              "python3 swAlign.py\nOr\n" \
              "python3 swAlign.py <matchScore> <mismatchScore> <gapPenalty> <Sequence1> <Sequence2>\nOr \n" \
              "python3 swAlign.py --matchScore=<matchScore> --mismatchScore=<mismatchScore> --gapPenalty=<gapPenalty> --seq1=<seq1> --seq2=<seq2>\n"

    print(message)
    exit()

#Print the resulting alignment
def printAligment(aligner):
    #Alignment less than 60 nucleotides
    if len(aligner.finalQ) and len(aligner.finalP) <= 60:
        print(aligner.stringQName)
        print("Q: " + aligner.finalQ)
        print("P: " + aligner.finalP)
        print(aligner.stringPName)

    #Alignment is longer than 60 nucleotides so in keeping with fasta format
    #print 60 nucleotide slices of the alignment on a new line
    else:
        try:
            length = max(len(aligner.finalP), len(aligner.finalQ))
            print("Q = " + aligner.stringQName)
            print("P = " + aligner.stringPName + '\n')
            for index in range(0, length, 60):
                qSlice = aligner.finalQ[index:index+60]
                pSlice = aligner.finalP[index:index+60]
                print("Q:" + qSlice)
                print("P:"+ pSlice + '\n')

        except:
            print("Error printing alignment")


def main():
    #Check if the user asked for help
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            printHelp()
            exit()

    #Parameter names for user provided arguments at the command line
    argsNames = ["--matchScore=","--mismatchScore=","--gapPenalty=","--seq1=","--seq2="]

    #Determine if default arguments are to be used
    if len(sys.argv) == 1:
        #Perform local alignment on default parameters
        aligner = LocalAligner()
        aligner.calcTables()
        aligner.calcAlignemnt()
        #Print the alignment
        printAligment(aligner)

    #Determine if user would like to provide arguments
    elif len(sys.argv) == 6:
        #Read in arguments from the command line
        matchScore = sys.argv[1]
        mismatchScore = sys.argv[2]
        gapPenalty = sys.argv[3]
        fileQ = sys.argv[4]
        fileP = sys.argv[5]

        #check arguments and remove parameter names if present
        aList = [matchScore,mismatchScore,gapPenalty,fileQ,fileP]
        args = ArgChecker(argsNames, "swAlign.py")
        arguments = args.checkArgs(aList)
        matchScore = arguments[0]
        mismatchScore = arguments[1]
        gapPenalty = arguments[2]
        fileQ = arguments[3]
        fileP = arguments[4]

        #Perform local alignment
        aligner = LocalAligner(matchScore, mismatchScore, gapPenalty, fileQ, fileP)
        aligner.calcTables()
        aligner.calcAlignemnt()
        #Print the alignment
        printAligment(aligner)

    #Incorrect arguments
    else:
        arguments = ArgChecker(argsNames, "swAlign.py")
        arguments.printError()
        exit()


if __name__=='__main__':
    main()
