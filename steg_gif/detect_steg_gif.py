import sys
import gif

    
def main():
    file = sys.argv[1]
    reader = gif.Reader()
    with open(file, 'rb') as f:
        reader.feed(f.read())
    
    length = 0
    for block in reader.blocks:
        length += block.length
    header_size = 13 + len(reader.color_table) * 3

    if length + header_size < len(reader.buffer):
        print("detected data at the end of gif")   
        data = reader.buffer[reader.blocks[-1].offset + 1:]
        with open('data.out', 'wb') as f:
            f.write(data)
        print("data written to data.out")

    else:
        print("no data detected")
        
    return

if __name__ == '__main__':
    main()