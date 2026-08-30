"use client";

import { useEffect, useState, useRef } from 'react';
import { API_BASE_URL } from '../lib/api';

export interface SSEEvent {
  event_type: string;
  investigation_id: string;
  timestamp: string;
  data?: Record<string, unknown>;
  payload?: Record<string, unknown>;
  agent?: string;
  round_number?: number;
}

export function useInvestigationSSE(investigationId: string | null) {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!investigationId) return;

    // Use FastAPI stream endpoint if API_BASE_URL is defined, else local events proxy
    const url = API_BASE_URL 
      ? `${API_BASE_URL}/api/investigations/${investigationId}/stream`
      : `/api/investigations/${investigationId}/events`;

    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        const normalized: SSEEvent = {
          event_type: parsed.event_type || parsed.event,
          investigation_id: parsed.investigation_id || investigationId,
          timestamp: parsed.timestamp || new Date().toISOString(),
          data: parsed.data || parsed.payload || {},
          payload: parsed.payload || parsed.data || {},
          agent: parsed.agent,
          round_number: parsed.round_number,
        };
        setEvents((prev) => [...prev, normalized]);
      } catch (err) {
        console.error('Error parsing SSE event', err);
      }
    };

    es.onerror = (err) => {
      console.warn('SSE EventSource error:', err);
      setIsConnected(false);
      setError('Connection interrupted. Retrying...');
    };

    return () => {
      es.close();
      setIsConnected(false);
    };
  }, [investigationId]);

  return { events, isConnected, error };
}
