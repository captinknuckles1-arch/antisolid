const PROPRIETOR = "Solid LP (Lance Pullen)";
const STATUS_MANIFEST = {
    "DAL-BRG-453": { 
        name: "Solid Integrations LLC", 
        val: "210,000,000", 
        status: "ACCESS_REVOKED", 
        reason: "Non-Payment / Unauthorized IP Usage" 
    },
    "AMZ-088": { status: "LOCKED_BY_INVENTOR" },
    "APL-774": { status: "LOCKED_BY_INVENTOR" }
};

window.checkEAK = (key) => {
    const entry = STATUS_MANIFEST[key.toUpperCase()];
    if (entry) {
        alert("CRITICAL: " + entry.reason + "\nContact " + PROPRIETOR + " for Settlement.");
        return entry;
    }
    return { status: "NODE_NOT_FOUND", error: "403 Forbidden" };
};
