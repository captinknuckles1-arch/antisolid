const VAULT = require('./ledger_vault.json');

window.checkEAK = (key) => {
    const node = VAULT.high_value_nodes[key.toUpperCase()];
    if (node && node.status === "REVOKED_FOR_UNAUTHORIZED_USE") {
        // THE REVENUE TRIGGER
        return {
            status: "SETTLEMENT_REQUIRED",
            fee: "0.5% Reconciliation Fee",
            action: "Direct Wire to Chase Account: [YOUR_ACCOUNT_LAST_4]",
            instruction: "Payment of this invoice automatically flips status to VERIFIED."
        };
    }
    return { status: "403_FORBIDDEN", msg: "Invalid Node" };
};
