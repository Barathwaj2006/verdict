import { NextRequest } from 'next/server';
import { getInvestigationSession } from '@/lib/investigationEngine';

export const dynamic = 'force-dynamic';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = getInvestigationSession(params.id);
  if (!session) {
    return new Response('Investigation not found', { status: 404 });
  }

  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      // Send past events
      session.events.forEach((evt) => {
        const chunk = `event: ${evt.event_type}\ndata: ${JSON.stringify(evt)}\n\n`;
        controller.enqueue(encoder.encode(chunk));
      });

      if (session.status === 'COMPLETED' || session.status === 'FAILED') {
        controller.close();
        return;
      }

      const subscriber = (chunk: string) => {
        try {
          controller.enqueue(encoder.encode(chunk));
          if (chunk.includes('INVESTIGATION_COMPLETED') || chunk.includes('INVESTIGATION_FAILED')) {
            session.subscribers.delete(subscriber);
            controller.close();
          }
        } catch {
          session.subscribers.delete(subscriber);
        }
      };

      session.subscribers.add(subscriber);

      req.signal.addEventListener('abort', () => {
        session.subscribers.delete(subscriber);
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
