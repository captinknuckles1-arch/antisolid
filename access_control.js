const VAULT = require('./ledger_vault.json');

window.checkEAK = (key) => {
    const node = VAULT.high_value_nodes[key.toUpperCase()];
    if (node) {
        console.log("SOLID_OS: INTERNAL VALIDATION SUCCESSFUL.");
        alert("STATUS: " + node.status + "\nVALUE: $" + node.value);
        return node;
    }
    return { status: "403_FORBIDDEN", msg: "Entity not in local vault." };
};
