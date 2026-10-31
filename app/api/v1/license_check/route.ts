import { NextRequest, NextResponse } from 'next/server';

const AUTHORIZED_NODES = new Set([
  process.env.SOLID_HARDWARE_ID || 'NODE_LANCE_MBA_01',
]);

export async function GET(req: NextRequest) {
  const nodeId = req.nextUrl.searchParams.get('id') || '';
  if (!AUTHORIZED_NODES.has(nodeId)) {
    return NextResponse.json(
      {
        status: 'REVOKED',
        framework: 'Solid OS Deterministic Governance Layer',
        notice: 'Access denied under DTSA 18 U.S.C. 1836 & TUTSA Tex. Civ. Prac. & Rem. Code Ch. 134A.',
      },
      { status: 403 }
    );
  }
  return NextResponse.json({
    status: 'ACTIVE',
    nodeId,
    rootHash: process.env.SOLID_FORENSIC_ROOT_HASH || '235021c9',
    timestamp: new Date().toISOString(),
  });
}
