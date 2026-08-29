import { NextRequest, NextResponse } from 'next/server';
import { getInvestigationSession, toInvestigationViewState } from '@/lib/investigationEngine';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = getInvestigationSession(params.id);
  if (!session) {
    return NextResponse.json({ error: 'Investigation not found' }, { status: 404 });
  }

  return NextResponse.json(toInvestigationViewState(session));
}
