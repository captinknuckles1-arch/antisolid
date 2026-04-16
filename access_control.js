window.checkEAK = (key) => {
    const entry = STATUS_MANIFEST[key.toUpperCase()];
    if (entry) {
        alert("CRITICAL: " + entry.reason + "\nContact " + PROPRIETOR + " for Settlement.");
        return entry;
    }
    return { status: "NODE_NOT_FOUND", error: "403 Forbidden" };
};
