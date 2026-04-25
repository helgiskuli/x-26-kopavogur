/**
 * Shared utilities for Kópavogur 2026.
 * Loaded by issue pages that render numbers dynamically.
 * Keep this file small — add nothing without a cross-page use case.
 */

/**
 * Format a number in Icelandic style: period thousands, comma decimal.
 * formatIS(1234567.5) → "1.234.567,5"
 */
function formatIS(n, decimals = 0) {
  return n.toLocaleString('is-IS', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Format as milljónir króna (m.kr.), rounded to nearest integer.
 * formatMkr(1234) → "1.234 m.kr."
 */
function formatMkr(n) {
  return formatIS(Math.round(n)) + ' m.kr.';
}

/**
 * Format as milljarðar króna (ma.kr.), one decimal place.
 * formatMakr(3.15) → "3,2 ma.kr."
 */
function formatMakr(n) {
  return formatIS(n, 1) + ' ma.kr.';
}
