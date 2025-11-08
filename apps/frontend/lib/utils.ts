import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Normalizes an API URL by removing trailing slashes
 * and ensuring proper path construction
 */
export function normalizeApiUrl(baseUrl: string, path: string): string {
  const normalizedBase = baseUrl.replace(/\/+$/, '') // Remove trailing slashes
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${normalizedBase}${normalizedPath}`
}

/**
 * Gets the API base URL from environment variables
 */
export function getApiUrl(): string {
  return (process.env.NEXT_PUBLIC_API_URL || "https://your-backend.vercel.app").replace(/\/+$/, '')
}

