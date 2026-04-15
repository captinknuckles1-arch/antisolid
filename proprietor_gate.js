const OWNER_ID = "LANCE-PULLEN-SOLID-LP";
const ASSET_MANIFEST = {
    "DAL-BRG-453": { value: "210,000,000", status: "LOCKED_PENDING_SETTLEMENT", owner: OWNER_ID },
    "44K_MASTER": { entities: 44218, status: "REVOKED_FOR_UNAUTHORIZED_USE" }
};

window.checkOwnership = (key) => {
    console.log("SOLID_OS: Ownership check initiated for node " + key);
    return ASSET_MANIFEST[key] || { status: "UNAUTHORIZED_COPY" };
};
