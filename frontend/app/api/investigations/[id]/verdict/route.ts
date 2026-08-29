import { NextRequest, NextResponse } from 'next/server';
import { getInvestigationSession } from '@/lib/investigationEngine';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = getInvestigationSession(params.id);
  if (!session) {
    return NextResponse.json({ error: 'Investigation not found' }, { status: 404 });
  }

  if (!session.finalVerdict) {
    return NextResponse.json({ error: 'Verdict not available yet' }, { status: 404 });
  }

  return NextResponse.json(session.finalVerdict);
}
