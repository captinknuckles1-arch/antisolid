const SOLID_ENTITIES = {
    "DAL-BRG-453": { name: "Solid Integrations LLC", settlement: "210,000,000", status: "VERIFIED" },
    "AMZ-088": { name: "AMAZON.COM INC", settlement: "1,250,000,000", status: "VERIFIED" },
    "APL-774": { name: "APPLE INC", settlement: "950,000,000", status: "VERIFIED" },
    "MSFT-101": { name: "MICROSOFT CORP", settlement: "520,000,000", status: "VERIFIED" }
};
window.checkEAK = (key) => SOLID_ENTITIES[key.toUpperCase()] || null;
console.log("SOLID_OS: Hard-Coded Revenue Nodes Active.");
