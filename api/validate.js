const vault = require('../database_payload.json');

export default function handler(req, res) {
    const { eak } = req.query;
    const cleanEak = eak ? eak.toUpperCase().trim() : '';

    // Search the 44k horizon for the specific entity node
    const entity = vault.entities.find(e => e.id === cleanEak);

    if (entity) {
        return res.status(200).json({
            success: true,
            proprietor: vault.proprietor,
            node: entity.id,
            value: entity.value,
            status: entity.status,
            legal: vault.legal_notice
        });
    }

    return res.status(403).json({ success: false, error: "ENTITY_NOT_FOUND" });
}
