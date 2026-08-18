#!/usr/bin/env python3
"""
Algorithm 1 Reference Implementation: In-Place Typed-Array ZIM Lexical Search & Range Scan
Demonstrates zero-copy binary search over contiguous raw byte buffers and typed-array offset tables.
"""

import struct
import array
import time
import argparse

class MockZimTypedArrayIndexer:
    def __init__(self, titles):
        """
        Initializes in-place binary buffer and typed array tables (Uint32Array and Uint16Array).
        """
        self.N = len(titles)
        raw_bytes_list = []
        offsets = []
        lengths = []
        
        current_offset = 0
        for t in sorted(titles, key=lambda s: s.lower()):
            b = t.encode('utf-8')
            raw_bytes_list.append(b)
            offsets.append(current_offset)
            lengths.append(len(b))
            current_offset += len(b)
            
        self.raw_buffer = b"".join(raw_bytes_list)
        # Using Python array('I') for 32-bit unsigned ints, array('H') for 16-bit unsigned ints
        self.offsets = array.array('I', offsets)
        self.lengths = array.array('H', lengths)
        
    def search_and_prefix_scan(self, query: str, max_results: int = 10):
        """
        Implements Algorithm 1: In-Place Binary Search & Range Scan
        """
        query_bytes = query.lower().encode('utf-8')
        low = 0
        high = self.N - 1
        match_idx = -1
        
        # 1. In-place binary search
        while low <= high:
            mid = low + ((high - low) // 2)
            entry_offset = self.offsets[mid]
            entry_len = self.lengths[mid]
            
            # Direct slice without full object instantiation
            entry_bytes = self.raw_buffer[entry_offset:entry_offset + entry_len].lower()
            
            if entry_bytes == query_bytes:
                match_idx = mid
                break
            elif entry_bytes < query_bytes:
                low = mid + 1
            else:
                high = mid - 1
                
        # 2. Probe insertion boundary for prefix match
        if match_idx == -1 and low < self.N:
            entry_offset = self.offsets[low]
            entry_len = self.lengths[low]
            if self.raw_buffer[entry_offset:entry_offset + entry_len].lower().startswith(query_bytes):
                match_idx = low
                
        # 3. Expand prefix scan window
        results = []
        if match_idx != -1:
            idx = match_idx
            while idx < self.N and len(results) < max_results:
                entry_offset = self.offsets[idx]
                entry_len = self.lengths[idx]
                title_slice = self.raw_buffer[entry_offset:entry_offset + entry_len]
                if title_slice.lower().startswith(query_bytes):
                    results.append({
                        "id": idx,
                        "title": title_slice.decode('utf-8'),
                        "byte_offset": entry_offset,
                        "length": entry_len
                    })
                    idx += 1
                else:
                    break
                    
        return results

def main():
    parser = argparse.ArgumentParser(description="Test Algorithm 1 In-Place Typed-Array ZIM Search")
    parser.add_argument("--query", type=str, default="quantum", help="Query string to search")
    args = parser.parse_args()
    
    sample_titles = [
        "Quantum mechanics", "Quantum computing", "Quantum entanglement", "Quantum electrodynamics",
        "Quantum field theory", "Quantum supremacy", "Quantum superposition", "Quantum teleportation",
        "Albert Einstein", "Arthur Schopenhauer", "Artificial intelligence", "Algorithm",
        "Deep learning", "Dense passage retrieval", "Reciprocal rank fusion", "Okapi BM25"
    ]
    
    indexer = MockZimTypedArrayIndexer(sample_titles)
    t0 = time.perf_counter()
    matches = indexer.search_and_prefix_scan(args.query)
    elapsed_us = (time.perf_counter() - t0) * 1e6
    
    print(f"Query: '{args.query}' (Found {len(matches)} matches in {elapsed_us:.2f} µs):")
    for m in matches:
        print(f"  * [Index {m['id']:03d} | Offset {m['byte_offset']:04d} | Len {m['length']:02d}]: {m['title']}")

if __name__ == '__main__':
    main()
