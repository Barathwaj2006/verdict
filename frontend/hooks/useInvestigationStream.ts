import { useEffect, useState, useRef } from 'react';
import { API_BASE_URL } from '@/lib/api';

export type EventType = 
  | 'INVESTIGATION_STARTED' | 'ROUND_STARTED' | 'RESEARCH_PLAN_RECEIVED'
  | 'RESEARCH_MISSION_CREATED' | 'RESEARCHER_STARTED' | 'RESEARCHER_COMPLETED'
  | 'CLAIM_CREATED' | 'CLAIM_SELECTED_FOR_REVIEW' | 'COUNTER_EVIDENCE_FOUND'
  | 'VERIFICATION_SEARCH_STARTED' | 'EVIDENCE_MATRIX_CREATED' | 'LEAD_EVALUATION_STARTED'
  | 'LEAD_DECISION' | 'KNOWLEDGE_GAP_IDENTIFIED' | 'FOLLOWUP_MISSION_CREATED'
  | 'ROUND_COMPLETED' | 'INVESTIGATION_COMPLETED' | 'INVESTIGATION_FAILED';

export interface StreamEvent {
  investigation_id: string;
  timestamp: string;
  event_type: EventType;
  round_number?: number;
  agent?: string;
  payload: any;
  _id?: string;
}

export function useInvestigationStream(investigationId: string | null) {
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [status, setStatus] = useState<'IDLE' | 'CONNECTING' | 'CONNECTED' | 'RECONNECTING' | 'COMPLETED' | 'FAILED'>('IDLE');
  
  const eventIds = useRef<Set<string>>(new Set());

  useEffect(() => {
    if (!investigationId) return;

    setStatus('CONNECTING');
    const url = `${API_BASE_URL}/api/investigations/${investigationId}/stream`;
    let eventSource = new EventSource(url);

    const handleMessage = (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data);
        const eventType = data.event_type;
        
        // Deduplication using payload identity + timestamp
        const eventId = `${data.timestamp}-${data.event_type}-${JSON.stringify(data.payload).length}`;
        if (eventIds.current.has(eventId)) return;
        eventIds.current.add(eventId);

        setEvents(prev => [...prev, { ...data, _id: eventId }]);

        if (eventType === 'INVESTIGATION_COMPLETED') {
          setStatus('COMPLETED');
          eventSource.close();
        } else if (eventType === 'INVESTIGATION_FAILED') {
          setStatus('FAILED');
          eventSource.close();
        }
      } catch (err) {
        console.error('Failed to parse SSE', err);
      }
    };

    const handleOpen = () => {
      setStatus('CONNECTED');
    };

    const handleError = () => {
      if (status !== 'COMPLETED' && status !== 'FAILED') {
        setStatus('RECONNECTING');
      }
    };

    eventSource.onmessage = handleMessage;
    eventSource.onopen = handleOpen;
    eventSource.onerror = handleError;

    return () => {
      eventSource.close();
    };
  }, [investigationId]);

  return { events, status };
}
