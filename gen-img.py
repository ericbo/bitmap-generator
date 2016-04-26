import struct

################################################################################
#                                   FUNCTIONS
################################################################################
#Creates a bitmap header
def BmpHeader(dibHeaderSize, bitmapSize):
    dataArray = bytearray()
    dataArray += b'\x42\x4D' #BM id feild
    dataArray += intToByteString(14 + dibHeaderSize + bitmapSize, 4) #Size of the bitmap.
    dataArray += b'\x00\x00' #Reserved
    dataArray += b'\x00\x00' #Reserved
    dataArray += intToByteString(14 + dibHeaderSize, 4) #Offset till the pixle array begins

    return dataArray

#Create a pixle array representing a windows DIB header for a 24-bit image.
def winDibHeader24(width, height, bitmapSize):
    dataArray = bytearray()
    dataArray += b'\x28\x00\x00\x00' #Dib header size.
    dataArray += intToByteString(width, 4) #Width
    dataArray += intToByteString(height, 4) #Height
    dataArray += b'\x01\x00' #Planes, always 1
    dataArray += b'\x18\x00' #Bits per pixle
    dataArray += b'\x00\x00\x00\x00' #Pixle array compression. None in this case.
    dataArray += b'\x44\x61\x6E\x69' #intToByteString(bitmapSize, 4) #Bitmap size. Not required for BI_RGB
    dataArray += b'\x13\x0B\x00\x00' #Print resolution (pixle/metter) horizontal
    dataArray += b'\x13\x0B\x00\x00' #Print resolution (pixle/metter) vertical
    dataArray += b'\x65\x6C\x6C\x65' #Colors in pallet. Does not apply in 24-bit images.
    dataArray += b'\x00\x00\x00\x00' #Important colors. All in this case.

    return dataArray

def encodeRGB(red, green, blue):
    rgbArray = [blue, green, red] #Little endian.
    return bytearray(rgbArray)

#Formats an integer to an unsigned little endian string
# Source: https://docs.python.org/2/library/struct.html
def intToByteString(int, size):
    if(size == 1):
        return struct.pack("<B", int) #unsigned char
    if(size == 2):
        return struct.pack("<H", int) #unsigned short
    if(size == 4):
        return struct.pack("<I", int) #unsigned int/long
    if(size == 8):
        return struct.pack("<Q", int) #unsigned long long

#Given a two dimentional array of letters, representing colors i.e r for red, create a bytearray
def genBitMap(array):
    rowLen = len(array[0])  #How many rows this bitmap contains
    padding = 4 - ((rowLen * 3) % 4) #Each row must be a multiple of 4, if not padding must be appended.
    bitmap = bytearray()

    for i in reversed(range(len(array))): #Each Row
        for j in range(len(array[i])): #Each Col
            bitmap += charToRGB(array[i][j])
        if(padding != 4):
            for k in range(padding):
                bitmap += b'\x00'
    return bitmap

#Convert a character/string into an rgb byte array.
def charToRGB(char):
    if(char.lower() == "r"):
        return encodeRGB(255,0,0) #Red
    if(char.lower() == "b"):
        return encodeRGB(0,0,0) #Black

    return encodeRGB(255,255,255) #Default is white

################################################################################
#                               SCRIPT BEGINS
################################################################################

#Create pixle array + get its properties dynamicaly
imageArray = [['b','r','b','b','b','b','b','b','b','r','b'],['r','r','b','b','b','b','b','b','b','r','r'],['b','b','b','r','r','r','r','r','b','b','b'],['b','b','r','r','r','r','r','r','r','b','b'],['b','b','r','b','b','r','b','b','r','b','b'],['b','b','r','r','r','r','r','r','r','b','b'],['b','b','b','r','r','r','r','r','b','b','b'],['r','r','b','r','b','r','b','r','b','r','r'],['b','r','b','b','b','b','b','b','b','r','b']]
pixleArray = genBitMap(imageArray)
width = len(imageArray[0])
height = len(imageArray)
size = len(pixleArray)

#Create both the dib and bmp headers given the pixle array.
dibHeader = winDibHeader24(width,height, size)
bmpHeader = BmpHeader(len(dibHeader), len(pixleArray))

#Sequential writes will be implimeneted in the future, rather then doing it all in one chunk at the end.
f = open("test.bmp", 'wb+') #Read/Write in binary format. Overwrite old file or create a new one.
f.write(bmpHeader)
f.write(dibHeader)
f.write(pixleArray)
f.close()
