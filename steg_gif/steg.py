import sys
import argparse

def cmdline_args():
        # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("-hf", type=str,
                   help="File that you want to hide", required=True)
    p.add_argument("-cf", type=str,
                   help="Hide file into this file", required=True)
    p.add_argument("-o", type=str,
                   help="Out file", required=True)

    return(p.parse_args())

def main():
    args = cmdline_args()
    
    payload = args.hf
    file = args.cf
    out = args.o
    
    with open(payload, 'rb') as f:
        payload_data = f.read()
        
    with open(file, 'rb') as f:
        data = f.read()

    data = bytearray(data)
    payload_data = bytearray(payload_data)

    data.extend(payload_data)
    
    with open(out, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    main()