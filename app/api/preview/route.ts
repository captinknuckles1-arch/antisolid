import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json(
    { preview: true },
    { headers: { 'Set-Cookie': 'preview=1; Path=/;' } }
  );
}
