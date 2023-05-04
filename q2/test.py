import bwtzip
import bwtunzip

enc = bwtzip.full_enc('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccccccccccc')
dec = bwtunzip.full_dec(enc)
print(enc)
print(dec)