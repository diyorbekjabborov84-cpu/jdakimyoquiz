"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  verifyAdminSessionWithRetry,
  DEFAULT_SESSION_RETRY_DELAYS_MS,
} from "./google-login";

export type AdminSessionState =
  | "checking"
  | "waking"
  | "authenticated"
  | "unavailable"
  | "unauthenticated";

export interface UseAdminSessionResult {
  adminUser: any;
  sessionState: AdminSessionState;
  isWaking: boolean;
  isUnavailable: boolean;
  isReady: boolean;
  retryAttempt: number;
  maxRetries: number;
  retrySession: () => void;
}

export function useAdminSession(): UseAdminSessionResult {
  const router = useRouter();
  const [adminUser, setAdminUser] = useState<any>(null);
  const [sessionState, setSessionState] = useState<AdminSessionState>("checking");
  const [retryAttempt, setRetryAttempt] = useState(0);
  const [maxRetries, setMaxRetries] = useState(DEFAULT_SESSION_RETRY_DELAYS_MS.length);
  const [trigger, setTrigger] = useState(0);

  const retrySession = useCallback(() => {
    setSessionState("checking");
    setRetryAttempt(0);
    setTrigger((prev) => prev + 1);
  }, []);

  useEffect(() => {
    let aborted = false;

    const run = async () => {
      setSessionState("checking");
      const result = await verifyAdminSessionWithRetry({
        fetchImpl: fetch,
        shouldAbort: () => aborted,
        onRedirectToLogin: (path) => {
          if (!aborted) {
            setSessionState("unauthenticated");
            router.push(path);
          }
        },
        onWakingChange: (waking, attempt, max) => {
          if (aborted) return;
          setMaxRetries(max);
          if (waking) {
            setSessionState("waking");
            setRetryAttempt(attempt);
          }
        },
      });

      if (aborted) return;

      if (result.status === "authenticated") {
        setAdminUser(result.user);
        setSessionState("authenticated");
      } else if (result.status === "unavailable") {
        setSessionState("unavailable");
      }
    };

    void run();

    return () => {
      aborted = true;
    };
  }, [router, trigger]);

  return {
    adminUser,
    sessionState,
    isWaking: sessionState === "waking",
    isUnavailable: sessionState === "unavailable",
    isReady: sessionState === "authenticated",
    retryAttempt,
    maxRetries,
    retrySession,
  };
}
