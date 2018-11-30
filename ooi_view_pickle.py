import ooi_classes as ooi
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


prmpt = input("Enter 1 for engineering, 2 for instruments: ")
    
# Define RSN Streams Object File
if prmpt == '1':
    in_file = 'rsn_eng_streams.pkl'
else:
    in_file = 'rsn_streams.pkl'

# Load RSN Data Structure
print('Loading %s' % in_file)
with open(in_file, 'rb') as input:
    rsn = pickle.load(input)

rsn.traversePrint()

