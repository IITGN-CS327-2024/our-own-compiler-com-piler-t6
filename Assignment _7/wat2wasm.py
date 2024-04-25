import subprocess

def wat_to_wasm(wat_path, wasm_path):
    try:
        subprocess.run(['wat2wasm', wat_path, '-o', wasm_path], check=True)
        print(f"WASM file created at {wasm_path}")
    except subprocess.CalledProcessError as e:
        print("Failed to convert WAT to WASM:", e)

wat_to_wasm('wat/arithmetic-test.wat', 'wasm/arithmetic-test.wasm')
