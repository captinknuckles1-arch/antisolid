const VAULT = require('./ledger_vault.json');

window.checkEAK = (key) => {
    const spec = VAULT.billing_specs[key.toUpperCase()];
    if (spec) {
        return {
            status: spec.status,
            total_due: "$" + spec.invoice_amount,
            protocol: spec.type,
            legal_notice: "Attorney Commission (0.5%) reserved for JW Settlement Counsel."
        };
    }
    return { error: "404_INVALID_NODE" };
};
