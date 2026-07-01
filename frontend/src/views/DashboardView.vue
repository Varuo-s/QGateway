<template>
  <div class="view-stack">
    <section class="metric-grid">
      <article class="glass-card metric-card">
        <span class="card-label">{{ labels.backend }}</span>
        <strong>{{ health?.status ?? labels.checking }}</strong>
        <small>{{ health?.service ?? 'QGateway' }}</small>
      </article>
      <article class="glass-card metric-card">
        <span class="card-label">{{ labels.runtime }}</span>
        <strong>{{ health?.runtime ?? labels.unknown }}</strong>
        <small>{{ labels.uptime }} {{ health?.uptime_seconds ?? 0 }}s</small>
      </article>
      <article class="glass-card metric-card">
        <span class="card-label">{{ labels.version }}</span>
        <strong>{{ health?.version ?? 'alpha-0.1' }}</strong>
        <small>{{ labels.milestone }}</small>
      </article>
    </section>

    <section class="glass-card feature-card">
      <div class="section-title">{{ labels.scope }}</div>
      <div class="glass-table two-columns">
        <div class="glass-row"><span>{{ labels.healthApi }}</span><strong>{{ labels.ready }}</strong></div>
        <div class="glass-row"><span>{{ labels.settings }}</span><strong>{{ labels.readOnly }}</strong></div>
        <div class="glass-row"><span>{{ labels.logs }}</span><strong>{{ labels.logViewer }}</strong></div>
        <div class="glass-row"><span>{{ labels.launcher }}</span><strong>{{ labels.detectionOnly }}</strong></div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  labels: {
    backend: string;
    runtime: string;
    version: string;
    uptime: string;
    milestone: string;
    scope: string;
    healthApi: string;
    settings: string;
    logs: string;
    launcher: string;
    ready: string;
    readOnly: string;
    logViewer: string;
    detectionOnly: string;
    unknown: string;
    checking: string;
  };
  health: null | {
    status: string;
    service: string;
    version: string;
    runtime: string;
    uptime_seconds: number;
  };
}>();
</script>
