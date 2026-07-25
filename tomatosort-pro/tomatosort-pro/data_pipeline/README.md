# 🧱 Data Pipeline — Lambda + Medallion

**Lambda:** Speed Layer (Kafka, real-time) + Batch Layer (Cassandra + SQL, historical).

**Medallion:**
- 🥉 `bronze/` — raw sensor & camera data.
- 🥈 `silver/` — cleaned & aggregated data.
- 🥇 `gold/` — business KPIs & annotated training sets.
