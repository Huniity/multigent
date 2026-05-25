import { useAuthStore } from '../store/authStore';

/**
 * A fetch wrapper that automatically injects the Authorization header and
 * handles expired access tokens by attempting a silent refresh.
 *
 * On a 401 response it:
 *  1. POSTs the stored refresh token to /api/auth/refresh/
 *  2. Persists the new access token via setTokens
 *  3. Retries the original request once with the new token
 *
 * If the refresh itself fails (expired / invalid refresh token), it clears
 * the auth state so the ProtectedRoute redirects to /login.
 */
export async function authFetch(
  input: RequestInfo | URL,
  init: RequestInit = {},
): Promise<Response> {
  const { accessToken, refreshToken, setTokens, clearTokens } =
    useAuthStore.getState();

  const makeHeaders = (token: string | null): HeadersInit => ({
    ...(init.headers as Record<string, string> | undefined),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  });

  // First attempt
  const res = await fetch(input, { ...init, headers: makeHeaders(accessToken) });

  if (res.status !== 401) return res;

  // Access token rejected — attempt silent refresh
  if (!refreshToken) {
    clearTokens();
    return res;
  }

  const refreshRes = await fetch('/api/auth/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  if (!refreshRes.ok) {
    clearTokens();
    return res; // return original 401 so callers can react
  }

  const { access } = (await refreshRes.json()) as { access: string };
  setTokens(access, refreshToken);

  // Retry with the new access token
  return fetch(input, { ...init, headers: makeHeaders(access) });
}
