"use client";

import { useEffect, useState, useRef } from 'react';
import { API_BASE_URL } from '../lib/api';

export interface SSEEvent {
  event_type: string;
  investigation_id: string;
  timestamp: string;
  data: Record<string, unknown>;
}

export function useInvestigationSSE(investigationId: string | null) {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!investigationId) return;

    const url = `${API_BASE_URL}/api/investigations/${investigationId}/events`;
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    es.onmessage = (event) => {
      try {
        const parsed: SSEEvent = JSON.parse(event.data);
        setEvents((prev) => [...prev, parsed]);
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
