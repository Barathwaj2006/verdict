import { NextRequest, NextResponse } from 'next/server';
import { createInvestigationSession, getAllInvestigations, toInvestigationViewState } from '@/lib/investigationEngine';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const objective = body.objective || 'Default Investigation';
    const constraints = body.constraints || [];

    const session = createInvestigationSession(objective, constraints);

    return NextResponse.json({
      investigation_id: session.id,
      status: session.status,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Failed to start investigation';
    return NextResponse.json(
      { error: message },
      { status: 500 }
    );
  }
}

export async function GET() {
  const sessions = getAllInvestigations();
  return NextResponse.json(sessions.map(toInvestigationViewState));
}
