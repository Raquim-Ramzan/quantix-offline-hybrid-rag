#!/usr/bin/env python3
"""
Reciprocal Rank Fusion (RRF) Reference Evaluator
Implements the formal fusion equation:
    RRF(d) = sum_{m in M} 1 / (k + r_m(d))
where k = 60 by default.
"""

from typing import List, Dict, Tuple

def compute_rrf(
    dense_ranked_ids: List[str], 
    sparse_ranked_ids: List[str], 
    k: int = 60
) -> List[Tuple[str, float, int, int]]:
    """
    Computes reciprocal rank fusion scores for documents across dense vector and sparse BM25 rankings.
    Returns: Sorted list of tuples: (doc_id, rrf_score, dense_rank, sparse_rank)
    """
    dense_ranks = {doc_id: rank + 1 for rank, doc_id in enumerate(dense_ranked_ids)}
    sparse_ranks = {doc_id: rank + 1 for rank, doc_id in enumerate(sparse_ranked_ids)}
    
    all_doc_ids = set(dense_ranks.keys()) | set(sparse_ranks.keys())
    fused_results = []
    
    for doc_id in all_doc_ids:
        r_vec = dense_ranks.get(doc_id, float('inf'))
        r_bm25 = sparse_ranks.get(doc_id, float('inf'))
        
        vec_score = 1.0 / (k + r_vec) if r_vec != float('inf') else 0.0
        bm25_score = 1.0 / (k + r_bm25) if r_bm25 != float('inf') else 0.0
        
        total_rrf = vec_score + bm25_score
        fused_results.append((doc_id, total_rrf, r_vec, r_bm25))
        
    fused_results.sort(key=lambda x: x[1], reverse=True)
    return fused_results

def main():
    print("=" * 70)
    print("  RECIPROCAL RANK FUSION (RRF) SCORER (k = 60)")
    print("=" * 70)
    
    dense_candidates = ["doc_A", "doc_B", "doc_C", "doc_D", "doc_E"]
    sparse_candidates = ["doc_C", "doc_A", "doc_F", "doc_B", "doc_G"]
    
    results = compute_rrf(dense_candidates, sparse_candidates, k=60)
    
    print(f"{'Final Rank':<12} | {'Document ID':<14} | {'RRF Score':<12} | {'Dense Rank':<12} | {'Sparse Rank':<12}")
    print("-" * 70)
    for idx, (doc_id, score, r_vec, r_bm25) in enumerate(results, start=1):
        r_vec_str = str(r_vec) if r_vec != float('inf') else "None (inf)"
        r_bm25_str = str(r_bm25) if r_bm25 != float('inf') else "None (inf)"
        print(f"{idx:<12} | {doc_id:<14} | {score:<12.5f} | {r_vec_str:<12} | {r_bm25_str:<12}")

if __name__ == '__main__':
    main()
