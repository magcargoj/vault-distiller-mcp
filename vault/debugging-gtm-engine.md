# Forensic Post-Mortem: GTM Job Engine Rate Limit Collision
**Date:** 2026-04-19
**Specialist:** Jeremy Wood
**Status:** Resolved / Documented

## Executive Summary
During the initial deployment of the `gtm_job_engine.py` scraper, the system encountered a cascading failure across three target job boards. The root cause was identified as a lack of jitter in the request headers, leading to a fingerprint match and immediate IP blacklisting.

## The Diagnostic Process
1. **Initial Symptom:** 403 Forbidden errors across all concurrent threads.
2. **Hypothesis:** Target sites implemented a sophisticated CAPTCHA challenge or fingerprinting.
3. **Forensic Evidence:** Analysis of the request headers revealed that the `User-Agent` was static, and the request interval was perfectly rhythmic (exactly 2.0s).

## The Fix
Implemented a `HeaderRotationEngine` and a `FibonacciJitter` class. 
- **Header Rotation:** Uses a pool of 50+ real-world browser fingerprints.
- **Jitter:** Instead of a static sleep, the engine now uses a randomized Fibonacci sequence to mimic human browsing patterns.

## Technical Takeaway
High-fidelity scraping isn't about speed; it's about transparency and mimicry. In a remote-first world, your tools must be as sophisticated as the platforms they interact with.

## Buffer Distillation Goal
Share this "Forensic Post-Mortem" format with my LinkedIn network to demonstrate how I approach technical failures with high-fidelity documentation.
