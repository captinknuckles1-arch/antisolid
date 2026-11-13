import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json(
    {
      status: 'disabled',
      message: 'This legacy endpoint did not perform authoritative license verification.',
    },
    { status: 410 }
  );
}
