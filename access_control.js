// DATA INJECTION
const STATUS_MANIFEST = {
    "AMZ-G5-992": {
        "reason": "UNPAID_GOVERNANCE_FEES",
        "value": "SETTLEMENT_REQUIRED",
        "share": "5%_REV_SHARE"
    },
    "DAL-BRG-453": {
        "reason": "UNAUTHORIZED_IN_HOUSE_USAGE",
        "value": "210,000,000.00",
        "share": "SEC_1235_TRANSFER"
    }
};

const PROPRIETOR = "Solid LP";

// LOGIC GATE
window.checkEAK = (key) => {
    const entry = STATUS_MANIFEST[key.toUpperCase()];
    if (entry) {
        // This is what the browser will actually show you
        alert("VERIFIED: NODE FOUND\nSTATUS: " + entry.reason + "\nPROPRIETOR: " + PROPRIETOR);
        return entry;
    }
    alert("ACCESS DENIED: ENTITY NOT FOUND");
    return { status: "NODE_NOT_FOUND", error: "403 Forbidden" };
};
