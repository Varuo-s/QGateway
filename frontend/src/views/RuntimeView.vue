<template>
  <div class="view-stack">
    <section class="glass-card feature-card models-header">
      <div>
        <div class="section-title">{{ labels.title }}</div>
        <p class="section-subtitle">{{ labels.subtitle }}</p>
      </div>
      <div class="top-actions">
        <button class="glass-button" @click="loadStatus">{{ labels.refresh }}</button>
        <button class="glass-button" @click="startRuntime">{{ labels.start }}</button>
        <button class="glass-button danger" @click="stopRuntime">{{ labels.stop }}</button>
      </div>
    </section>

    <section class="metric-grid three-metrics">
      <article class="glass-card metric-card compact">
        <span class="card-label">{{ labels.state }}</span>
        <strong>{{ stateLabel }}</strong>
      </article>
      <article class="glass-card metric-card compact">
        <span class="card-label">{{ labels.provider }}</span>
        <strong>{{ status?.provider ?? labels.unknown }}</strong>
      </article>
      <article class="glass-card metric-card compact">
        <span class="card-label">{{ labels.pid }}</span>
        <strong>{{ status?.pid ?? '--' }}</strong>
      </article>
    </section>

    <section class="glass-card feature-card">
      <div class="glass-table settings-table" v-if="status">
        <div class="glass-row"><span>{{ labels.endpoint }}</span><strong>{{ status.host }}:{{ status.port }}</strong></div>
        <div class="glass-row"><span>{{ labels.executable }}</span><strong>{{ status.executable }} · {{ status.executable_exists ? labels.exists : labels.missing }}</strong></div>
        <div class="glass-row"><span>{{ labels.model }}</span><strong>{{ status.model_path }} · {{ status.model_exists ? labels.exists : labels.missing }}</strong></div>
        <div class="glass-row"><span>{{ labels.command }}</span><strong>{{ status.command.join(' ') }}</strong></div>
        <div v-if="status.error" class="glass-row error-row"><span>{{ labels.error }}</span><strong>{{ status.error }}</strong></div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { getJson } from "../api/client";

type RuntimeStatus = {
  state: "stopped" | "running" | "error";
  provider: string;
  executable: string;
  executable_exists: boolean;
  model_path: string;
  model_exists: boolean;
  host: string;
  port: number;
  pid: number | null;
  command: string[];
  error: string | null;
};

const props = defineProps<{
  labels: {
    title: string; subtitle: string; start: string; stop: string; refresh: string; state: string; provider: string; pid: string; endpoint: string; executable: string; model: string; command: string; exists: string; missing: string; error: string; running: string; stopped: string; unknown: string;
  };
}>();

const status = ref<RuntimeStatus | null>(null);
const stateLabel = computed(() => {
  if (!status.value) return props.labels.unknown;
  if (status.value.state === "running") return props.labels.running;
  if (status.value.state === "stopped") return props.labels.stopped;
  return "Error";
});

async function postRuntime(path: string) {
  const response = await fetch(path, { method: "POST", headers: { Accept: "application/json", "Content-Type": "application/json" } });
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  status.value = await response.json() as RuntimeStatus;
}

async function loadStatus() { status.value = await getJson<RuntimeStatus>("/api/v1/runtime/status"); }
async function startRuntime() { await postRuntime("/api/v1/runtime/start"); }
async function stopRuntime() { await postRuntime("/api/v1/runtime/stop"); }

onMounted(loadStatus);
</script>
