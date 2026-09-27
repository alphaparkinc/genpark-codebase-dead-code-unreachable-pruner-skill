import sys, json
from client import CodebaseDeadCodePruner

def main():
    pruner = CodebaseDeadCodePruner()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(pruner.run_benchmark_dead_code_pruning(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "build_call_graph", "description": "Construct caller-callee call graph from Python source."},
                        {"name": "find_unreachable_symbols", "description": "Find unreferenced functions from entry points."},
                        {"name": "run_benchmark_dead_code_pruning", "description": "Run dead code detection benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "build_call_graph":
                    out = pruner.build_call_graph(args.get("python_code", ""))
                elif tname == "find_unreachable_symbols":
                    out = pruner.find_unreachable_symbols(args.get("python_code", ""), args.get("entry_points", ["main"]))
                elif tname == "run_benchmark_dead_code_pruning":
                    out = pruner.run_benchmark_dead_code_pruning()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
