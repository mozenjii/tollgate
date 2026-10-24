# tollgate

An OpenAI-compatible gateway that sends each request to the cheapest model that is good enough, caches only when reuse is safe, and keeps working when a provider doesn't.

> **Status:** early. I'm at the design stage and there is no released code yet. The results table below stays empty until a script in this repo produces the numbers.

## The problem

Most apps send every request to the same expensive model, skip caching because a wrong cached answer is worse than a slow one, and learn about provider outages from their users. Gateways like LiteLLM, Portkey and OpenRouter already handle the plumbing. What's usually missing is evidence: how much quality did routing cost, how often does the cache serve the wrong answer, how long did recovery take.

## What it will do

- Speak the OpenAI chat API, so existing code only changes its base URL.
- Route by predicted difficulty, with the threshold chosen so quality loss stays inside a stated bound on a labelled set.
- Serve a cache hit only after the similarity match survives a check on names, numbers and dates, scoped to tenant, prompt version and model.
- Use circuit breakers, retry budgets and probe requests to route around failing providers, and always say which model answered.
- Enforce per-key budgets and rate limits, and emit OpenTelemetry traces and metrics.

## How I plan to know it works

| Measurement | How | Result |
|---|---|---|
| Cost saved at a bounded quality drop | Labelled set, per slice, against always-strong and always-cheap | not measured |
| Cache hit rate and wrong-hit rate | Labelled paraphrase and near-miss pairs | not measured |
| Time to detect and recover from an outage, error rate, spend | Scripted failures against a fake provider | not measured |
| Gateway overhead, p50 and p99 | Load test against a fake provider | not measured |

## Design notes

**A router with a guarantee.** Picking a routing threshold by eye gives you a feeling, not a bound. I'll calibrate it on labelled data with conformal risk control, so the expected quality loss is bounded under the assumption that live traffic looks like the calibration set. I'll compare it with a cascade that tries the cheap model first and escalates when a check fails.

**Wrong hits are the cache's real metric.** Hit rate is easy to inflate. "Order 123" and "order 456" embed almost identically and need different answers. The cache will require entities, numbers and dates to match before it serves a hit, and I'll plot hit rate against wrong-hit rate rather than quote one point.

**Write down the failure behaviour.** What happens to a stream that dies halfway? When does a fallback model count as compatible (context length, tool calling, JSON mode)? How many retries before a retry storm? Each of these gets an explicit rule and a test.

**Chaos as a test suite.** Failure scenarios (latency spikes, rate limits, malformed output, slow-drip streams) are scripted with fixed seeds, so recovery time is a number I can reproduce.

## Roadmap

- [ ] Gateway core with a fake provider that can fail on command
- [ ] Keys, budgets and tenant isolation
- [ ] Router and semantic cache with calibration
- [ ] Breakers, hedging and probe recovery
- [ ] Benchmarks and write-up

## Related projects

Part of a set of six projects about building LLM systems you can trust:
[evalgate](https://github.com/mozenjii/evalgate),
[policylens](https://github.com/mozenjii/policylens),
[docproof](https://github.com/mozenjii/docproof),
[tollgate](https://github.com/mozenjii/tollgate),
[redline](https://github.com/mozenjii/redline),
[casefile](https://github.com/mozenjii/casefile).

Built by Mohib Ahmad.
