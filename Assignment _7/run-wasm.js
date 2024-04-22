const fs = require('fs');
const path = require('path');

async function loadWasmFile() {
    const filePath = path.join(__dirname, 'test3.wasm'); // Replace 'output.wasm' with your WASM file's path
    const wasmBuffer = fs.readFileSync(filePath);
    const wasmModule = await WebAssembly.instantiate(wasmBuffer);

    // Assuming your module exports a function named 'main'
    const result = wasmModule.instance.exports.main(); // Execute an exported function
    console.log("Result from WASM:", result);
}

loadWasmFile();
