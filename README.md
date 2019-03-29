# binwalk-deltas
Compute deltas from a binwalk output file for estimating size of objects
identified by binwalk.

*Note: probably a more useful approach is to just dump the files out, see
https://github.com/ReFirmLabs/binwalk/wiki/quick-start-guide#file-extraction*

## Usage
```bash
# normal binwalk
➜ binwalk dist/binwalk_deltas-0.1.0-py2.py3-none-any.whl

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v2.0 to extract, compressed size: 803, uncompressed size: 2193, name: binwalk_deltas.py
850           0x352           Zip archive data, at least v2.0 to extract, compressed size: 406, uncompressed size: 775, name: binwalk_deltas-0.1.0.dist-info/METADATA
1325          0x52D           Zip archive data, at least v2.0 to extract, compressed size: 95, uncompressed size: 110, name: binwalk_deltas-0.1.0.dist-info/WHEEL
1486          0x5CE           Zip archive data, at least v2.0 to extract, compressed size: 48, uncompressed size: 56, name: binwalk_deltas-0.1.0.dist-info/entry_points.txt
1611          0x64B           Zip archive data, at least v2.0 to extract, compressed size: 17, uncompressed size: 15, name: binwalk_deltas-0.1.0.dist-info/top_level.txt
1702          0x6A6           Zip archive data, at least v2.0 to extract, compressed size: 305, uncompressed size: 502, name: binwalk_deltas-0.1.0.dist-info/RECORD
2570          0xA0A           End of Zip archive, footer length: 22

# binwalk with deltas
➜ binwalk-deltas <(binwalk dist/binwalk_deltas-0.1.0-py2.py3-none-any.whl ) dist/binwalk_deltas-0.1.0-py2.py3-none-any.whl
Offset       Est. Size       Object
0x0          850 Bytes       Zip archive data, at least v2.0 to extract, compressed size: 803, uncompressed size: 2193, name: binwalk_deltas.py
0x352        475 Bytes       Zip archive data, at least v2.0 to extract, compressed size: 406, uncompressed size: 775, name: binwalk_deltas-0.1.0.dist-info/METADATA
0x52d        161 Bytes       Zip archive data, at least v2.0 to extract, compressed size: 95, uncompressed size: 110, name: binwalk_deltas-0.1.0.dist-info/WHEEL
0x5ce        125 Bytes       Zip archive data, at least v2.0 to extract, compressed size: 48, uncompressed size: 56, name: binwalk_deltas-0.1.0.dist-info/entry_points.txt
0x64b        91 Bytes        Zip archive data, at least v2.0 to extract, compressed size: 17, uncompressed size: 15, name: binwalk_deltas-0.1.0.dist-info/top_level.txt
0x6a6        868 Bytes       Zip archive data, at least v2.0 to extract, compressed size: 305, uncompressed size: 502, name: binwalk_deltas-0.1.0.dist-info/RECORD
0xa0a        22 Bytes        End of Zip archive, footer length: 22