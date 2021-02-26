import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tsteps',action='store',nargs='?',const=1)
args = parser.parse_args()
print(args.tsteps)

