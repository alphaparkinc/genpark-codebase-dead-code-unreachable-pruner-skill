import sys, json
from client import CodebaseDeadCodePruner

def main():
    print("Testing CodebaseDeadCodePruner...")
    pruner = CodebaseDeadCodePruner()
    res = pruner.run_benchmark_dead_code_pruning()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["has_dead_orphan"] is True
    assert res["helper_is_reachable"] is True
    print("All Codebase Dead Code Pruner tests passed successfully!")

if __name__ == "__main__":
    main()
